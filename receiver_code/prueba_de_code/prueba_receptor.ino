//#include <SPI.h>
//#include <RF24.h>
//#include<ArduinoJson.h>

RF24 radio(17,5);

byte direccion[6] = {0x01,0x02,0x03,0x04,0x05,0x06};

struct sensor_data
{
    float aceleracion[3];
    float gyroscopio[3];
    int magnetometro[3];
    float temperatura;
    float presion;
    float radiacion_uv;
};

void setup(){
    Serial.begin(115200);
    radio.begin();
    radio.openReadingPipe(1, direccion);
    radio.setPALevel(RF24_PA_HIGH);
    radio.startListening();

    Serial.println("Escuchando datos...");
}

void loop(){
    if (radio.avaliable()){
        char recived_data[32] = "";
        radio.read(&recived_data, sizeof(recived_data));
        StaticJsonDocument<200> doc;
        DeserializationError error = deserializeJson(doc, datosRecibidos);
        
        if (error){
            Serial.println("Error al leer transmision: ");
            Serial.println(error.fstr());
            return ;
        }

        SensorData data;
        data.aceleracion[0] = doc["aceleracion"][0];
        data.aceleracion[1] = doc["aceleracion"][1];
        data.aceleracion[2] = doc["aceleracion"][2];
        data.gyroscopio[0] = doc["gyroscopio"][0];
        data.gyroscopio[1] = doc["gyroscopio"][1];
        data.gyroscopio[2] = doc["gyroscopio"][2];
        data.magnetometro[0] = doc["magnetometro"][0];
        data.magnetometro[1] = doc["magnetometro"][1];
        data.magnetometro[2] = doc["magnetometro"][2];
        data.temperatura = doc["temperatura"];
        data.presion = doc["presion"];
        data.radiacion_uv = doc["radiacion_uv"];

        // Escribe los datos recividos

        Serial.println("Datos recibidos:");
        Serial.print("Aceleracion: ");
        Serial.print(data.aceleracion[0]);
        Serial.print(", ");
        Serial.print(data.aceleracion[1]);
        Serial.print(", ");
        Serial.println(data.aceleracion[2]);

        Serial.print("Giroscopio: ");
        Serial.print(data.gyroscopio[0]);
        Serial.print(", ");
        Serial.print(data.gyroscopio[1]);
        Serial.print(", ");
        Serial.println(data.gyroscopio[2]);

        Serial.print("Magnetometro: ");
        Serial.print(data.magnetometro[0]);
        Serial.print(", ");
        Serial.print(data.magnetometro[1]);
        Serial.print(", ");
        Serial.println(data.magnetometro[2]);

        Serial.print("Temperatura: ");
        Serial.println(data.temperatura);
        Serial.print("Presion: ");
        Serial.println(data.presion);
        Serial.print("Radiacion UV: ");
        Serial.println(data.radiacion_uv);

        Serial.println();
       
    }
}
