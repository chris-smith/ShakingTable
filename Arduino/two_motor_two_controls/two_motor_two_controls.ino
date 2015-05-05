const int Lmotor1Pin = 3;    // H-bridge leg 1 (pin 2, 1A)
const int Lmotor2Pin = 4;    // H-bridge leg 2 (pin 7, 2A)
const int LenablePin = 9;    // H-bridge left enable pin
const int Rmotor1Pin = 5;    // H-bridge leg 1 (pin 2, 1A)
const int Rmotor2Pin = 6;    // H-bridge leg 2 (pin 7, 2A)
const int RenablePin = 10;    // H-bridge enable pin
const int RATE = 1;
const int statusLED = 7;
const int CutoffVoltage = 700;
unsigned int power;
unsigned int pause;
unsigned int userStatus;
boolean forward;

void setup() {
  
  pinMode(Lmotor1Pin, OUTPUT);
  pinMode(Lmotor2Pin, OUTPUT);
  pinMode(Rmotor1Pin, OUTPUT);
  pinMode(Rmotor2Pin, OUTPUT);
  pinMode(statusLED, OUTPUT);
  
  Serial.begin(9600);
//  pinMode(LenablePin, OUTPUT);
//  pinMode(RenablePin, OUTPUT);
  
  // set enablePin high so that motor can turn on:
//  digitalWrite(enablePin, HIGH); 
//  analogWrite(enablePin, 80);
}

void loop() {
  power = assignPower(analogRead(A0));
  pause = assignPause(power);
  
  analogWrite(RenablePin, power);
  analogWrite(LenablePin, power);
  Serial.print("power: "); Serial.println(power);
  Serial.print("reading 1: "); Serial.println(analogRead(A1));
  Serial.print("reading 2: "); Serial.println(analogRead(A2));
  
  if(analogRead(A1) > CutoffVoltage) {
    while(power > 0 && analogRead(A1) > CutoffVoltage) {
      goBackward();
//      Serial.println(analogRead(A1));
      delay(10);
    }
  } else {
    while(power > 0 && analogRead(A2) > CutoffVoltage) {
      goForward();
//      Serial.println(analogRead(A2));
      delay(10);
    }
  }
  digitalWrite(RenablePin, 0);
  digitalWrite(LenablePin, 0); 
  delay(pause);
}

void goForward() {
  digitalWrite(Lmotor1Pin, HIGH);   // set leg 1 of the H-bridge low
  digitalWrite(Lmotor2Pin, LOW);  // set leg 2 of the H-bridge high
  digitalWrite(Rmotor1Pin, HIGH);   // set leg 1 of the H-bridge low
  digitalWrite(Rmotor2Pin, LOW);  // set leg 2 of the H-bridge high
}

void goBackward() {
  digitalWrite(Lmotor1Pin, LOW);   // set leg 1 of the H-bridge low
  digitalWrite(Lmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
  digitalWrite(Rmotor1Pin, LOW);   // set leg 1 of the H-bridge low
  digitalWrite(Rmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
}

unsigned int assignPower(int power) {
  unsigned int new_power = 0;
  if(power > 768) {
    new_power = 90;
  } else if(power > 512) {
    new_power = 70;
  }
  
  return new_power;
}

unsigned int assignPause(unsigned int power) {
  unsigned int pause = 500;
  
  switch(power) {
    case 80:
      pause = 500;
      break;
    case 70:
      pause = 1000;
  }
  return pause;
}
  
  
