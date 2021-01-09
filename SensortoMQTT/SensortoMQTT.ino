#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

// Set DHT pin:
#define DHTPIN 5
#define DHTTYPE DHT22 
DHT dht = DHT(DHTPIN, DHTTYPE);

int RXPin = 12;
int TXPin = 14;

unsigned long timer = millis();
unsigned long secondTimer;

static const uint32_t GPSBaud = 9600;
String hourtime = "";
String minutetime = "";
String secondtime = "";
String totaltime = "";
String latitude = "";
String longitude = "";
String coordinates = "";

// Create a TinyGPS++ object
TinyGPSPlus gps;

// Create a software serial port called "gpsSerial"
SoftwareSerial gpsSerial(RXPin, TXPin);

// use onboard LED for convenience 
#define LED (2)

// Wifi configuration
const char* ssid = "DESKTOP-EONMLP1 1596";
const char* password = "76T{r870";

// MQTT Configuration
// if you have a hostname set for the MQTT server, you can use it here
const char *serverHostname = "broker.hivemq.com";


// the topic we want to use
const char* topic = "Project3/LDR_classroom/Mads";
const char* topic2 = "Project3/Temperature_classroom/Mads";
const char* topic3 = "Project3/GPS_location/Mads";
const char* topic4 = "Project3/GPS_time/Mads";
const char* topic5 = "Project3/Humidity_classroom/Mads";

int ldr = A0;
int value = 0;

WiFiClient espClient;
PubSubClient client(espClient);

// connect to wifi
void connectWifi() 
{
  delay(10);
  // Connecting to a WiFi network
  Serial.printf("\nConnecting to %s\n", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected on IP address ");
  Serial.println(WiFi.localIP());
}


// connect to MQTT server - checks for a connection,
// if none is active it attempts to connect to MQTT server

void connectMQTT() 
{
  // Wait until we're connected
  while (!client.connected()) 
  {
    // Create a random client ID
    String clientId = "ESP8266-";
    clientId += String(random(0xffff), HEX);
    Serial.printf("MQTT connecting as client %s...\n", clientId.c_str());
    // Attempt to connect
    if (client.connect(clientId.c_str())) 
    {
      Serial.println("MQTT connected");
      // ... and resubscribe
      client.subscribe(topic);
    } else 
    {
      Serial.printf("MQTT failed, state %s, retrying...\n", client.state());
      // Wait before retrying
      delay(2500);
    }
  }
}



void setup() 
{     
  // Configure serial port for debugging
  Serial.begin(9600);
  // Initialise wifi connection - this will wait until connected
  connectWifi();
  // connect to MQTT server  
  client.setServer(serverHostname, 1883);
  gpsSerial.begin(GPSBaud);
  //client.setCallback(callback);
  dht.begin();
}

void loop() 
{
    Serial.println("Godmorgen jeg er klar igen!");
//    Serial.println(timer);
    if (!client.connected()) 
      {
      connectMQTT();
      }
    // this is ESSENTIAL!
    client.loop();
    value = analogRead(ldr);
    client.publish(topic, String(value).c_str());
    if (value >= 70)
    {
      display_values();
      displayInfo();
      TempHumi();
      secondTimer = millis();
      if (secondTimer - timer > 11000)
      {
        Serial.println("sleeping");
        ESP.deepSleep(600e5);
      }
//      Serial.println("Sleeping");
//      ESP.deepSleep(600e6); //10 min delay når lys nivauet er acceptabelt
    }
    else
    {   
    Serial.println("Det er sgu lidt for mørkt, tænd lige noget lys");
    delay(5000);
    Serial.println("Jeg sover lige ;)");
    ESP.deepSleep(1200e6); //20 min delay når der er mørkt
    }
}
