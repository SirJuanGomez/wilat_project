import math
from machine import Pin, SoftSPI
import utime
from nrf24l01 import NRF24L01

# --- Configuración del NRF24 ---
def configurar_nrf():
    spi = SoftSPI(sck=Pin(25), mosi=Pin(33), miso=Pin(32))
    csn = Pin(26, Pin.OUT)
    ce = Pin(27, Pin.OUT)
    nrf = NRF24L01(spi, csn, ce, payload_size=32)

    tx_pipe = b"\xe1\xf0\xf0\xf0\xf0"  # Dirección TX
    rx_pipe = b"\xd2\xf0\xf0\xf0\xf0"  # Dirección RX
    nrf.open_tx_pipe(tx_pipe)
    nrf.open_rx_pipe(1, rx_pipe)c

    return nrf

# --- Generación de datos con función seno (subir y bajar) ---
def generar_parabola(x, A=5, k=math.pi/10, B=5):
    # Usamos la función seno para hacer que Y suba y baje entre 0 y 10
    # La fórmula será: y = A * sin(k * x) + B
    # A es la amplitud (cuánto sube o baja), B es el desplazamiento (la media).
    y = A * math.sin(k * x) + B
    return y

# --- Enviar datos con control de tamaño ---
def enviar_mensaje(nrf, mensaje, retries=3, delay=0.5):
    nrf.stop_listening()
    for _ in range(retries):
        if len(mensaje) <= 32:  # Verificar si el mensaje es de tamaño adecuado
            try:
                nrf.send(mensaje.encode("utf-8"))
                print(f"Mensaje enviado: {mensaje}")
                return True  # Si el envío es exitoso, salimos de la función
            except OSError:
                print("Error al enviar el mensaje. Reintentando...")
        else:
            print(f"Error: el mensaje es demasiado largo (>{32} bytes).")
            break
        utime.sleep(delay)  # Pausa de reintento
    print(f"Error al enviar el mensaje después de {retries} intentos.")
    return False  # Si se superan los reintentos, devolvemos False

# --- Programa principal ---
def main():
    nrf = configurar_nrf()
    nrf.start_listening()
    print("Emisor listo para enviar datos parabólicos.\n")

    x = 0  # Valor inicial de x (índice para la parábola)
    A, k, B = 5, math.pi/10, 5  # Parámetros de la función seno (sube hasta 10 y baja a 0)

    # La cantidad de pasos o la longitud total del ciclo para que la parábola suba y baje
    max_x = int(2 * math.pi / k)  # Un ciclo completo de seno

    while x <= max_x:
        # Generar el valor parabólico y usando seno
        y = generar_parabola(x, A, k, B)
        
        # Crear el mensaje con el valor de X e Y en formato (X, Y)
        mensaje = f"{x},{y:.2f}"
        
        # Verificar si el mensaje no excede el límite de 32 bytes
        if len(mensaje) <= 32:
            # Enviar el mensaje
            if enviar_mensaje(nrf, mensaje, retries=3, delay=1):
                print(f"Datos enviados: {mensaje}")
        
        # Incrementar x para la siguiente iteración
        x += 1
        
        # Esperar un poco antes de enviar el siguiente valor
        utime.sleep(1)  # Pausa de 1 segundo entre los envíos

    print("Ciclo completo de subida y bajada realizado.")

# --- Ejecutar ---
main()


