const int motor1Pin = 3;    // H-bridge leg 1 (pin 2, 1A)
const int motor2Pin = 4;    // H-bridge leg 2 (pin 7, 2A)
const int enablePin = 9;    // H-bridge enable pin
int power = 0;

void setup() {
  pinMode(motor1Pin, OUTPUT);
  pinMode(motor2Pin, OUTPUT);
//  pinMode(enablePin, OUTPUT);
  
  // set enablePin high so that motor can turn on:
//  digitalWrite(enablePin, HIGH); 
  analogWrite(enablePin, 80);
}

void loop() {
  power = map(analogRead(A0), 0, 1024, 0, 240); 
  analogWrite(enablePin, power);
  digitalWrite(motor1Pin, LOW);   // set leg 1 of the H-bridge low
  digitalWrite(motor2Pin, HIGH);  // set leg 2 of the H-bridge high
}
