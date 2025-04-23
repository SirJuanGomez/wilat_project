from gps_module import NE06M  # Importa la clase desde el archivo donde la definiste
import time

# Crear una instancia de la clase NE06M con valores personalizados
gps = NE06M(uart_num=1, baudrate=9600, tx_pin=17, rx_pin=16)  # Parámetros personalizados

# O bien, usar la configuración por defecto:
# gps = NE06M()  # Usará los valores por defecto

# Bucle principal para actualizar y obtener la información
while True:
    gps.update()  # Actualiza la información del GPS
    print(f"Latitud: {gps.latitude}")
    print(f"Longitud: {gps.longitude}")
    print(f"Altitud: {gps.altitude}")
    print(f"Satelites visibles: {gps.satellites}")
    print(f"Hora: {gps.time}")
    print(f"Hemisferio: {gps.hemisphere}")
    time.sleep(1)  # Espera 1 segundo antes de actualizar nuevamente
