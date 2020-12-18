#include <Servo.h>

Servo lightServo;

void setup() {
  // put your setup code here, to run once:
  lightServo.attach(10);
  lightServo.write(0);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  Serial.println("0");
  lightServo.write(0);
  delay(1000);
  Serial.println("90");
  lightServo.write(90);
  delay(1000);
  Serial.println("180");
  lightServo.write(180);
  delay(1000);
  
}
