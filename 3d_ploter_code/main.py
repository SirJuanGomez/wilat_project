import serial
import json
import time
import datetime
import plotly.graph_objects as go

# Configura el puerto serial (ajusta 'COM3' a tu puerto correcto)
serial_port = serial.Serial('COM3', 115200)
guardar_datos = False  # Variable para controlar si se deben guardar los datos
datos_recibidos = []  # Lista para almacenar los datos de los sensores

# Nombre del archivo JSON donde se guardarán los datos
archivo_json = 'datos_sensor.json'

try:
    while True:
        line = serial_port.readline().decode('utf-8').strip()  # Leer la línea del puerto serial
        if line:
            if line == "graficar":  # Comando para graficar
                print("Comando de graficar recibido. Generando gráfico...")
                
                # Graficar los datos almacenados
                ac_x = [dato['aceleracion'][0] for dato in datos_recibidos]
                ac_y = [dato['aceleracion'][1] for dato in datos_recibidos]
                ac_z = [dato['aceleracion'][2] for dato in datos_recibidos]
                
                g_x = [dato['gyroscopio'][0] for dato in datos_recibidos]
                g_y = [dato['gyroscopio'][1] for dato in datos_recibidos]
                g_z = [dato['gyroscopio'][2] for dato in datos_recibidos]
                
                # Crear el gráfico 3D
                trayectoria = go.Scatter3d(
                    x=ac_x, y=ac_y, z=ac_z, 
                    mode='lines+markers',
                    marker=dict(size=2.5, color='red'),
                    line=dict(color='green', width=2),
                    name='Trayectoria'
                )

                vectores = go.Cone(
                    x=ac_x, y=ac_y, z=ac_z,
                    u=g_x, v=g_y, w=g_z,
                    sizemode="scaled",
                    sizeref=0.5,
                    anchor="tail",
                    colorscale='Inferno',
                    showscale=False,
                    name='Orientación (giro)'
                )

                final_fig = go.Figure(data=[trayectoria, vectores])

                final_fig.update_layout(
                    title="Trayectoria 3D con orientación de giroscopio",
                    scene=dict(
                        xaxis_title="X",
                        yaxis_title="Y",
                        zaxis_title="Z"
                    ),
                    margin=dict(l=0, r=0, b=0, t=40)
                )

                final_fig.show()

            else:
                try:
                    # Convertir la línea recibida en un objeto JSON
                    data = json.loads(line)
                    
                    # Obtener la marca de tiempo actual
                    timestamp = datetime.datetime.now().isoformat()

                    # Agregar el timestamp a los datos
                    data_con_timestamp = {
                        "timestamp": timestamp,
                        "datos": data
                    }

                    if guardar_datos:
                        # Guardar los datos en la lista con el tiempo correspondiente
                        datos_recibidos.append(data_con_timestamp)

                    # Guardar los datos en el archivo JSON
                    with open(archivo_json, 'a') as archivo:
                        json.dump(data_con_timestamp, archivo)
                        archivo.write('\n')

                    print(f"Datos recibidos y guardados: {data_con_timestamp}")
                
                except json.JSONDecodeError:
                    print(f"Error al decodificar los datos JSON.")

        else:
            print("No se recibieron datos.")
except KeyboardInterrupt:
    print("Programa Finalizado...")
finally:
    serial_port.close()
