#include <Servo.h>    // サーボライブラリ
#include <stdio.h>
#include <stdlib.h>

Servo servoL;        // サーボオブジェクト
Servo servoR;


int SL;
int SR;

int cL;
int cR;

int e2;
int e3;
int ret;
int p;

void setup() {
  servoL.attach(16);
  servoR.attach(15);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    //cutting
    int N[8];
    for (int i = 0; i < 8; i++) {
      N[i] = (int)(data[i] - '0');
    }

    SL = N[3];
    e2 = N[2];
    e3 = N[1];
    SL = SL + (e2 * 10) + (e3 * 100);
    SR = N[7];
    e2 = N[6];
    e3 = N[5];
    SR = SR + (e2 * 10) + (e3 * 100);
    
  }
    
  
    
  servoL.write(SL);
  servoR.write(SR);
  Serial.println("R");
  delay( 50 );
}
