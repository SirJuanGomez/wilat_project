import json
import plotly.graph_objects as go

# Leer los datos desde el archivo JSON
with open('datos_simulados.json', 'r') as file:
    datos = json.load(file)

# Extraer las coordenadas x, y y z
x = [d['x'] for d in datos]
y = [d['y'] for d in datos]
z = [d['z'] for d in datos]

# Crear la gráfica 3D interactiva
fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=z,  # Usar z para el color de los puntos
        colorscale='Viridis',  # Escala de colores
        opacity=0.8
    )
)])

# Configurar el layout de la gráfica
fig.update_layout(
    title='Datos Simulados en 3D',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    margin=dict(l=0, r=0, b=0, t=40)  # Márgenes para mejor visualización
)

# Mostrar la gráfica
fig.show()
