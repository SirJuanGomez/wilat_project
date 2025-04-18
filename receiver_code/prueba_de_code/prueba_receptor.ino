#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <IRremote.h>

RF24 radio(4, 5);  // CE, CSN
const byte direccion[5] = {0x01, 0x02, 0x03, 0x04, 0x05};

int recv_pin = 2;  // Pin del receptor IR
IRrecv irrecv(recv_pin);
decode_results results;

float data[15];    // Almacena los 15 datos
uint8_t index = 0; // Índice actual de recepción
bool graficar = false;  // Flag que indica si se debe graficar o recibir datos

void setup() {
  Serial.begin(115200);  // Inicia la comunicación Serial con el PC
  irrecv.enableIRIn();   // Habilitar el receptor IR
  radio.begin();
  radio.setChannel(30);
  radio.setPALevel(RF24_PA_HIGH);
  radio.setDataRate(RF24_250KBPS);
  radio.openReadingPipe(1, direccion);
  radio.startListening();
}

void loop() {
  // Revisar si se recibe un comando IR para graficar
  if (irrecv.decode(&results)) {
    long int decCode = results.value;
    irrecv.resume();  // Recibir el siguiente código

    // Comprobar si el comando es el de "graficar"
    if (decCode == 0x1234) {  // Suponiendo que el código IR para "graficar" es 0x1234
      Serial.println("graficar");  // Enviar comando al PC
      graficar = true;  // Activar flag de graficar
      delay(1000);  // Evitar múltiples envíos del mismo comando
    }
  }

  // Si el flag de "graficar" está activado, no se reciben datos, solo se espera
  if (graficar) {
    return;  // Si estamos en modo graficar, no procesamos más datos
  }

  // Revisar si se reciben los datos del NRF24L01
  if (radio.available()) {
    char buffer[32] = {0};
    radio.read(&buffer, sizeof(buffer));
    float valor = atof(buffer);  // Convertimos a número
    data[index] = valor;
    index++;

    if (index >= 15) {
      // Ya tenemos todos los datos, enviar como JSON al PC
      enviarComoJson();
      index = 0;  // Resetear el índice para el siguiente conjunto de datos
    }
  }
}

void enviarComoJson() {
  Serial.print("{");
  Serial.print("\"aceleracion\":[");
  Serial.print(data[0], 3); Serial.print(", ");
  Serial.print(data[1], 3); Serial.print(", ");
  Serial.print(data[2], 3); Serial.print("], ");

  Serial.print("\"gyroscopio\":[");
  Serial.print(data[3], 3); Serial.print(", ");
  Serial.print(data[4], 3); Serial.print(", ");
  Serial.print(data[5], 3); Serial.print("], ");

  Serial.print("\"magnetometro\":[");
  Serial.print(data[6], 3); Serial.print(", ");
  Serial.print(data[7], 3); Serial.print(", ");
  Serial.print(data[8], 3); Serial.print("], ");

  Serial.print("\"temperatura\":");
  Serial.print(data[9], 2); Serial.print(", ");

  Serial.print("\"presion\":");
  Serial.print(data[10], 2); Serial.print(", ");

  Serial.print("\"altitud\":");
  Serial.print(data[11], 2); Serial.print(", ");

  Serial.print("\"radiacion_uv\":");
  Serial.print(data[12], 2); Serial.print(", ");

  Serial.print("\"gps\":{");
  Serial.print("\"latitud\":");
  Serial.print(data[13], 6); Serial.print(", ");
  Serial.print("\"longitud\":");
  Serial.print(data[14], 6);
  Serial.print("}");

  Serial.println("}");
}
