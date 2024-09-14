import io
import pandas as pd
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

class XLSReader:    
    
    def clasificar_categoria(self,Descripcion):        
        # Diccionario de categorías y necesidades
        categorias_necesidades = {
            'METRO': ('SUPERMERCADO', 'BASICA'),
            'TOTTUS': ('SUPERMERCADO', 'BASICA'),
            'PROMART': ('SUPERMERCADO', 'BASICA'), 
            'MAKRO HUAYLAS': ('SUPERMERCADO', 'BASICA'),        
            'MARKET': ('SUPERMERCADO', 'BASICA'),        
            'SODIMAC': ('SHOPING', 'BASICA'),
            'PLAZA VEA': ('SUPERMERCADO', 'BASICA'),        
            'VENDOMATICA': ('SUPERMERCADO', 'BASICA'),        
            'VETMUNDO': ('VETERINARIA', 'BASICA'),
            'BASTARDOS': ('PERSONAL', 'BASICA'),  
            'MEDIC': ('SALUD', 'BASICA'),                
            'IZI*MISHA RASTRERA': ('SALUD', 'BASICA'),                
            'IZI*TIERRA MIA': ('SALUD', 'BASICA'),                
            'MARATI': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'BOCANADA': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'JUICY LUCY': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'ENCANTADA DE VILLA': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'HELADERIA ITALIANA 4D': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'LISTO SANNA': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'CINEMARK': ('CINE', 'ENTRETENIMIENTO'), 
            'LISTO SARAPAMPA': ('AUTOSERVICIO', 'AUTO'),               
            'RUTAS DE HUAYLAS': ('PEAJES', 'AUTO'),
            'PEAJE': ('PEAJES', 'AUTO'),        
            'PEAJE JAHUAY': ('PEAJES', 'AUTO'),   
            'RUTAS': ('PEAJES', 'AUTO'),
            'RUTAS DE LIMA SAC': ('PEAJES', 'AUTO'),                
            'SPORTWAGEN': ('SERVICIO AUTO', 'AUTO'),
            'AGROPLAZA': ('FERTILIZANTES', 'PALTA'),        
            'PECSA': ('COMBUSTIBLE', 'AUTO'),
            'GASEOCENTRO ELIZABETH': ('COMBUSTIBLE', 'AUTO'),
            'GRIFO': ('COMBUSTIBLE', 'AUTO'),
            'ESTACION DE SERV HERC': ('COMBUSTIBLE', 'AUTO'),        
            'KIO': ('COMBUSTIBLE', 'AUTO'),  
            'COMBUSTIBLES': ('COMBUSTIBLE', 'AUTO'),  
            'ADM TRIBUTARIA': ('IMPUESTOS', 'AUTO'),              
            'INKA CHICKEN': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'CHIFA': ('RESTAURANTE', 'ENTRETENIMIENTO'),    
            'RUSTICA': ('RESTAURANTE', 'ENTRETENIMIENTO'),             
            'LA LUCHA': ('RESTAURANTE', 'ENTRETENIMIENTO'),  
            'LA PATRON': ('RESTAURANTE', 'ENTRETENIMIENTO'),              
            'MUTTI': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'LA FONTANA': ('RESTAURANTE', 'ENTRETENIMIENTO'),        
            'WIN': ('SERVICIO INTERNET', 'SERVICIOS'),        
            'GOOGLE YOUTUBE': ('SERVICIO INTERNET', 'SERVICIOS'),
            'SEDAPAL': ('SERVICIO AGUA', 'SERVICIOS'),        
            'LUZ DEL SUR': ('SERVICIO LUZ', 'SERVICIOS'),
            'CLARO': ('SERVICIO MOVIL', 'SERVICIOS'),        
            'MAPFRE': ('SERVICIO SEGURO', 'SERVICIOS'),
            'DATACAMP': ('EDUCACION', 'SERVICIOS'),
            'CHUN KOC': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'PAZ APART HOTEL': ('RESTAURANTE', 'ENTRETENIMIENTO'),        
            'INKAS CHICKEN': ('RESTAURANTE', 'ENTRETENIMIENTO'),
            'TORTAS DE LA CASA': ('PASTELERIA', 'SOCIAL')        
        }   
        
        # Convertir la descripción a mayúsculas
        descripcion_upper = Descripcion.upper()
        
        # Buscar la descripción en el diccionario
        for key in categorias_necesidades:
            if key in descripcion_upper:
                return categorias_necesidades[key]        
        
        # Retornar valores por defecto si no se encuentra la descripción
        return ('DESCONOCIDO', 'BASICA')
    
    def identificar_moneda(self,monto):
        # Función para identificar la moneda
        if monto.startswith('US$'):
            return 'DOLARES'
        else:
            return 'SOLES'
    
    def convertir_a_soles(self,monto, moneda):
        # Función para convertir el monto a soles
        # Tipo de cambio (soles a dólares)
        tipo_de_cambio = 3.70  # Ejemplo: 1 dólar = 3.50 soles

        if moneda == 'DOLARES':
            return float(monto.split()[1]) * tipo_de_cambio
        else:
            return float(monto.split()[1])
    
    def etl_info(self,file_id):

        # ID del archivo EXCEL en Google Drive
        #file_id = '1x-CmYRD4N2rNUSnckYyqIzAWj8-ux1Mz'
        url = f'https://drive.google.com/uc?id={file_id}'
        

        # Realizar una solicitud GET para obtener el archivo
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            logging.info(f"Error al descargar el archivo: {e}")
            return None    
            

        # Leer el archivo Excel desde el contenido de la respuesta
        excel_file = io.BytesIO(response.content)
        
        df = pd.read_excel(excel_file,skiprows=5)        
        df = df[['FECHA', 'DESCRIPCIÓN','MONTO']]
        df_cleaned = df.dropna()

        #LIMPIEZA#       

        df_cleaned = df_cleaned[~df_cleaned['DESCRIPCIÓN'].isin([
            '*** PAGO AUTOMATICO ***',
            '* SEGURO DE DESGRAVAMEN',
            'BM. PAGO TARJETA DE CRED.'
            ])]

        # Obtener la fecha actual
        fecha_actual = datetime.now()        
        
        dia_actual = fecha_actual.day

        # Calcular el mes anterior
        if dia_actual >= 10:
            mes_anterior = fecha_actual 
        else:
            mes_anterior = fecha_actual - relativedelta(months=1)
    
        # Formatear el resultado
        mes_anterior_formateado = mes_anterior.strftime('%m/%Y')
        fecha_filtro = '10/'+mes_anterior_formateado
        
        logging.info(f"Fecha inicio Mes : {fecha_filtro}")

        #Convertir la columna 'FECHA' a formato datetime
        df_cleaned['FECHA'] = pd.to_datetime(df_cleaned['FECHA'], format='%d/%m/%Y')

        # Filtrar por fecha mayor a una fecha en particular

        fecha_filtro = pd.to_datetime(fecha_filtro, format='%d/%m/%Y')

        df_filtrado = df_cleaned[df_cleaned['FECHA'] > fecha_filtro]

        df_filtrado[['CATEGORIA','NECESIDAD']] = df_filtrado['DESCRIPCIÓN'].str.upper().apply(self.clasificar_categoria).apply(pd.Series)

        # Crear el campo "MONEDA"
        df_filtrado['MONEDA'] = df_filtrado['MONTO'].apply(self.identificar_moneda)

        # Crear el campo "MontoSoles"
        df_filtrado['MTO_SOL'] = df_filtrado.apply(lambda row: self.convertir_a_soles(row['MONTO'], row['MONEDA']), axis=1)

        return df_filtrado