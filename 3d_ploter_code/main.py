import serial 
import json 
import plotly.graph_objects as go

serial_port = serial.Serial('COM3',115200)
archivo = open(r'3D_ploter_code\datos_sensor.json','a')

try:
    while True:
        line = serial_port.readline().decode('uft-8').strip()
        if line:
            try:
                data = json.loads(line)
                json.dump(data,archivo)
                archivo.write('\n')
                print(f"Datos Guardados.")
            except json.JSONDecodeError:
                print(f"Error al decodificar")
except KeyboardInterrupt:
    print(f"Programa Finalizado...")

finally:
    archivo.close()
    serial_port.close()

with open(r'3D_ploter_code\datos_sensor.json', 'r') as file :
    data_read = [json.loads(line) for line in file]

ac_x = [date['aceleracion'][0] for date in data_read]
ac_y = [date['aceleracion'][1] for date in data_read]
ac_z = [date['aceleracion'][2] for date in data_read]

g_x = [date['gyroscopio'][0] for date in data_read]
g_y = [date['gyroscopio'][1] for date in data_read]
g_z = [date['gyroscopio'][2] for date in data_read]

trayectoria = go.Scatter3d(
    x=ac_x,
    y=ac_y,
    z=ac_z
    mode='lines+markers',
    marker=dict(size=2.5, color='red'),
    line= dict(color= 'green', width=2),
    name='Trayectoria' 
    )

vectores = go.Cone(
    x=ac_x,
    y=ac_y,
    z=ac_z,
    u=g_x,
    v=g_y,
    w=g_z,
    sizemode="scaled",
    sizeref=0.5,
    anchor="tail",
    colorscale='Inferno',
    showscale=False,
    name='Orientación (giro)'
)

final_fig = go.Figure(data=[trayectoria,vectores])

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

