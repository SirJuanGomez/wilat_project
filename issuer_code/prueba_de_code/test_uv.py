import macine as mch 
import time 

uv_pin = mch.Pin(34,mch.Pin.IN)

try:
    uv_adc = mch.ADC(uv_pin)
    uv_adc.width(mch.ADC.WIDHT_12BIT)
    uv_adc.attten(mch.ADC.ATTN_0DB)
    print(f"Sensor Configurado")
except Exception as e:
    print(f"Sensor no encontrado:",e)

def read_data():
    try:
        uv_value = uv_adc.read()
        print(f"Valor UV: {uv_value}")
        return uv_value
    except Exception as e:
        print(f"Error al leer los datos: {e}")
        return None 

while True:
    uv_value = read_data()
    if uv_value is not None:

        if uv_value < 1000:
            print("Nivel UV bajo")
        elif uv_value < 2000:
            print("Nivel UV moderado")
        else:
            print("Nivel UV alto")
    time.sleep(1)