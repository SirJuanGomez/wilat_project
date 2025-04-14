import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Parámetros del lanzamiento
v_0 = 50  # Velocidad inicial en m/s
angulo = 75  # Ángulo de lanzamiento en grados
g = 9.81  # Aceleración de la gravedad en m/s^2
t_max = 2 * v_0 * np.sin(np.radians(angulo)) / g  # Tiempo total de vuelo

u = 0
# Frecuencia de muestreo
frecuencia_muestreo = 0.03
t = np.arange(0, t_max, frecuencia_muestreo)

# Trayectoria parabólica con la elevación en Z
x = v_0 * np.cos(np.radians(angulo)) * t
y = np.zeros_like(t)
z = v_0 * np.sin(np.radians(angulo)) * t - 0.5 * g * t**2

# Agregar ruido a las posiciones para simular inestabilidad
x = x + np.random.normal(0, 0.1, len(t))
z = z + np.random.normal(0, 0.1, len(t))
u = u + np.random.normal(0,2, len(t))


# Vectores de dirección (derivadas numéricas de las posiciones)
u = np.gradient(x)
v = np.gradient(y)  # Esto será 0, pero se incluye por consistencia
w = np.gradient(z)

# Escalar los vectores para ajustar el tamaño visual de los conos
escalador = 0.5  # Ajusta este valor para agrandar o reducir conos
u_escalado = u * escalador
v_escalado = v * escalador
w_escalado = w * escalador

# Guardar los datos generados en un archivo JSON
datos = []
for i in range(len(t)):
    datos.append({
        "aceleracion": [x[i], y[i], z[i]],
        "gyroscopio": [u[i], v[i], w[i]]
    })

# Ruta del archivo
ruta_archivo = r'3D_ploter_code\prueba_de_code\data_probe\trayectoria_json.json'
with open(ruta_archivo, 'w') as file:
    json.dump(datos, file, indent=4)

# Visualización con Plotly

# Trayectoria 3D (puntos)
trayectoria = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=z,
        colorscale='Viridis',
        opacity=0.8
    ),
    name='Trayectoria'
)

# Vectores de dirección (conos)
vectores = go.Cone(
    x=x,
    y=y,
    z=z,
    u=u_escalado,
    v=v_escalado,
    w=w_escalado,
    sizemode="scaled",
    sizeref=2,
    anchor="tail",
    colorscale='Plasma',
    showscale=False,
    name='Dirección (simulada)'
)

# Crear subgráficos
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Trayectoria sin conos", "Trayectoria con conos"),
    specs=[[{"type": "scatter3d"}, {"type": "scatter3d"}]]
)

# Gráfico sin conos
fig.add_trace(trayectoria, row=1, col=1)

# Gráfico con conos
fig.add_trace(trayectoria, row=1, col=2)
fig.add_trace(vectores, row=1, col=2)

# Layout
fig.update_layout(
    title="📈 Trayectoria parabólica con y sin conos (frecuencia de muestreo 0.3s)",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z (Elevación)"
    ),
    margin=dict(l=0, r=0, b=0, t=50)
)

# Mostrar gráfico
fig.show()
