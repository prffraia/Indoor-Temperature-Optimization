#include "DHT.h"
// #include <WiFiS3.h>
#include "SPI.h"
#include "WiFiNINA.h"
#define Type DHT22

//----------------------------------------------------------------------------------------------------------------------

//constants WiFi
const char ssid[] = "MIWIFI_CASA_2G";
const char pass[] = "PEREZRAYON2021";

int status = WL_IDLE_STATUS;
WiFiClient client;

int HTTP_PORT = 80;
String HTTP_METHOD = "GET";
char HOST_NAME[] = "192.168.1.200";
String PATH_NAME = "/php_code/insert_dht22_GET.php";
String query_humidity = "?humidity=";
String query_temperature = "?temperature=";

//constants DHT22
int sensePin = 2;

DHT HT(sensePin, Type); //object creation

float humidityData;
float temperatureData;

//-------------------------------------------------------------------------------------------------------------------------

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  HT.begin();
  //check for the wifi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    //don't continue
    while (true)
      ;
  }
  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION){
    Serial.println("Please upgrade the firmware");
  }

  //attempt to connect to WiFi network:
  Serial.println("Attempting to connect to WPA network...");
  Serial.print("SSID: ");
  Serial.println(ssid);

  status = WiFi.begin(ssid, pass);
  delay(10000); //wait 10 seconds for connection
  if (status != WL_CONNECTED){
    Serial.print("Couldn't get a WiFi connection");
    while(true);
  }
  else {
    Serial.println("Connected to WiFi");
    delay(10000);
  }
  //print you board's IP address:
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  delay(3000);

}


//---------------------------------------------------------------------------------------------------------------------------

void loop() {
  // put your main code here, to run repeatedly:
humidityData = HT.readHumidity();
temperatureData = HT.readTemperature();
Sending_To_phpmyadmindatabase();
delay(300000); //interval
}

  void Sending_To_phpmyadmindatabase() //Connecting with SQL
  {
    Serial.println("Starting SQL Connection...");
    if (client.connect(HOST_NAME, HTTP_PORT)){
      Serial.println("connected");
      //Make HTTP request:
      Serial.print(HTTP_METHOD + " " + PATH_NAME + query_humidity);
      client.print(HTTP_METHOD + " " + PATH_NAME + query_humidity);
      Serial.println(humidityData);
      client.print(humidityData);
      Serial.print("&temperature=");
      client.print("&temperature=");
      Serial.println(temperatureData);
      client.print(temperatureData);
      client.print(" "); //Space before HTTP/1.1
      client.print("HTTP/1.1");
      client.println();
      client.print("Host:");
      client.println(HOST_NAME);
      client.println("Connection: close");
      client.println();
    } else{
      Serial.println("connection failed");
    }
  }