import random
import json

def generar_datos():
    # Inicializar las variables
    z = 0
    datos = []
    ruido_max = 0.5  # Máximo valor de ruido para las coordenadas x, y y z
    pasos_subida = 50  # Subimos hasta z = 50m
    pasos_descenso = 50  # Luego descendemos hasta z = 0m
    base_ruido = 0.2  # Ruido base que se sumará a las coordenadas x, y y z

    # Generar datos para la subida (z = 0 a 50)
    for i in range(pasos_subida):
        # Generar coordenadas x y y con ruido integrado
        x_base = i * 0.1  # Valor base para x
        y_base = i * 0.1  # Valor base para y
        z_base = z + random.uniform(0, 1)  # Valor base para z

        # Integrar el ruido directamente en las mediciones
        x = x_base + random.uniform(-ruido_max, ruido_max)
        y = y_base + random.uniform(-ruido_max, ruido_max)
        z = min(50, z_base + random.uniform(-base_ruido, base_ruido))  # Aumentar z hasta 50 con ruido

        # Añadir el dato con ruido
        datos.append({
            "x": round(x, 2),
            "y": round(y, 2),
            "z": round(z, 2)
        })

    # Generar datos para el descenso (z = 50 a 0)
    for i in range(pasos_descenso):
        x_base = (pasos_subida + i) * 0.1  # Movimiento progresivo de x
        y_base = (pasos_subida + i) * 0.1  # Movimiento progresivo de y
        z_base = z - random.uniform(0, 1)  # Valor base para z

        # Integrar el ruido directamente en las mediciones
        x = x_base + random.uniform(-ruido_max, ruido_max)
        y = y_base + random.uniform(-ruido_max, ruido_max)
        z = max(0, z_base + random.uniform(-base_ruido, base_ruido))  # Disminuir z hasta 0 con ruido

        # Añadir el dato con ruido
        datos.append({
            "x": round(x, 2),
            "y": round(y, 2),
            "z": round(z, 2)
        })

    return datos

# Generar los datos
datos = generar_datos()

# Guardar los datos en un archivo JSON
with open("datos_simulados.json", "w") as file:
    json.dump(datos, file, indent=4)

print("Datos simulados guardados en 'datos_simulados.json'")
