import json

def process_data(data):
    # Variable para determinar si el paracaídas debe abrirse
    parachute_opened = False
    # Guardamos el valor anterior de la aceleración Z para detectar el descenso
    previous_z = None

    for entry in data:
        x = entry['x']
        y = entry['y']
        z = entry['z']

        # Imprime los valores de la aceleración
        print(f"x: {x}, y: {y}, z: {z}")
        
        # Si ya tenemos un valor previo de Z, comparamos para detectar el descenso
        if previous_z is not None:
            if z < previous_z and not parachute_opened:
                # Si Z es menor que el valor previo, significa que está descendiendo
                print("¡El objeto está descendiendo! Paracaídas abierto.")
                parachute_opened = True  # Marcamos que el paracaídas ya se ha abierto
        # Guardamos el valor de Z para la próxima comparación
        previous_z = z

def main():
    # Cargar el JSON desde un archivo (ajusta la ruta si es necesario)
    with open('datos_simulados.json', 'r') as file:
        data = json.load(file)

    process_data(data)

if __name__ == "__main__":
    main()
