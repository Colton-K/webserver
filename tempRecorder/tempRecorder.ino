#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

ESP8266WebServer localserver(80);

#define WIFI_SSID "thinkAP"
#define WIFI_PASS "penguinPinapplePizza"
IPAddress server(192, 168, 11, 8);
#define sensor A0
const int httpPort = 80;

// globals for controlling temperature
int tempControl = 0;
int thresholdLevel = 0;
int desiredTemp = 80;

void fanOn() {
  WiFiClient client;
  if (client.connect(server, httpPort)) {  
    Serial.println("Turning fans on");
//    Serial.println("Connected");
    client.println("GET /fans?fans=\"on\" HTTP/1.1");
    client.println();
  }
}

void fanOff() {
  WiFiClient client;
  if (client.connect(server, httpPort)) {
    Serial.println("Turning fans off");
//    Serial.println("Connected");
    client.println("GET /fans?fans=\"off\" HTTP/1.1");
    client.println();
  }
}

void recordTemperature(int temp) {
  WiFiClient client;

  String url = "GET /temp?temp1=";
  url += temp;

  if (client.connect(server, httpPort)) {
//    Serial.println("Connected");
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

  // for changing the tempcontrol and desiredtemp settings, need to host website
  localserver.on("/", root);
  localserver.on("/tempcontrol", tempcontrol);
  localserver.on("/settemp", settemp);
  localserver.on("/setthreshold", setthreshold);
  localserver.onNotFound(root);
  localserver.begin();
  Serial.println("HTTP server started");
}

// declarations for pages 
void root() {
  localserver.send(200, "text/plain", "On tempController root page");
}

void tempcontrol() {
  String sendStr = "Setting tempControl to ";

  if (localserver.hasArg("status")) {
    tempControl = localserver.arg("status").toInt();
    sendStr += localserver.arg("status").toInt();
  }

  localserver.send(200, "text/plain", sendStr);
}

void settemp() {
  String sendStr = "Setting desired temperature to ";

  if (localserver.hasArg("temp")) {
    tempControl = localserver.arg("temp").toInt();
    sendStr += localserver.arg("temp").toInt();
  }

  desiredTemp = tempControl;

  localserver.send(200, "text/plain", sendStr);
}

void setthreshold() {
    String sendStr = "Setting threshold to ";

    if(localserver.hasArg("threshold")) {
        thresholdLevel = localserver.arg("threshold").toInt();
        sendStr += localserver.arg("threshold").toInt();
    }

    localserver.send(200, "text/plain", sendStr);
}

void smartdelay(int t) {
  for(int i = 0; i < t; i++) {
//    Serial.println("Handling client");
    localserver.handleClient(); // will finish current effect, but at least update the webpage accordingly
    delay(1); 
  }
}

void loop() {
  int reading = analogRead(sensor); //needs 5V input not 3.3V
  float temperatureC = (double)reading / 1024;
  temperatureC = temperatureC * 5;
  temperatureC = temperatureC - .5;
  temperatureC = temperatureC * 100;
  Serial.print(temperatureC);
  Serial.println(" degrees C");
  
  Serial.println(desiredTemp);

  // control fan if needed
  if (tempControl) {
    if (temperatureC > (desiredTemp + thresholdLevel)) {
      fanOn();
    }
    else if (temperatureC < (desiredTemp - thresholdLevel)){
      fanOff();
    }
  }

  // fanOn();
  recordTemperature(temperatureC);
  smartdelay(300000);
}
