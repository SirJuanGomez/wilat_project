import serial
import json
import time

SERIAL_PORT = 'COM5'
BAUDRATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

fragment_buffer = {}
last_receive_time = time.time()
timeout = 2  # segundos para reiniciar el buffer si no llega nada nuevo

print("Esperando fragmentos en COM5...")

def reset_buffer():
    global fragment_buffer
    fragment_buffer = {}
    print("🧹 Buffer reiniciado por timeout o error.\n")

try:
    while True:
        if ser.in_waiting:
            raw = ser.read(ser.in_waiting)
            for byte_chunk in raw.split(b'\n'):  # separa si hay múltiples paquetes juntos
                if len(byte_chunk) > 1:
                    index = byte_chunk[0]
                    data = byte_chunk[1:]
                    fragment_buffer[index] = data
                    last_receive_time = time.time()

            # Comprobamos si recibimos todos los fragmentos esperados
            # Solo intentamos reconstruir si hay fragmentos
            if fragment_buffer:
                expected_count = max(fragment_buffer.keys()) + 1
                if len(fragment_buffer) == expected_count:
                    # Reconstruimos y procesamos el mensaje
                    full_bytes = b''.join(fragment_buffer[i] for i in sorted(fragment_buffer))
                    try:
                        decoded = full_bytes.decode('utf-8')
                        data = json.loads(decoded)
                        print("\n✅ Paquete completo recibido:")
                        print(json.dumps(data, indent=2))
                    except Exception as e:
                        print(f"⚠️ Error al decodificar paquete: {e}")

                    reset_buffer()


        # Reinicia si pasa mucho tiempo sin completar el paquete
        if time.time() - last_receive_time > timeout and fragment_buffer:
            print("⏰ Timeout esperando fragmentos faltantes.")
            reset_buffer()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nLectura interrumpida por el usuario.")
finally:
    ser.close()
