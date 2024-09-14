import logging
from gdrive_api import GDriveAPI
from etl_xls import XLSReader
from dash_creator import DashboardGenerator
from whatsapp_api import WS_API
import time
import os
import requests
import json


class DataPipeline:
    def __init__(self):
        # Constantes
        self.current_dir = os.path.dirname(__file__)
        self.id_folder_in = os.getenv('GH_ID_FOLDER_IN') #Para el archivo excel
        self.id_folder_out = os.getenv('GH_ID_FOLDER_OUT') #Donde se dejan las img a enviar en la Nube          
        self.id_file_cfg = os.getenv('GH_ID_FILE_CFG') # donde se encuentra credentials_module.json en la Nube
        #self.directorio_credenciales = os.path.join(self.current_dir, 'cfg','credentials_module.json')    
        self.whatsapp_token = os.getenv('GH_WHATSAPP_TOKEN')
        

        self.credenciales_dic = self.descargar_json_desde_drive(self.id_file_cfg)

        if self.credenciales_dic:
            logging.info("Datos descargados correctamente:")            
        else:
            logging.info("Error al descargar o procesar el archivo JSON.")

        self.img_base_path = os.path.join(self.current_dir, 'img')

        #self.gdrive_api = GDriveAPI(self.directorio_credenciales,self.credenciales_dic)
        self.gdrive_api = GDriveAPI(self.credenciales_dic)
        self.etl_xls = XLSReader()
        self.dash_creator = DashboardGenerator()
        self.whatsapp_api = WS_API()

        # Configuración básica de logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                #logging.FileHandler("pipeline.log"),
                logging.StreamHandler()
            ]
        )   

        

    def run_pipeline(self):
        # dash_names = ['main_dash','budget_dash','categoria_bar_dash']
        dash_names = ['main_dash']

        # Leer Informacion desde el excel en Gdrive        
        id_file_xls_subido = self.buscar_id_archivo('(BBVA)_Movimientos_Tarjeta.xls',self.id_folder_in)                   
        data = self.etl_xls.etl_info(id_file_xls_subido)

        # Se Recorre los dashboard a Generar:
        for dash in dash_names:
            try:
                logging.info(f"                                    ")
                logging.info(f"  --->    INI : {dash}       <---   ")                
                # Paso 1: Busco archivos para Eliminar:
                self.buscar_y_borrar_archivo_img(f"{dash}.png")
                logging.info(f"{dash} ELIMINADO")

                # Paso 2: Generar el dashboard
                #PENDIENTE Ver como guardar los archivos en carpeta relativa
                if dash == 'main_dash':
                    self.dash_creator.main_dash(data)   
                    logging.info(f"Dashboard {dash} CREADO")
                elif dash == 'budget_dash':
                    self.dash_creator.budget_dash(data)
                    logging.info(f"Dashboard {dash} CREADO")   
                elif dash == 'categoria_bar_dash':
                    self.dash_creator.categoria_bar_dash(data)
                    logging.info(f"Dashboard {dash} CREADO")
                
                # Paso 3 : Subo el archivo de la imagen generada al google drive                
                img_path_send = os.path.join(self.current_dir, 'img',f"{dash}.png")                
                
                self.gdrive_api.subir_archivo(img_path_send,
                                            self.id_folder_out)
                logging.info("Esperando para subir archivo ...")   
                time.sleep(10)
                logging.info("Subiendo archivo ...")
                logging.info(f"Imagen {dash}.png subida a GDrive")

                # Paso 4 : busco el Id del file que se ha subido al GDrive para crear el link y enviarlo x el API de FB/WS           

                id_file_subido = self.buscar_id_archivo(f"{dash}.png",self.id_folder_out)            

                # Paso 5: Enviar la Imagen por medio del link
                #PENDIENTE pasar parametro FB_WHATSAPP_TOKEN
                if id_file_subido:
                        
                        self.whatsapp_api.send_img_via_whatsapp(id_file_subido,self.whatsapp_token)
                        logging.info(f"Imagen {dash}.png enviada por WhatsApp")
                else:
                        logging.warning(f"No se encontró el archivo {dash}.png en GDrive tras subirlo")
                
                logging.info(f"  --->    FIN : {dash}       <---   ")
            except Exception as e:
                logging.error(f"Error en el pipeline de {dash}: {str(e)}")
            #self.whatsapp_api.send_img_via_whatsapp(id_file_in_folder)
            #print("img Enviada")

            # Agregar logging

    def buscar_y_borrar_archivo_img(self, filename):
        """
        Busca un archivo por su nombre en Google Drive y lo elimina si existe.
        """
        ids_file, titles = self.gdrive_api.buscar_archivos_en_folder(
            self.id_folder_out)

        for i, title in enumerate(titles):
            if title == filename:
                self.gdrive_api.borrar_recuperar(
                    ids_file[i])
                return ids_file[i]  # Retornar el ID del archivo eliminado
        logging.warning(f"Archivo {filename} no encontrado en GDrive para eliminar.")
        return None
    
    def buscar_id_archivo(self, filename,id_folder):
        """
        Busca un archivo por su nombre en Google Drive y retorna su ID si existe.
        """
           
        ids_file, titles = self.gdrive_api.buscar_archivos_en_folder(id_folder)

        for i, title in enumerate(titles):
            if title == filename:
                return ids_file[i]
        logging.warning(f"Archivo {filename} no encontrado en GDrive.")
        return None
    
    def descargar_json_desde_drive(self,file_id):
        url = f'https://drive.google.com/uc?id={file_id}'
        
        # Realizar una solicitud GET para obtener el archivo
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Verificar que la solicitud fue exitosa
        except requests.exceptions.RequestException as e:
            logging.info(f"Error al descargar el archivo: {e}")
            return None
        
        try:
            # Leer el archivo JSON desde el contenido de la respuesta
            json_data = json.loads(response.content.decode('utf-8'))
            return json_data
        except json.JSONDecodeError as e:
            logging.info(f"Error al decodificar el archivo JSON: {e}")
            return None


# Ejemplo de uso
if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()
