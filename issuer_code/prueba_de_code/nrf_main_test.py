import machine as mch
import time
import json
from nrf24l01 import NRF24L01

# Función para configurar el SPI (ya preconfigurado en el módulo)
def init_spi():
    spi = mch.SPI(1, baudrate=5000000, polarity=0, phase=0)
    return spi

# Función para inicializar el radio (NRF24L01)
def initialize_radio():
    try:
        # Configurar los pines CSN y CE
        csn_pin = mch.Pin(5, mch.Pin.OUT)
        ce_pin = mch.Pin(4, mch.Pin.OUT)
        spi = init_spi()

        # Crear una instancia del NRF24L01
        radio = NRF24L01(spi, csn_pin, ce_pin)

        # Configuración de canal y dirección de transmisión
        radio.set_channel(30)  # Cambiar al canal 30 (2.430 GHz)
        radio.set_power_speed(radio.POWER_3, radio.SPEED_250K)  # Máxima potencia y velocidad baja
        radio.open_tx_pipe(b'\x01\x02\x03\x04\x05')  # Dirección de la tubería de transmisión
        return radio
    except Exception as e:
        print("Error al inicializar el radio:", e)
        return None

# Función para enviar paquetes de datos
def send_data_in_packets(radio, data):
    try:
        # Convertir los datos a un formato JSON
        json_data = json.dumps(data)
        data_length = len(json_data)
        
        # Dividir el dato JSON en paquetes de tamaño máximo de 32 bytes
        packet_size = 32
        num_packets = (data_length + packet_size - 1) // packet_size  # Dividir en el número de paquetes necesarios
        
        print(f"Enviando {num_packets} paquetes...")

        # Enviar los paquetes
        for i in range(num_packets):
            start = i * packet_size
            end = min((i + 1) * packet_size, data_length)
            packet = json_data[start:end]
            print(f"Enviando paquete {i + 1}/{num_packets}: {packet}")
            radio.send(packet.encode())  # Enviar el paquete
            
            # Esperar hasta que la transmisión sea confirmada
            start_time = time.time()
            while time.time() - start_time < 2:  # Esperar hasta 2 segundos para confirmar
                if radio.send_done() == 1:  # Transmisión exitosa
                    print(f"Paquete {i + 1}/{num_packets} enviado exitosamente.")
                    break
                elif radio.send_done() == 2:  # Error en la transmisión
                    print(f"Error al enviar el paquete {i + 1}/{num_packets}.")
                    break
            else:
                print(f"Tiempo agotado para el paquete {i + 1}/{num_packets}. Reintentando...")
                radio.flush_tx()  # Limpiar el buffer de TX en caso de fallo

            time.sleep(0.1)  # Retardo entre paquetes
    except Exception as e:
        print("Error al enviar los datos:", e)

# Función principal de transmisión
def main():
    print("Iniciando el emisor NRF24L01...")
    radio = initialize_radio()

    if radio:
        print("Emisor listo para enviar datos.")
        while True:
            # Ejemplo de datos que se van a enviar
            data = {
                "aceleracion": [1.0, 2.5, -0.5],
                "gyroscopio": [0.03, 0.1, -0.02],
                "magnetometro": [15.0, -8.5, 12.3],
                "temperatura": 25.5,
                "presion": 101325,
                "altitud": 150,
                "radiacion_uv": 3.2,
                "gps": {"latitud": 19.432608, "longitud": -99.133209}
            }
            
            # Enviar los datos en paquetes
            send_data_in_packets(radio, data)
            
            # Esperar antes de enviar otro conjunto de datos
            time.sleep(1)
    else:
        print("No se pudo inicializar el emisor.")

# Iniciar la transmisión
if __name__ == "__main__":
    main()
