#library to Gdrive API
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError
import logging

import tempfile
import json

class GDriveAPI:
    def __init__(self,credenciales_dict):
        self.credenciales_path = self.save_credentials_to_temp_file(credenciales_dict)
        self.credenciales = self.login(self.credenciales_path)
        

    def save_credentials_to_temp_file(self, credenciales_dict):
        # Crear un archivo temporal para guardar las credenciales JSON
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        with open(temp_file.name, 'w') as f:
            json.dump(credenciales_dict, f)
        return temp_file.name

    def login(self,directorio_credenciales):
        # INICIAR SESION
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(directorio_credenciales)
        
        if gauth.credentials is None:
            gauth.LocalWebserverAuth(port_numbers=[8092])
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
            
        gauth.SaveCredentialsFile(directorio_credenciales)
        #credenciales = GoogleDrive(gauth)
        #return credenciales
        return GoogleDrive(gauth)

    def crear_archivo_texto(self, nombre_archivo,contenido,id_folder):        
        archivo = self.credenciales.CreateFile({'title': nombre_archivo,\
                                        'parents': [{"kind": "drive#fileLink",\
                                                        "id": id_folder}]})
        archivo.SetContentString('Hey MoonCoders!')
        archivo.Upload()


    # SUBIR UN ARCHIVO A DRIVE
    def subir_archivo(self, ruta_archivo, id_folder):        
        try:
            archivo = self.credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                            "id": id_folder}]})
            #LEER: para WINDOWS usar esta linea -> archivo['title'] = ruta_archivo.split("/")[-1]
            #LEER: para WINDOWS y relativo usar esta linea -> archivo['title'] = ruta_archivo.split("\\")[-1]
            archivo['title'] = ruta_archivo.split("/")[-1]
            archivo.SetContentFile(ruta_archivo)
            archivo.Upload()
        except FileNotUploadedError as e:
            logging.info(f"Error al subir el archivo: {e}")
        except Exception as e:
            logging.info(f"Error desconocido: {e}")

    # DESCARGAR UN ARCHIVO DE DRIVE POR ID
    def bajar_archivo_por_id(self, id_drive, ruta_descarga):
        
        archivo = self.credenciales.CreateFile({'id': id_drive}) 
        nombre_archivo = archivo['title']
        archivo.GetContentFile(ruta_descarga + nombre_archivo)

    # BUSCAR ARCHIVOS
    def busca(self, query):
        resultado = []
        
        # Archivos con el nombre 'mooncode': title = 'mooncode'
        # Archivos que contengan 'mooncode' y 'mooncoders': title contains 'mooncode' and title contains 'mooncoders'
        # Archivos que NO contengan 'mooncode': not title contains 'mooncode'
        # Archivos que contengan 'mooncode' dentro del archivo: fullText contains 'mooncode'
        # Archivos en el basurero: trashed=true
        # Archivos que se llamen 'mooncode' y no esten en el basurero: title = 'mooncode' and trashed = false
        lista_archivos = self.credenciales.ListFile({'q': query}).GetList()
        for f in lista_archivos:
            # ID Drive
            print('ID Drive:',f['id'])
            # Link de visualizacion embebido
            print('Link de visualizacion embebido:',f['embedLink'])
            # Link de descarga
            print('Link de descarga:',f['downloadUrl'])
            # Nombre del archivo
            print('Nombre del archivo:',f['title'])
            # Tipo de archivo
            print('Tipo de archivo:',f['mimeType'])
            # Esta en el basurero
            print('Esta en el basurero:',f['labels']['trashed'])
            # Fecha de creacion
            print('Fecha de creacion:',f['createdDate'])
            # Fecha de ultima modificacion
            print('Fecha de ultima modificacion:',f['modifiedDate'])
            # Version
            print('Version:',f['version'])
            # Tamanio
            print('Tamanio:',f['fileSize'])
            # CARPETA
            print(f'Title: {f["title"]}, ID: {f["id"]}')
            resultado.append(f)
        
        return resultado

    # DESCARGAR UN ARCHIVO DE DRIVE POR NOMBRE
    def bajar_archivo_por_nombre(self, nombre_archivo, ruta_descarga):
        
        lista_archivos = self.credenciales.ListFile({'q': "title = '" + nombre_archivo + "'"}).GetList()
        if not lista_archivos:
            print('No se encontro el archivo: ' + nombre_archivo)
        archivo = self.credenciales.CreateFile({'id': lista_archivos[0]['id']}) 
        archivo.GetContentFile(ruta_descarga + nombre_archivo)

    # BORRAR/RECUPERAR ARCHIVOS
    def borrar_recuperar(self, id_archivo):
        
        archivo = self.credenciales.CreateFile({'id': id_archivo})
        # MOVER A BASURERO
        # archivo.Trash()
        # SACAR DE BASURERO
        #archivo.UnTrash()
        # ELIMINAR PERMANENTEMENTE
        archivo.Delete()

    # CREAR CARPETA
    def crear_carpeta(self, nombre_carpeta, id_folder):
        
        folder = self.credenciales.CreateFile({'title': nombre_carpeta, 
                                'mimeType': 'application/vnd.google-apps.folder',
                                'parents': [{"kind": "drive#fileLink",\
                                                        "id": id_folder}]})
        folder.Upload()

    # MOVER ARCHIVO
    def mover_archivo(self, id_archivo, id_folder):        
        archivo = self.credenciales.CreateFile({'id': id_archivo})
        propiedades_ocultas = archivo['parents']
        archivo['parents'] = [{'isRoot': False, 
                            'kind': 'drive#parentReference', 
                            'id': id_folder, 
                            'selfLink': 'https://www.googleapis.com/drive/v2/files/' + id_archivo + '/parents/' + id_folder,
                            'parentLink': 'https://www.googleapis.com/drive/v2/files/' + id_folder}]
        archivo.Upload(param={'supportsTeamDrives': True})

    def buscar_archivos_en_folder(self, folder_id):        
        # Construir la consulta para obtener los archivos en la carpeta especificada
        query = f"'{folder_id}' in parents and trashed=false"
        file_list = self.credenciales.ListFile({'q': query}).GetList()        

        # Crear listas separadas para los títulos e IDs de los archivos
        titles = [file['title'] for file in file_list]
        ids = [file['id'] for file in file_list]

        return ids,titles
