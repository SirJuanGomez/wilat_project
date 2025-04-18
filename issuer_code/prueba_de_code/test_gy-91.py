import machine as mch 
import time 
import mpu9250
import bmp280

i2c = mch.I2C(0)
led_pin = mch.Pin(2,mch.Pin.OUT)

print("iniciando i2c")

devices = i2c.scan()

print("Dispositivos conectados: ",devices)

mpu_ok = 0x68 in devices
bmp_ok = 0x76 in devices or 0x77 in devices

if (mpu_ok and bmp_ok):
    led_pin.on()
    mpu = mpu9250.MPU9250()
    bmp = bmp280.BMP280()
    led_pin.off()
elif mpu_ok:
    mpu = mpu9250.MPU9250()
    print("Solo se conecto MPU")
elif bmp_ok:
    bmp = bmp280.BMP280()
    print("Solo se conecto BMP")
else:
    print("Fallo en la conexion")


def read_data(max_retries=3):
    attempts = 0
    while attempts < max_retries:
        try:
            aceleracion = mpu.accel
            giroscopio = mpu.gyro
            magnetometro = mpu.mag
            temperatura = bmp.temp
            presion = bmp.press
            altitud = bmp.alt
            return aceleracion, giroscopio, magnetometro, temperatura, presion, altitud
        except Exception as e:
            attempts += 1
            print(f"Error al leer datos, intento {attempts}/{max_retries}: {e}")
            if attempts >= max_retries:
                print("Número máximo de intentos alcanzado. Reiniciando sensores...")
                # Aquí podrías agregar un reinicio de los sensores o el I2C
                reset_sensors()
                return None
            time.sleep(1)  # Espera antes de intentar nuevamente

def reset_sensors():
    print("Reiniciando I2C...")
    # Resetear o reiniciar el bus I2C
    i2c.deinit()  # Desactiva I2C
    time.sleep(1)
    i2c.init(mch.I2C, baudrate=100000)  # Vuelve a inicializar I2C
    print("I2C reiniciado.")

def loop():
    try:
        resultados = read_data()
        if resultados is None:
            print("No hay datos")
            return
        
        aceleracion, giroscopio, magnetometro, temperatura, presion, altitud = resultados
        
        print("\n--- Datos Recolectados ---")
        print(f"Aceleración:    x={aceleracion[0]:.2f}, y={aceleracion[1]:.2f}, z={aceleracion[2]:.2f} (m/s²)")
        print(f"Giroscopio:     x={giroscopio[0]:.2f}, y={giroscopio[1]:.2f}, z={giroscopio[2]:.2f} (°/s)")
        print(f"Magnetómetro:   x={magnetometro[0]:.2f}, y={magnetometro[1]:.2f}, z={magnetometro[2]:.2f} (µT)")
        print(f"Temperatura:    {temperatura:.2f} °C")
        print(f"Presión:        {presion:.2f} hPa")
        print(f"Altitud:        {altitud:.2f} m")
        print("--------------------------\n")

    except Exception as e:
        print("Error en loop:", e)

while True:
    led_pin.on()
    loop()
    time.sleep(0.5)
    led_pin.off()
    time.sleep(0.5)
