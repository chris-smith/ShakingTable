// Shaky table with back and forth motion. The sketch initially looks for motor
// power from Serial.read() then defaults to a potentiometer plugged into A0. 
// Motion is moderated by a feedback control system that becomes grounded on 
// either side whenever the tabletop touches a wall.

const int Lmotor1Pin = 3;    // H-bridge leg 1 (pin 2, 1A)
const int Lmotor2Pin = 4;    // H-bridge leg 2 (pin 7, 2A)
const int LenablePin = 9;    // H-bridge left enable pin
const int Rmotor1Pin = 5;    // H-bridge leg 1 (pin 2, 1A)
const int Rmotor2Pin = 6;    // H-bridge leg 2 (pin 7, 2A)
const int RenablePin = 10;    // H-bridge enable pin
const int RATE = 1;
// wait this many milliseconds after Serial input stops before reverting to A0 (pot)
const int WAIT_FOR_STOP = 3000;  
// wait this many milliseconds before automatically switching motor direction
const int SWITCH_DIRECTION = 1000;

int power;
boolean forward;
unsigned long start_pulse;
unsigned long last_input;
int input;
int threshold;

void setup() {
  
  pinMode(Lmotor1Pin, OUTPUT);
  pinMode(Lmotor2Pin, OUTPUT);
  pinMode(Rmotor1Pin, OUTPUT);
  pinMode(Rmotor2Pin, OUTPUT);
  
  forward = true;
  last_input = 0;
  
  // threshold is the cutoff between a HIGH reading and a ground reading for
  // the control strips. This has been a little sketchy in the past; eventually
  // we should come up with a better system or a way to keep the threshold up to
  // date
  threshold = 900;
  Serial.begin(9600);
}

void loop() {
  
  input = Serial.read();
  if(input != -1) {
    power = input;
    last_input = millis();
  } else if (millis() - last_input > WAIT_FOR_STOP) {
    power = map(analogRead(A0), 0, 1024, 0, 150);
  }
    
  analogWrite(RenablePin, power);
  analogWrite(LenablePin, power);
  
  Serial.print("power: "); Serial.print(power);
  Serial.print("    A1 reading: "); Serial.print(analogRead(A1));
  Serial.print("    A2 reading: "); Serial.println(analogRead(A2));
  
  start_pulse = millis();
  if(forward) {
    while(analogRead(A1) > threshold && (millis() - start_pulse) < SWITCH_DIRECTION) {
      digitalWrite(Lmotor1Pin, HIGH);   // set leg 1 of the H-bridge low
      digitalWrite(Lmotor2Pin, LOW);  // set leg 2 of the H-bridge high
      digitalWrite(Rmotor1Pin, HIGH);   // set leg 1 of the H-bridge low
      digitalWrite(Rmotor2Pin, LOW);  // set leg 2 of the H-bridge high
    }
    digitalWrite(RenablePin, 0);
    digitalWrite(LenablePin, 0);
  } else {
    while(analogRead(A2) > threshold && (millis() - start_pulse) < SWITCH_DIRECTION) {
      digitalWrite(Lmotor1Pin, LOW);   // set leg 1 of the H-bridge low
      digitalWrite(Lmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
      digitalWrite(Rmotor1Pin, LOW);   // set leg 1 of the H-bridge low
      digitalWrite(Rmotor2Pin, HIGH);  // set leg 2 of the H-bridge high
    }
    digitalWrite(RenablePin, 0);
    digitalWrite(LenablePin, 0);
  } 
  forward = !forward;
}

