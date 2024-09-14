import logging
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
import os



class DashboardGenerator:
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

    def main_dash(self,data):
        df_filtrado = data
        suma_acumulada_dolares = 0
        for index, row in df_filtrado.iterrows():
            if row['MONEDA'] == 'DOLARES':
                suma_acumulada_dolares += row['MTO_SOL']

        # Redondear la suma acumulada a 2 decimales
        suma_acumulada_dolares_redondeada = round(suma_acumulada_dolares, 2)       

        # Calcular la suma acumulada en SOLES
        suma_acumulada_soles = 0
        for index, row in df_filtrado.iterrows():
            if row['MONEDA'] == 'SOLES':
                suma_acumulada_soles += row['MTO_SOL']

        # Redondear la suma acumulada a 2 decimales
        suma_acumulada_sol_redondeada = round(suma_acumulada_soles, 2)        
        suma_Total_sol = round((suma_acumulada_soles+suma_acumulada_dolares_redondeada), 2)
        

        ###GRAFICO
        # Crear la figura
        fig = go.Figure()

        # Primer indicador (arriba a la izquierda)
        fig.add_trace(go.Indicator(
            mode = "number",
            value = suma_acumulada_dolares_redondeada,    
            number = {'prefix': "$"},
            delta = {'position': "top", 'reference': 320},
            domain = {'x': [0, 0.5], 'y': [0.5, 1]},  # Mitad superior izquierda
            title = {'text': "En Dólares"}
        ))

        # Segundo indicador (arriba a la derecha)
        fig.add_trace(go.Indicator(
            mode = "number",
            value = suma_acumulada_sol_redondeada,    
            number = {'prefix': "S/. "},
            delta = {'position': "top", 'reference': 250},
            domain = {'x': [0.5, 1], 'y': [0.5, 1]},  # Mitad superior derecha
            title = {'text': "En Soles"}
        ))

        # Tercer indicador (debajo de los dos anteriores)
        fig.add_trace(go.Indicator(
            mode = "number",
            value = suma_Total_sol,    
            number = {'prefix': "S/. "},
            delta = {'position': "top", 'reference': 450},
            domain = {'x': [0, 1], 'y': [0, 0.5]},  # Parte inferior
            title = {'text': "Total en Soles"}
        ))

        # Configurar fondo
        fig.update_layout(paper_bgcolor = "lightgray")

        # Mostrar la gráfica
        #fig.show()

        # Guardar el gráfico como una imagen
        # Definir la ruta relativa de la carpeta 'img' y el nombre del archivo
        image_path = os.path.join(self.current_dir, 'img', 'main_dash.png')        
        fig.write_image(image_path)
        logging.info("Imagen main_dash.png creada")
    
    def budget_dash(self, data):
        df_filtrado = data

        # Convertir el campo MONTO a numérico        
        gasto_total_por_categoria = df_filtrado.groupby('CATEGORIA')['MTO_SOL'].sum().reset_index()
        
        filtro_co = gasto_total_por_categoria[gasto_total_por_categoria['CATEGORIA'] == 'COMBUSTIBLE']
        if not filtro_co.empty:
            monto_combustible = filtro_co['MTO_SOL'].values[0]
        else:
            monto_combustible = 0        

        filtro_pe = gasto_total_por_categoria[gasto_total_por_categoria['CATEGORIA'] == 'PEAJES']

        if not filtro_pe.empty:
            monto_peajes = filtro_pe['MTO_SOL'].values[0]
        else:
            monto_peajes = 0

        filtro_su = gasto_total_por_categoria[gasto_total_por_categoria['CATEGORIA'] == 'SUPERMERCADO']

        if not filtro_su.empty:
            monto_super = filtro_su['MTO_SOL'].values[0]
        else:
            monto_super = 0

        filtro_re = gasto_total_por_categoria[gasto_total_por_categoria['CATEGORIA'] == 'RESTAURANTE']

        if not filtro_re.empty:
            monto_resto = filtro_re['MTO_SOL'].values[0]
        else:
            monto_resto = 0

        fig_2 = go.Figure()
        # Indicador para PEAJES
        fig_2.add_trace(go.Indicator(
            mode = "number+delta",
            value = monto_peajes,
            delta = {
                'reference': 150,
                'relative': False,
                'increasing': {'color': 'red'},  
                'decreasing': {'color': 'green'},
                'valueformat': '0'
            },
            title = {'text': "Peajes(150)"},
            domain = {'x': [0, 0.5], 'y': [0.7, 1]},
        ))

        # Indicador para Super
        fig_2.add_trace(go.Indicator(
            mode = "number+delta",
            value = monto_super,
            delta = {
                'reference': 350,
                'relative': False,
                'increasing': {'color': 'red'},  
                'decreasing': {'color': 'green'},
                'valueformat': '0'
            },
            title = {'text': "Super(350)"},
            domain = {'x': [0.5, 1], 'y': [0.7, 1]},
        ))

        # Indicador para Restaurante
        fig_2.add_trace(go.Indicator(
            mode = "number+delta",
            value = monto_resto,
            delta = {
                'reference': 250,
                'relative': False,
                'increasing': {'color': 'red'},  
                'decreasing': {'color': 'green'},
                'valueformat': '0'
            },
            title = {'text': "Restaurante(250)"},
            domain = {'x': [0, 0.5], 'y': [0, 0.5]},
        ))

        # Indicador para Combustible
        fig_2.add_trace(go.Indicator(
            mode = "number+delta",
            value = monto_combustible,
            delta = {
                'reference': 300,
                'relative': False,
                'increasing': {'color': 'red'},  
                'decreasing': {'color': 'green'},
                'valueformat': '0'
            },
            title = {'text': "Combustible(300)"},
            domain = {'x': [0.5, 1], 'y': [0, 0.5]},
        ))

        # Definir el layout en formato de cuadrícula de 2 filas y 2 columnas
        fig_2.update_layout(
            grid={'rows': 2, 'columns': 2, 'pattern': "independent"},
            paper_bgcolor="lightblue"
        )        
        # Crear la figura
        # Guardar el gráfico como una imagen        
        image_path_2 = os.path.join(self.current_dir, 'img', 'budget_dash.png')

        fig_2.write_image(image_path_2)
        logging.info("Imagen budget_dash.png creada")

    def categoria_bar_dash(self, data):
        df_filtrado = data
        gasto_total_por_categoria = df_filtrado.groupby('CATEGORIA')['MTO_SOL'].sum().reset_index()
        # Crear el gráfico de barras
        fig_3 = go.Figure(data=[go.Bar(
            x=gasto_total_por_categoria['CATEGORIA'],
            y=gasto_total_por_categoria['MTO_SOL'],
            text=gasto_total_por_categoria['MTO_SOL'].apply(lambda x: f"{int(x):,}"),  # Texto con formato de moneda
            marker_color='lightskyblue'  # Color de las barras
        )])

        # Personalizar el diseño del gráfico
        fig_3.update_layout(
            title='Gasto total por categoría',
            xaxis_title='Categoría',
            #yaxis_title='Gasto total',
            #yaxis=dict(title='Gasto total', tickformat='$,.2f'),  # Formato del eje Y como moneda
            yaxis=dict(tickformat='$,.2f'),  # Formato del eje Y como moneda
            bargap=0.2  # Espacio entre las barras
        )

        # Mostrar el gráfico        
        image_path_3 = os.path.join(self.current_dir, 'img', 'categoria_bar_dash.png')
        
        fig_3.write_image(image_path_3)
        logging.info("Imagen categoria_bar_dash.png creada")
        