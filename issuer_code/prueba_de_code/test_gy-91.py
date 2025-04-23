import machine as mch
import time
import mpu9250
import bmp280

i2c = mch.I2C(0, scl=mch.Pin(22), sda=mch.Pin(21), freq=400000)  # Usando SCL=22, SDA=21
led_pin = mch.Pin(2, mch.Pin.OUT)

print("Iniciando I2C...")

devices = i2c.scan()

print("Dispositivos conectados: ", devices)

mpu_ok = 0x68 in devices
bmp_ok = 0x76 in devices or 0x77 in devices

if (mpu_ok and bmp_ok):
    led_pin.on()
    mpu = mpu9250.MPU9250(i2c)  # Configura el MPU9250 (con X o Y como opción)
    bmp = bmp280.BMP280(i2c)
    led_pin.off()
    print("MPU9250 y BMP280 conectados.")
elif mpu_ok:
    mpu = mpu9250.MPU9250(i2c)
    print("Solo se conectó MPU")
elif bmp_ok:
    bmp = bmp280.BMP280(i2c)
    print("Solo se conectó BMP")
else:
    print("Fallo en la conexión de los sensores.")


def read_data(max_retries=3):
    attempts = 0
    while attempts < max_retries:
        try:
            aceleracion = mpu.accel
            giroscopio = mpu.gyro
            temperatura = bmp.temp
            presion = bmp.press
            altitud = bmp.alt

            # Accediendo a las componentes del vector
            aceleracion_x, aceleracion_y, aceleracion_z = aceleracion.x, aceleracion.y, aceleracion.z
            giroscopio_x, giroscopio_y, giroscopio_z = giroscopio.x, giroscopio.y, giroscopio.z

            return aceleracion_x, aceleracion_y, aceleracion_z, giroscopio_x, giroscopio_y, giroscopio_z, temperatura, presion, altitud
        except Exception as e:
            attempts += 1
            print(f"Error al leer datos, intento {attempts}/{max_retries}: {e}")
            if attempts >= max_retries:
                print("Número máximo de intentos alcanzado. Reiniciando sensores...")
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
        
        aceleracion_x, aceleracion_y, aceleracion_z, giroscopio_x, giroscopio_y, giroscopio_z, temperatura, presion, altitud = resultados
        
        print("\n--- Datos Recolectados ---")
        print(f"Aceleración:    x={aceleracion_x:.2f}, y={aceleracion_y:.2f}, z={aceleracion_z:.2f} (m/s²)")
        print(f"Giroscopio:     x={giroscopio_x:.2f}, y={giroscopio_y:.2f}, z={giroscopio_z:.2f} (°/s)")
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

