import machine as mch
import time
import json
from mpu9250 import MPU9250
from bmp280 import BMP280
from nrf24 import NRF24

i2c = mch.I2C(0)

mpu = MPU9250(i2c, address=0x68)
bmp = BMP280(i2c, address=0x77)

spi = mch.SPI(1, baudrate=5000000, polarity=0, phase=0)
csn_pin = mch.Pin(5, mch.Pin.OUT)
ce_pin = mch.Pin(4, mch.Pin.OUT)

radio = NRF24(spi, csn_pin, ce_pin)
radio.open_tx_pipe(b'\x01\x02\x03\x04\x05')

uv_pin = mch.Pin(34)
uv_adc = mch.ADC(uv_pin)

def read_data():
    try:
        aceleracion = mpu.accel
        gyroscopio = mpu.gyro
        magnetometro = mpu.mag
        temperatura, presion = bmp.read_compensated_data()
        uv_value = uv_adc.read()  # Aquí se obtiene el valor del sensor UV

        return aceleracion, gyroscopio, magnetometro, temperatura, presion, uv_value
    except Exception as e:
        return None

def transmitir_data(data):
    try:
        radio.write(data)
    except Exception as e:
        return None

def convert_adc(valor):
    converted_value = (valor / 4095) * 100 
    return converted_value

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

def open_parachute():
    return None

def loop():
    acel, gyro, mag, temp, press, uv_value = read_data()  # Leer los datos

    if acel is not None and gyro is not None and mag is not None and temp is not None and press is not None:
        data_to_trans = format_data(acel, gyro, mag, temp, press, uv_value)  # Pasar uv_value a la función
        transmitir_data(data_to_trans)

while True:
    loop()
    time.sleep(0.3)

