#include <ESP8266WiFi.h>

#define WIFI_SSID "thinkAP"
#define WIFI_PASS "penguinPinapplePizza"
IPAddress server(192, 168, 11, 8);
#define sensor A0
const int httpPort = 80;

void fanOn() {
  WiFiClient client;
  if (client.connect(server, httpPort)) {
    Serial.println("Connected");
    client.println("GET /fan1?status1=\"on\" HTTP/1.1");
    client.println();
  }
}

void fanOn() {
  WiFiClient client;
  if (client.connect(server, httpPort)) {
    Serial.println("Connected");
    client.println("GET /fan1?status1=\"on\" HTTP/1.1");
    client.println();
  }
}

void recordTemperature(int temp) {
  WiFiClient client;

  String url = "GET /temp?temp1=";
  url += temp;

  if (client.connect(server, httpPort)) {
    Serial.println("Connected");
    client.println(url);
    client.println();
  }
}


void setup() {
  pinMode(A0, INPUT);
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Starting up....");

  //  set up wifi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);

  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println();

  Serial.println(WiFi.localIP());

}

void loop() {
  int reading = analogRead(sensor); //needs 5V input not 3.3V
  float temperatureC = (double)reading / 1024;
  temperatureC = temperatureC * 5;
  temperatureC = temperatureC - .5;
  temperatureC = temperatureC * 100;
  Serial.print(temperatureC);
  Serial.println(" degrees C");
  recordTemperature(temperatureC);
  delay(300000);
}
