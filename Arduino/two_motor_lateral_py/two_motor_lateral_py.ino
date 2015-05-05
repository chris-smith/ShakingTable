const int Lmotor1Pin = 3;    // H-bridge leg 1 (pin 2, 1A)
const int Lmotor2Pin = 4;    // H-bridge leg 2 (pin 7, 2A)
const int LenablePin = 9;    // H-bridge left enable pin
const int Rmotor1Pin = 5;    // H-bridge leg 1 (pin 2, 1A)
const int Rmotor2Pin = 6;    // H-bridge leg 2 (pin 7, 2A)
const int RenablePin = 10;    // H-bridge enable pin
const int RATE = 1;
unsigned int power;
int input;
boolean clockwise;

void setup() {
  
  pinMode(Lmotor1Pin, OUTPUT);
  pinMode(Lmotor2Pin, OUTPUT);
  pinMode(Rmotor1Pin, OUTPUT);
  pinMode(Rmotor2Pin, OUTPUT);
  
  clockwise = true;
  input = -1;
  power = 0;
  Serial.begin(9600);
//  pinMode(LenablePin, OUTPUT);
//  pinMode(RenablePin, OUTPUT);
  
  // set enablePin high so that motor can turn on:
//  digitalWrite(enablePin, HIGH); 
//  analogWrite(enablePin, 80);
}

void loop() {
  power = map(analogRead(A0), 0, 1024, 0, 100);
  input = Serial.read();
  if(input != -1) {
    power = input;
  }
//  analogWrite(LenablePin, power);
  analogWrite(RenablePin, power);
  analogWrite(LenablePin, power);
  Serial.print("power: "); Serial.println(power);
  
  if(clockwise) {
    Serial.println("forward!");
    digitalWrite(Lmotor1Pin, HIGH);   // set leg 1 of the H-bridge low
    digitalWrite(Lmotor2Pin, LOW);  // set leg 2 of the H-bridge high
    digitalWrite(Rmotor1Pin, HIGH);   // set leg 1 of the H-bridge low
    digitalWrite(Rmotor2Pin, LOW);  // set leg 2 of the H-bridge high
  } else {
    digitalWrite(Lmotor1Pin, LOW);   // set leg 1 of the H-bridge low
    digitalWrite(Lmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
    digitalWrite(Rmotor1Pin, LOW);   // set leg 1 of the H-bridge low
    digitalWrite(Rmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
  } 
  delay(1000);
  clockwise = !clockwise;
}

