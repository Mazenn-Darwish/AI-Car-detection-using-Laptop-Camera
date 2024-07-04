#include <Servo.h>

Servo myServo;
const int servoPin = 10;
const int trigPin = 8;
const int echoPin = 9;
const int gopen = 120; 
const int gclose = -10;
const long timeout = 10000;  

void setup() {
  myServo.attach(servoPin); // pin 10
  myServo.write(gclose);  
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'a') {
      myServo.write(gopen);  
    } else if (command == 'b') {
      myServo.write(gclose);  
    } else if (command == 'c') {
      checkGarageStatus();
    }
  }
}

void checkGarageStatus() {
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH, timeout);
  distance = (duration / 2) / 29.1;  // Calculate the distance in cm

  if (distance < 5) {  // Adjust the threshold distance as needed
    Serial.println("full");
  } else {
    Serial.println("empty");
  }
}