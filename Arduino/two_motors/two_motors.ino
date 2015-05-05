const int Lmotor1Pin = 3;    // H-bridge leg 1 (pin 2, 1A)
const int Lmotor2Pin = 4;    // H-bridge leg 2 (pin 7, 2A)
const int LenablePin = 9;    // H-bridge left enable pin
const int Rmotor1Pin = 5;    // H-bridge leg 1 (pin 2, 1A)
const int Rmotor2Pin = 6;    // H-bridge leg 2 (pin 7, 2A)
const int RenablePin = 10;    // H-bridge enable pin
int Lpower = 0;
int Rpower = 0;

void setup() {
  pinMode(Lmotor1Pin, OUTPUT);
  pinMode(Lmotor2Pin, OUTPUT);
  pinMode(Rmotor1Pin, OUTPUT);
  pinMode(Rmotor2Pin, OUTPUT);
//  pinMode(LenablePin, OUTPUT);
//  pinMode(RenablePin, OUTPUT);
  
  // set enablePin high so that motor can turn on:
//  digitalWrite(enablePin, HIGH); 
//  analogWrite(enablePin, 80);
}

void loop() {
  Lpower = map(analogRead(A0), 0, 1024, 0, 80);
  Rpower = map(analogRead(A1), 0, 1024, 0, 80);
  analogWrite(LenablePin, Lpower);
  digitalWrite(Lmotor1Pin, LOW);   // set leg 1 of the H-bridge low
  digitalWrite(Lmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
  analogWrite(RenablePin, Rpower);
  digitalWrite(Rmotor1Pin, LOW);   // set leg 1 of the H-bridge low
  digitalWrite(Rmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
}
