from machine import Pin, SoftSPI
import utime
from nrf24l01 import NRF24L01

# Configuración SPI
spi = SoftSPI(sck=Pin(25), mosi=Pin(33), miso=Pin(32))
csn = Pin(26, Pin.OUT)
ce = Pin(27, Pin.OUT)
nrf = NRF24L01(spi, csn, ce, payload_size=32)

# Direcciones
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
nrf.open_tx_pipe(pipes[0])
nrf.open_rx_pipe(1, pipes[1])
nrf.start_listening()

print("Emisor listo para enviar mensajes.")

while True:
    msg = input("Escribe un mensaje: ")[:32]  # Limita a 32 bytes
    nrf.stop_listening()
    nrf.send(msg.encode("utf-8"))
    print("Mensaje enviado:", msg)

    # Esperar respuesta
    nrf.start_listening()
    start = utime.ticks_ms()
    while not nrf.any():
        if utime.ticks_diff(utime.ticks_ms(), start) > 2000:
            print("Sin respuesta del receptor.")
            break

    if nrf.any():
        respuesta = nrf.recv().decode("utf-8").strip()
        print("Respuesta del receptor:", respuesta)

    print("-----\n")
    utime.sleep(0.5)

