import json
import random

# Función para generar valores aleatorios con algo de ruido
def generar_dato(valor_base, ruido_max):
    return valor_base + random.uniform(-ruido_max, ruido_max)

# Función para generar los datos del lanzamiento
def simular_lanzamiento(num_datos):
    datos_lanzamiento = []

    for _ in range(num_datos):
        # Generar aceleración y giroscopio con ruido
        aceleracion = [round(generar_dato(9.8, 1.0), 2) for _ in range(3)]  # Aceleración aproximada de gravedad con ruido
        gyroscopio = [round(generar_dato(0, 1.0), 2) for _ in range(3)]  # Giroscopio con ruido

        # Crear un diccionario para cada conjunto de datos
        datos_lanzamiento.append({
            "aceleracion": aceleracion,
            "gyroscopio": gyroscopio
        })

    return datos_lanzamiento

# Generar 100 lecturas de datos (simulando un lanzamiento)
num_datos = 100
datos = simular_lanzamiento(num_datos)

# Guardar los datos en un archivo JSON
with open(r'3D_ploter_code\prueba_de_code\data_probe\trayectoria.json', 'w') as file:
    json.dump(datos, file, indent=4)

print(f"Archivo JSON con {num_datos} datos aleatorios generado exitosamente.")
