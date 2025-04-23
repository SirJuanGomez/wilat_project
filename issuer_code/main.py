import machine as mch
import time
import math
import json 
from mpu9250 import MPU9250
from bmp280 import BMP280
from nrf24l01 import NRF24L01
from gps_module import NE06M
def modules_ini():
    try:
        i2c = mch.I2C(0, scl=mch.Pin(22), sda=mch.Pin(21), freq=400000)
        devices = i2c.scan()
        mpu_ok = 0x68 in devices
        bmp_ok = 0x76 in devices or 0x77 in devices

        if mpu_ok and bmp_ok:
            mpu = MPU9250(i2c)
            bmp = BMP280(i2c)
            blinked()
        elif mpu_ok:
            mpu = MPU9250()
            print("Solo se conectó MPU")
            bmp = None
        elif bmp_ok:
            bmp = BMP280()
            print("Solo se conectó BMP")
            mpu = None
        else:
            print("Fallo en la conexión de MPU/BMP")
            return False, None, None, None, None, None
        
        try:
            gps = NE06M(uart_num=1, baudrate=9600, tx_pin=17, rx_pin=16)
            blinked()
            gps_ok = True
        except Exception as e:
            gps_ok = False
            print("Error al inicializar GPS:", e)

        try:
            nrf = nrf_set()
            nrf_ok = True
            blinked()
            print("NRF24L01 inicializado.")
        except Exception as e:
            nrf_ok = False
            print("NRF24L01 no disponible:", e)
        
        if not(mpu_ok and bmp_ok and gps_ok and nrf_ok):
            print("Faltan módulos:")
            print("Resumen de estado:")
            print(f"MPU9250: {'OK' if mpu_ok else 'ERROR'}")
            print(f"BMP280: {'OK' if bmp_ok else 'ERROR'}")
            print(f"GPS: {'OK' if gps_ok else 'ERROR'}")
            print(f"NRF24L01: {'OK' if nrf_ok else 'ERROR'}")
            return False, mpu, bmp, gps, radio, nrf_ok
        
        print("Todos los módulos se inicializaron correctamente.")
        return True, mpu, bmp, gps, nrf, nrf_ok
    
    except Exception as e:
        print(f"Error en la inicialización: {e}")
        return False, None, None, None, None, None
    
def nrf_set():
    spi = mch.SoftSPI(sck=mch.Pin(25), mosi=mch.Pin(33), miso=mch.Pin(32))
    csn = mch.Pin(26, mch.Pin.OUT)
    ce = mch.Pin(27, mch.Pin.OUT)
    nrf = NRF24L01(spi, csn, ce, payload_size=32)
    pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.stop_listening()
    
    return nrf

def read_data(mpu, bmp, gps):
    try:
        aceleracion = mpu.accel if mpu else None
        giroscopio = mpu.gyro if mpu else None
        temperatura = bmp.temp if bmp else None
        presion = bmp.press/100 if bmp else None
        altitud = bmp.alt if bmp else None
        gps.update()
        lat = gps.latitude
        lon = gps.longitude
        return (
            [round(aceleracion.x, 3), round(aceleracion.y, 3), round(aceleracion.z, 3)] if aceleracion else None,
            [round(giroscopio.x, 3), round(giroscopio.y, 3), round(giroscopio.z, 3)] if giroscopio else None,
            round(temperatura, 2) if temperatura is not None else None,
            round(presion, 2) if presion is not None else None,
            round(altitud, 2) if altitud is not None else None,
            {"lat": lat, "lon": lon} if lat and lon else None
        )
    except Exception as e:
        print("Error al leer sensores:", e)
        return None

def packed(mpu, bmp, gps, nrf):
    acc, gyro, temp, pres, alt, gps_data = read_data(mpu, bmp, gps)

    data = {
        "a": acc,
        "g": gyro,
        "t": temp,
        "p": pres,
        "at": alt,
        "gp": gps_data
    }

    if data:
        data_str = json.dumps(data) + "end"
        data_bytes = data_str.encode('utf-8')

        def sub_chunk(data_bytes, chunk_size=31):
            return [data_bytes[i:i + chunk_size] for i in range(0, len(data_bytes), chunk_size)]

        chunks = sub_chunk(data_bytes)
        count = len(chunks)

        print(f"Enviando {count} fragmentos...")

        for i, chunk in enumerate(chunks):
            packet = bytes([i]) + chunk  # índice + fragmento
            try:
                nrf.stop_listening()
                nrf.send(packet)
                print(f"Paquete {i + 1}/{count} enviado.")
            except Exception as e:
                print(f"Error al enviar paquete {i + 1}: {e}")

            print("-" * 40)

def blinked():
    led_pin = mch.Pin(2, mch.Pin.OUT)
    for _ in range(3):
        led_pin.on()
        time.sleep(0.1)
        led_pin.off()
        time.sleep(0.1)
def main():
    initialized, mpu, bmp, gps, nrf, nrf_ok = modules_ini()
    if not initialized:
        print("Error en la inicialización de los módulos.")
        return

    print("Sistema listo. Enviando datos sin esperar respuesta...\n")

    while True:
        packed(mpu, bmp, gps, nrf)
        time.sleep(3)

main()

