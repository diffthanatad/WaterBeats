#include "wifiCredentials.h"
#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 14

#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(9600);
  Serial.println("");
  Serial.print("ESP Board MAC Address:  ");
  Serial.println(WiFi.macAddress());
  initWiFi();
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements
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
