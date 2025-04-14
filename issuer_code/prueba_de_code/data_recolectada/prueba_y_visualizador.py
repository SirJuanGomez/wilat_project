import json

# Leer los datos desde el archivo JSON
with open('datos_simulados.json', 'r') as file:
    datos = json.load(file)

# Estado inicial
z_maximo = datos[0]['z']
paracaidas_abierto = False

for i in range(1, len(datos)):
    z_anterior = datos[i - 1]['z']
    z_actual = datos[i]['z']

    # Actualizar el máximo si estamos subiendo
    if z_actual > z_maximo:
        z_maximo = z_actual

    # Detectar inicio de descenso justo después del máximo
    if not paracaidas_abierto and z_anterior == z_maximo and z_actual < z_anterior:
        print(f"Valor de z disminuyó: {z_actual}")
        print("Paracaídas abierto")
        paracaidas_abierto = True

    # Mostrar cuando z disminuye (como monitoreo)
    elif z_actual < z_anterior:
        print(f"Valor de z disminuyó: {z_actual}")
