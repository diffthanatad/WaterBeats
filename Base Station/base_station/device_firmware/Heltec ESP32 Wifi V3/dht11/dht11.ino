#include "Arduino.h"
#include "wifiCredentials.h"
#include "HT_SSD1306Wire.h"
#include "DHT.h"
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

SSD1306Wire display(0x3c, 500000, SDA_OLED, SCL_OLED, GEOMETRY_128_64, RST_OLED);  // addr , freq , i2c group , resolution , rst

void initWiFi() {
  display.clear();
  display.drawString(0, 0, "Connecting to WiFi...");
  display.display();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.println(WiFi.localIP());
  display.clear();
  display.drawString(0, 0, "WiFi Connected");
  display.drawString(0, 20, "Local IP:");
  display.drawString(0, 30, (WiFi.localIP().toString()));
  display.drawString(0, 40, "MAC Address:");
  display.drawString(0, 50, (String)(WiFi.macAddress()));
  display.display();
}



void setup() {
  Serial.begin(115200);
  pinMode(Vext, OUTPUT);
  digitalWrite(Vext, LOW);
  delay(100);
  display.init();
  display.setFont(ArialMT_Plain_10);
  display.clear();
  display.display();
  initWiFi();
}


void loop() {
  delay(1000);

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  if (WiFi.status()==WL_CONNECTED) {
    HTTPClient http;
    http.begin(server);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    String temperatureData = "{\"sensor_id\": \"" + (String)(WiFi.macAddress()) + "_A\", \"reading\": \"" + String(t) + "\"}";
    String humidityData = "{\"sensor_id\": \"" + (String)(WiFi.macAddress()) + "_B\", \"reading\": \"" + String(h) + "\"}";
    Serial.println(temperatureData);
    Serial.println(humidityData);
    int temperatureReponse = http.POST(temperatureData);
    Serial.print("Temperature HTTP Response code is: ");
    Serial.println(temperatureReponse);
    int humidityReponse = http.POST(humidityData);
    Serial.print("Humidity HTTP Response code is: ");
    Serial.println(humidityReponse);
    http.end();
    }
    else {
      Serial.println("Failed to send sensor data. No connection!");
    }

  
  display.clear();
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0, 0, "MAC Address:");
  display.drawString(0, 10, (String)(WiFi.macAddress()));
  display.drawString(0, 30, "Temperature:");
  display.drawString(0, 50, "Humidity:");
  display.setTextAlignment(TEXT_ALIGN_RIGHT);
  display.drawString(128, 30, String(t) + " C");
  display.drawString(128, 50, String(h) + " %");
  display.display();


  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.println(F(""));
}
