#include <DFRobot_DHT11.h>

DFRobot_DHT11 DHT;

const int buzzerPin = 13;
const int redLedPin = 4;

#define DHT11_PIN 2

void setup() {
  Serial.begin(9600);
  pinMode(redLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  DHT.read(DHT11_PIN);
  Serial.print("temp: ");
  Serial.println(DHT.temperature);

  if (Serial.available() > 0) { //시리얼 버퍼 존재
    char command = Serial.read();

    if (command == 's') { //파이썬에서 s가 버퍼로 전송
      digitalWrite(redLedPin, HIGH); //부저 & LED ON
      tone(buzzerPin, 1000);
      delay(3000);
      noTone(buzzerPin);
      digitalWrite(redLedPin, LOW);
    }
  }
  delay(50);
}
