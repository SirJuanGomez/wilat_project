import machine as mch
import time
import nrf24l01  # Asumiendo que este es el archivo con la clase NRF24L01

# Configuración de SPI
spi = mch.SPI(1, baudrate=5000000, polarity=0, phase=0)
csn_pin = mch.Pin(5, mch.Pin.OUT)
ce_pin = mch.Pin(4, mch.Pin.OUT)

# Inicialización de la radio
try:
    radio = nrf24l01.NRF24L01(spi, csn_pin, ce_pin)
    radio.set_channel(50)  # Puedes ajustar el canal a tu necesidad
    radio.open_tx_pipe(b'\x01\x02\x03\x04\x05')  # Dirección del receptor
except Exception as e:
    print(f"No se pudo iniciar porque: {e}")

# Función para enviar datos
def send_data(radio, data):
    try:
        # Enviar datos de manera no bloqueante
        radio.send(data)
        print(f"Datos enviados: {data}")
        bytes_sent = len(data)
        print(f"Cantidad de bytes enviados: {bytes_sent}")

        # Esperar la confirmación de transmisión
        start_time = time.time()
        result = None

        # Espera hasta que la transmisión se complete o se agote el tiempo
        while result is None and time.time() - start_time < 2:
            result = radio.send_done()  # Verifica el estado de la transmisión

        if result is None:
            # Si se agotó el tiempo sin confirmación
            print("Tiempo agotado, la transmisión no se completó.")
            radio.flush_tx()
            radio.reg_write(nrf24l01.CONFIG, radio.reg_read(nrf24l01.CONFIG) & ~nrf24l01.PWR_UP)
        elif result == 1:
            print("Transmisión exitosa.")
        elif result == 2:
            print("Error en la transmisión.")

    except Exception as e:
        print(f"Error al enviar los datos: {e}")

# Datos a enviar
data_sending = "Hola, este es un mensaje de prueba"
data_bytes = data_sending.encode('utf-8')  # Asegúrate de que sea 'utf-8'

# Calcular tamaño de los datos
data_bytes_size = len(data_bytes)
print(f"Bytes calculados: {data_bytes_size}")

# Enviar los datos
send_data(radio, data_sending)

# Esperar antes de continuar
time.sleep(2)
