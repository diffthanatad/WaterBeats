#include "wifiCredentials.h"
#include "DHT.h"
#include "heltec.h"
#include <WiFi.h>

#define DHTPIN 2

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void initWiFi() {
  Heltec.display -> clear();
  Heltec.display -> drawString(0, 0, "Connecting to WiFi...");
  Heltec.display -> display();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.println(WiFi.localIP());
  Heltec.display -> clear();
  Heltec.display -> drawString(0, 0, "WiFi Connected");
  Heltec.display -> drawString(0, 20, "Local IP:");
  Heltec.display -> drawString(0, 30, (WiFi.localIP().toString()));
  Heltec.display -> drawString(0, 40, "MAC Address:");
  Heltec.display -> drawString(0, 50, (String)(WiFi.macAddress()));
  Heltec.display -> display();
}

void setup() {
  Serial.begin(9600);
  
  //Heltec.begin(true /*DisplayEnable Enable*/, false /*LoRa Enable*/, true /*Serial Enable*/);
  //Heltec.display -> clear();
  
  //initWiFi();
  dht.begin();
}

void loop() {
  delay(2000);
  
  // Reading temperature or humidity takes about 250 milliseconds, readings may be up to 2 seconds old
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.println(F(""));
  
}
