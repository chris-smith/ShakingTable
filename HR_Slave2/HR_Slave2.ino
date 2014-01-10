/*
  Xbee1
  D. Thiebaut
  
  Makes Arduino send 1 character via XBee wireless to another XBee connected
  to a computer via a USB cable. 

  The circuit: 
  * RX is digital pin 2 (connect to TX of XBee)
  * TX is digital pin 3 (connect to RX of XBee)
 
  Based on a sketch created back in the mists of time by Tom Igoe
  itself based on Mikal Hart's example
 
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
ShiftBrite shift(1);     //declare a shiftbrite system. Only has 1 shiftbrite
Color color = {"",0,0,0};

int pulsePin = A0;                 // Pulse Sensor purple wire connected to analog pin 0
int blinkPin = 13;                // pin to blink led at each beat
int fadePin = 5;                  // pin to do fancy classy fading blink at each beat
int fadeRate = 0;                 // used to fade LED on with PWM on fadePin
int openAPin = A5;                // set this to any open analog pin. Used to seed random number

//interrupt variables. volatile because they hold data during interrupt service routine
volatile int BPM;                   // used to hold the pulse rate
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // holds the time between beats, the Inter-Beat Interval
volatile int HRV;                   // holds info about heart rate variability
volatile boolean Pulse = false;     // true when pulse wave is high, false when it's low
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.

void setup()  {
   //Serial.begin(115200);
   //Serial.println( "Arduino started sending bytes via XBee" );

   // set the data rate for the SoftwareSerial port
   xbee.begin( 57600 );
   interruptSetup();
   listenTo = "table";
   slaveID = "";
   randomSeed(analogRead(openAPin));
   timeout = 5000;
   registered = false;
   shift.turnOff(0);
}

void loop()  
{  
  msg_rcv = waitForXbee();
  xbee.println(msg_rcv);
  handleMsg(msg_rcv);
  //if receives no relevant msgs for some time, reset
  delay(100);
}

//Unique ID's are 5
String assignUniqueID(){
  long rand = random(5E6); //max str length is 6
  String id = String(rand, HEX);
  while (id.length() < 6){
    id = '0' + id; //pad front of str with zeros if needed
  }
  return id;
}
