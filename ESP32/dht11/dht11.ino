#include "wifiCredentials"
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

  if (WiFi.status()==WL_CONNECTED){
    HTTPClient http;

    http.begin(server);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      String httpRequestData = "field1=" + String(t);    
      int httpResponseCode = http.POST(httpRequestData);
     
      Serial.print("HTTP Response code is: ");
      Serial.println(httpResponseCode);
      http.end();
    }
    else {
      Serial.println("WiFi is Disconnected!");
    }

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.println(F(""));
}
