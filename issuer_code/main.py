import machine as mch
import time
import json
import mpu9250
import bmp280
from nrf24l01 import NRF24L01
from gps_module import NE06M

def initialize_modules():
    try:
        # Comprobar I2C
        i2c = mch.I2C(0)
        print("Escaneando I2C...")
        devices = i2c.scan()
        print("Dispositivos encontrados en I2C:", devices)

        mpu_ok = 0x68 in devices
        bmp_ok = 0x76 in devices or 0x77 in devices

        # Inicialización de MPU y BMP
        if mpu_ok and bmp_ok:
            mpu = mpu9250.MPU9250()
            bmp = bmp280.BMP280()
        elif mpu_ok:
            mpu = mpu9250.MPU9250()
            print("Solo se conectó MPU")
            bmp = None
        elif bmp_ok:
            bmp = bmp280.BMP280()
            print("Solo se conectó BMP")
            mpu = None
        else:
            print("Fallo en la conexión de MPU/BMP")
            return False, None, None, None, None, None, None

        # Inicialización GPS
        try:
            gps = NE06M()
            print("GPS inicializado.")
            gps_ok = True
        except Exception as e:
            gps_ok = False
            print("Error al inicializar GPS:", e)

        # Inicialización Sensor UV
        try:
            uv_pin = mch.Pin(34, mch.Pin.IN)
            uv_adc = mch.ADC(uv_pin)
            print("Sensor UV configurado")
            uv_ok = True
        except Exception as e:
            print("Sensor UV no encontrado:", e)
            uv_ok = False

        # Inicialización NRF24L01
        try:
            spi = mch.SPI(1, baudrate=5000000, polarity=0, phase=0)
            csn_pin = mch.Pin(5, mch.Pin.OUT)
            ce_pin = mch.Pin(4, mch.Pin.OUT)
            radio = NRF24L01(spi, csn_pin, ce_pin)
            radio.open_tx_pipe(b'\x01\x02\x03\x04\x05')
            nrf_ok = True
            print("NRF24L01 inicializado.")
        except Exception as e:
            nrf_ok = False
            print("NRF24L01 no disponible:", e)

        # Verificar que todos los módulos estén funcionando
        if not (mpu_ok and bmp_ok and gps_ok and uv_ok and nrf_ok):
            print("Faltan módulos requeridos. Abortando ejecución.")
            print("Resumen de estado:")
            print(f"MPU9250: {'OK' if mpu_ok else 'ERROR'}")
            print(f"BMP280: {'OK' if bmp_ok else 'ERROR'}")
            print(f"GPS: {'OK' if gps_ok else 'ERROR'}")
            print(f"UV: {'OK' if uv_ok else 'ERROR'}")
            print(f"NRF24L01: {'OK' if nrf_ok else 'ERROR'}")
            return False, mpu, bmp, gps, uv_adc, radio, nrf_ok

        # Si todo está bien, devolver los módulos inicializados
        return True, mpu, bmp, gps, uv_adc, radio, nrf_ok

    except Exception as e:
        print(f"Error en la inicialización: {e}")
        return False, None, None, None, None, None, None

def convert_adc(valor):
    return (valor / 4095) * 100

def read_all_sensors(mpu, bmp, uv_adc, gps):
    try:
        # Leer sensores I2C y analógico
        aceleracion = mpu.accel if mpu else None
        gyroscopio = mpu.gyro if mpu else None
        magnetometro = mpu.mag if mpu else None
        temperatura = bmp.temp if bmp else None
        presion = bmp.press if bmp else None
        altitud = bmp.alt if bmp else None
        uv_value = uv_adc.read() if uv_adc else None

        # Leer GPS
        gps.update()
        lat = gps.latitude if gps.latitude else None
        lon = gps.longitude if gps.longitude else None

        # Validación básica de GPS
        if lat is None or lon is None:
            print("GPS aún no tiene datos válidos.")
            return None

        return {
            "aceleracion": aceleracion,
            "gyroscopio": gyroscopio,
            "magnetometro": magnetometro,
            "temperatura": temperatura / 100 if temperatura else None,
            "presion": presion / 100 if presion else None,
            "altitud": altitud,
            "radiacion_uv": convert_adc(uv_value) if uv_value else None,
            "gps": {
                "latitud": lat,
                "longitud": lon
            }
        }
    except Exception as e:
        print("Error al leer sensores:", e)
        return None

def transmitir_data(data, radio):
    try:
        json_data = json.dumps(data)
        print("Transmitiendo:", json_data)
        radio.write(json_data)
    except Exception as e:
        print("Error al transmitir datos:", e)

def loop(mpu, bmp, uv_adc, gps, radio):
    data = read_all_sensors(mpu, bmp, uv_adc, gps)
    if data:
        transmitir_data(data, radio)
    else:
        print("Datos incompletos, no se transmite.")

# Inicio del programa
print("Iniciando la inicialización de módulos...")
while True:
    initialized, mpu, bmp, gps, uv_adc, radio, nrf_ok = initialize_modules()

    if initialized:
        print("Todos los módulos están listos. Iniciando transmisión...")
        while True:
            loop(mpu, bmp, uv_adc, gps, radio)
            time.sleep(0.3)
    else:
        print("Fallo en la inicialización de los módulos. Reintentando...")
        time.sleep(5)  # Esperar 5 segundos antes de intentar nuevamente
