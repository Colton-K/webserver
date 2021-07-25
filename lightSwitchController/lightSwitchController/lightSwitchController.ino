// webserver vars
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define WIFI_SSID "thinkAP"
#define WIFI_PASS "penguinPinapplePizza"
ESP8266WebServer server(80);

// servo vars
#include <Servo.h>
//#define OFFSET -6
#define OFFSET -15

//#define SERVOPIN 14 // D5
#define SERVOPIN 4

Servo myservo;
void turnLightsOff();
void turnLightsOn();

/* 
 * Main Program code
 */
void setup() {
  Serial.begin(115200);
  Serial.println("Starting up....");

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);

  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("My IP: ");
  Serial.println(WiFi.localIP());  

  server.on("/", root);
  server.on("/switch", lightSwitch);
  server.onNotFound(notFound);
  server.begin();
  Serial.println("HTTP server started");

  // servo
  myservo.attach(SERVOPIN);
}

void root() {
  server.send(200, "text/plain", "On root page");
  
}

void lightSwitch() {
  if(server.hasArg("light")) {
    if(server.arg("light").toInt() == 0) {
      turnLightsOff();
      server.send(200, "text/plain", "Turning lights off");
    }
    else {
      turnLightsOn();
      server.send(200, "text/plain", "Turning lights on");
    }
  }
  
  server.send(200, "text/plain", "Starting switch page!");

}

void notFound() {
  server.send(200, "text/plain", "request not available");
}

void loop() {
  server.handleClient();
}

void turnLightsOff() {
  Serial.println("turning lights off");
//  move down
  myservo.write(30+OFFSET);
  delay(500);
// move center
  myservo.write(90+OFFSET);
  delay(500);
}

void turnLightsOn() {
  Serial.println("turning lights on");
// move up
  myservo.write(160+OFFSET);
  delay(500);
// move center
  myservo.write(90+OFFSET);
  delay(500);
}
