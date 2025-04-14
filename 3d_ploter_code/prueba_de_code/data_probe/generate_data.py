import numpy as np
import pandas as pd
import plotly.graph_objs as go
import os

# Configuración de simulación
fs = 1000  # Hz
dt = 1 / fs
t = np.arange(0, 10, dt)  # 12 segundos

# Parámetros físicos
g = -9.81  # m/s² (gravedad)
v0 = 50    # m/s (velocidad inicial hacia arriba)

# Aceleración: constante en Z (gravedad), más ruido en todos los ejes
noise_std = 0.05  # nivel de ruido

ax = np.random.normal(0, noise_std, len(t))  # sin movimiento real en X
ay = np.random.normal(0, noise_std, len(t))  # sin movimiento real en Y
az = g * np.ones_like(t) + np.random.normal(0, noise_std, len(t))  # gravedad con ruido

# Integración a velocidad (suponemos velocidad inicial solo en Z)
vx = np.cumsum(ax) * dt
vy = np.cumsum(ay) * dt
vz = np.cumsum(az) * dt + v0  # incluye velocidad inicial en Z

# Integración a posición
x = np.cumsum(vx) * dt
y = np.cumsum(vy) * dt
z = np.cumsum(vz) * dt

# Guardar datos simulados
df = pd.DataFrame({'t': t, 'x': x, 'y': y, 'z': z})

# Ruta del archivo
file_path = r'3D_ploter_code\prueba_de_code\data_probe\trayectoria.json'

# Verificar si el archivo existe y limpiarlo antes de escribir los nuevos datos
if os.path.exists(file_path):
    print("El archivo existe, limpiando datos antiguos...")

# Escribir los nuevos datos en el archivo JSON
df.to_json(file_path, index=False)

print(f"Datos guardados correctamente en {file_path}")
