from machine import Pin, UART
import time

class NE06M:
    def __init__(self, uart_num=1, baudrate=9600, tx_pin=17, rx_pin=16):
        # Inicialización de UART
        self.uart = UART(uart_num, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))
        self.uart.init(bits=8, parity=None, stop=2)  # 8 bits de datos, sin paridad, 2 bits de parada
        time.sleep(1)  # Esperar un momento para asegurarnos de que el GPS esté listo

    def decode(self, coord):
        l = list(coord)
        for i in range(0, len(l)-1):
            if l[i] == ".":
                break
        base = l[0:i-2]
        degi = l[i-2:i]
        degd = l[i+1:]
        baseint = int("".join(base))
        degiint = int("".join(degi))
        degdint = float("".join(degd))
        degdint = degdint / (10**len(degd))
        degs = degiint + degdint
        full = float(baseint) + (degs / 60)
        return full

    def latitude(self, nmea):
        if nmea[0:6] == "$GPGGA":
            x = nmea.split(",")
            if x[7] == '0' or x[7] == '00':
                print("Incorrect Data")
                return
            lati = self.decode(x[2])
            return lati

    def longitude(self, nmea):
        if nmea[0:6] == "$GPGGA":
            x = nmea.split(",")
            if x[7] == '0' or x[7] == '00':
                print("Incorrect Data")
                return
            lon = self.decode(x[4])
            return lon

    def time(self, nmea):
        if nmea[0:6] == "$GPGGA":
            x = nmea.split(",")
            if x[7] == '0' or x[7] == '00':
                print("Incorrect Data")
                return
            t = x[1][0:2] + ":" + x[1][2:4] + ":" + x[1][4:6]
            return t

    def satellite(self, nmea):
        if nmea[0:6] == "$GPGGA":
            x = nmea.split(",")
            if x[7] == '0' or x[7] == '00':
                print("Incorrect Data")
                return
            s = int(x[7])
            return s

    def altitude(self, nmea):
        if nmea[0:6] == "$GPGGA":
            x = nmea.split(",")
            if x[7] == '0' or x[7] == '00':
                print("Incorrect Data")
                return
            alt = x[9]
            return alt

    def hemisphere(self, nmea):
        if nmea[0:6] == "$GPGGA":
            x = nmea.split(",")
            if x[7] == '0' or x[7] == '00':
                print("Incorrect Data")
                return
            hemi = x[3] + x[5]
            return hemi

    def read_gps_data(self):
        while True:
            if self.uart.any():
                data = self.uart.read().decode('utf-8')
                nmea_sentences = data.split("\r\n")
                for sentence in nmea_sentences:
                    if sentence.startswith("$GPGGA"):
                        lat = self.latitude(sentence)
                        lon = self.longitude(sentence)
                        t = self.time(sentence)
                        sat = self.satellite(sentence)
                        alt = self.altitude(sentence)
                        hemi = self.hemisphere(sentence)
            time.sleep(1)  # Esperar antes de leer el siguiente conjunto de datos

# Ejemplo de uso:
# Inicializar el objeto NE06M, usando UART1, a 9600 baudios, pines 17 (TX) y 16 (RX)
gps = NE06M(uart_num=1, baudrate=9600, tx_pin=17, rx_pin=16)
gps.read_gps_data()  # Iniciar la lectura de datos GPS
