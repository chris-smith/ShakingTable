/*
  This code is meant to be loaded on an Arduino based HR monitor for use with
  the Shaking Table @Boston Children's Hospital by Jason Kahn
  
  HR monitor has 2 functions
    - Measure and Report HR and HR Variability
    - Indicate User by color -- currently uses shiftbrite for this
  
  ----REQUIRED----
  You need to install ShiftBrite.h in your Arduino Libraries
  Shiftbrite Library found at github.com/chris-smith/ShiftBrite
 
*/

#include <SoftwareSerial.h>
#include "ShiftBrite.h"

//    XBEE VARS
SoftwareSerial xbee(2, 5); // RX, TX
//These variables are initialized in setup()
String listenTo;     //  the only ID this xbee will respond to
String slaveID;      //  this xbee's unique ID
long timeout;        //  time spent waiting for message from listenTo
boolean registered;  //  tracks whether this slave is registered with master


char c = 'A';
int  pingPong = 1;
String msg_rcv;
ShiftBrite shift(1);                //declare a shiftbrite system. HR only has 1 shiftbrite
Color color = {"",0,0,0};

int pulsePin = A0;                  // Signal wire connected to analog pin 0
int blinkPin = 13;                  // pin to blink led at each beat
int fadePin = 5;                    // pin to do fancy classy fading blink at each beat
int fadeRate = 0;                   // used to fade LED on with PWM on fadePin
int openAPin = A5;                  // set this to any open analog pin. Used to seed random number

//interrupt variables. volatile because they hold data during interrupt service routine
volatile int BPM;                   // used to hold the pulse rate
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // holds the time between beats, the Inter-Beat Interval
volatile int HRV;                   // holds info about heart rate variability
volatile boolean Pulse = false;     // true when pulse wave is high, false when it's low
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.

void setup()  {
   // Serial used for debugging -- interferes with XBEE
   //Serial.begin(115200);
   //Serial.println( "Arduino started sending bytes via XBee" );

   // set the data rate for the SoftwareSerial port -- Need to talk FAST
   xbee.begin( 57600 );
   // HR samples at 500Hz -- ensured by hardware interrupt
   interruptSetup();
   // This Xbee is a slaved to the table. Will get commands from it
   listenTo = "table";
   slaveID = "";
   
   // used for assigning random slaveID upon register
   randomSeed(analogRead(openAPin));
   
   // timeout used when waiting for Xbee message
   timeout = 5000;
   registered = false;
   
   // set shiftbrite to be off, until HR is registered with table
   shift.turnOff(0);
}

void loop()  
{  
  // Get msg
  msg_rcv = waitForXbee();
  //xbee.println(msg_rcv); // echo message for debugging
  
  // Received Message handler
  handleMsg(msg_rcv);
  
  //if receives no relevant msgs for some time, implement reset
  
  delay(20);
}


String assignUniqueID(){
  // Determines a unique ID for this HR monitor
  long rand = random(5E6); //max str length is 6
  String id = String(rand, HEX);
  while (id.length() < 6){
    id = '0' + id; //pad front of str with zeros if needed
  }
  return id;
}
