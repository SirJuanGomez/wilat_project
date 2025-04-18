import machine as mch
import time
import json
import mpu9250
import bmp280
from nrf24l01 import NRF24L01
from gps_module import NE06M

# Escaneo I2C
i2c = mch.I2C(0)
print("Escaneando I2C...")
devices = i2c.scan()
print("Dispositivos encontrados en I2C:", devices)

# Verificación de sensores I2C
mpu_ok = 0x68 in devices
bmp_ok = 0x76 in devices or 0x77 in devices

if mpu_ok:
    print("✅ MPU9250 detectado.")
    mpu = mpu9250.MPU9250()
else:
    print("❌ MPU9250 no detectado.")

if bmp_ok:
    print("✅ BMP280 detectado.")
    bmp = bmp280.BMP280()
else:
    print("❌ BMP280 no detectado.")

# Inicialización GPS
try:
    gps = NE06M()
    time.sleep(1)
    if gps.uart.any():
        line = gps.uart.readline()
        if line:
            gps_ok = True
            print("✅ GPS detectado.")
        else:
            gps_ok = False
            print("❌ GPS no responde.")
    else:
        gps_ok = False
        print("❌ GPS sin datos.")
except Exception as e:
    gps_ok = False
    print("❌ Error al inicializar GPS:", e)

# Sensor UV (ADC)
try:
    uv_adc = mch.ADC(mch.Pin(34))
    _ = uv_adc.read()
    uv_ok = True
    print("✅ Sensor UV operativo.")
except Exception as e:
    uv_ok = False
    print("❌ Sensor UV no disponible:", e)

# Módulo NRF24L01
try:
    spi = mch.SPI(1, baudrate=5000000, polarity=0, phase=0)
    csn_pin = mch.Pin(5, mch.Pin.OUT)
    ce_pin = mch.Pin(4, mch.Pin.OUT)
    radio = NRF24L01(spi, csn_pin, ce_pin)
    radio.open_tx_pipe(b'\x01\x02\x03\x04\x05')
    nrf_ok = True
    print("✅ NRF24L01 inicializado.")
except Exception as e:
    nrf_ok = False
    print("❌ NRF24L01 no disponible:", e)

# Validación final de todos los módulos
if not (mpu_ok and bmp_ok and gps_ok and uv_ok and nrf_ok):
    print("❌ Faltan módulos requeridos. Abortando ejecución.")
    print("Resumen de estado:")
    print(f"MPU9250: {'✅' if mpu_ok else '❌'}")
    print(f"BMP280: {'✅' if bmp_ok else '❌'}")
    print(f"GPS: {'✅' if gps_ok else '❌'}")
    print(f"UV: {'✅' if uv_ok else '❌'}")
    print(f"NRF24L01: {'✅' if nrf_ok else '❌'}")
    raise SystemExit()

# Funciones principales
def read_data():
    try:
        aceleracion = mpu.accel
        gyroscopio = mpu.gyro
        magnetometro = mpu.mag
        temperatura = bmp.temp
        presion = bmp.press
        altitud = bmp.alt
        uv_value = uv_adc.read()
        return aceleracion, gyroscopio, magnetometro, temperatura, presion,altitud , uv_value
    except Exception as e:
        print("Error en read_data:", e)
        return None

def transmitir_data(data):
    try:
        radio.write(data)
    except Exception as e:
        print("Error al transmitir datos:", e)

def convert_adc(valor):
    return (valor / 4095) * 100

def format_data(acel, gyro, mag, temp, press, uv_value): 
    uv = convert_adc(uv_value)
    data_collected = {
        "aceleracion": acel,
        "gyroscopio": gyro,
        "magnetometro": mag,
        "temperatura": temp / 100,
        "presion": press / 100,
        "radiacion_uv": uv
    }
    return json.dumps(data_collected)

def loop():
    try:
        result = read_data()
        if result is None:
            print("No se pudo leer datos.")
            return
        acel, gyro, mag, temp, press, uv_value = result
        data_to_trans = format_data(acel, gyro, mag, temp, press, uv_value)
        print("Transmitiendo:", data_to_trans)
        transmitir_data(data_to_trans)
    except Exception as e:
        print("Error en loop:", e)

# Inicio del programa
print("🚀 Todos los módulos están listos. Iniciando transmisión...")
while True:
    loop()
    time.sleep(0.3)

