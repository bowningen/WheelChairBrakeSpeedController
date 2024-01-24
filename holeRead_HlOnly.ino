#include <stdio.h>
#include <stdlib.h>

double value;
double value2;

void setup() {
  // put your setup code here, to run once:
  pinMode(14,OUTPUT);
  pinMode(15,OUTPUT);
  pinMode(A2,INPUT);
  pinMode(A3,INPUT);
  Serial.begin(115200);
  value = 0.0;
  value2 = 0.0;
  digitalWrite(14,HIGH);
  digitalWrite(15,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long time;
  value = analogRead(A2);
  value2 = analogRead(A3);
  value *= 1.0 * 5.0 / 1024;
  value2 *= 1.0 * 5.0 / 1024;
  time = millis();
  Serial.println(time);
  Serial.println(value);
  Serial.println(value2);
}
