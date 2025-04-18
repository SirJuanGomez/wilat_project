import machine as mch
import time

class NE06M:
    def __init__(self, uart_num=1, baudrate=9600, tx_pin=17, rx_pin=16):
        self.set_uart_params(uart_num, baudrate, tx_pin, rx_pin)
        self._latitude = None
        self._longitude = None
        self._altitude = None
        self._satellites = None
        self._time = None
        self._hemisphere = None
        time.sleep(1)

    def set_uart_params(self, uart_num, baudrate, tx_pin, rx_pin):
        self.uart = mch.UART(uart_num, baudrate=baudrate, tx=mch.Pin(tx_pin), rx=mch.Pin(rx_pin))
        self.uart.init(bits=8, parity=None, stop=2)

    def _is_valid_gpgga(self, nmea):
        return nmea.startswith("$GPGGA") and "," in nmea and nmea.split(",")[7] not in ['0', '00']

    def _decode_coord(self, coord):
        try:
            deg = int(coord[:2])
            min_float = float(coord[2:])
            return deg + (min_float / 60)
        except:
            return None

    def update(self):
        while self.uart.any():
            try:
                data = self.uart.read().decode('utf-8')
                for sentence in data.split("\r\n"):
                    if self._is_valid_gpgga(sentence):
                        self._parse_gpgga(sentence)
                        return 
            except Exception as e:
                print("Error leyendo datos GPS:", e)

    def _parse_gpgga(self, sentence):
        parts = sentence.split(",")
        if len(parts) < 10:
            return

        self._time = f"{parts[1][0:2]}:{parts[1][2:4]}:{parts[1][4:6]}"
        self._latitude = self._decode_coord(parts[2])
        self._longitude = self._decode_coord(parts[4])
        self._hemisphere = parts[3] + parts[5]
        self._satellites = int(parts[7])
        self._altitude = float(parts[9]) if parts[9] else None


    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def altitude(self):
        return self._altitude

    @property
    def satellites(self):
        return self._satellites

    @property
    def time(self):
        return self._time

    @property
    def hemisphere(self):
        return self._hemisphere
