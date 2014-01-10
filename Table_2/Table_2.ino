/*

    This is the main code used to run the Shaking Table
    @Boston Children's Hospital by Jason Kahn
    Mostly setup to communicate with HR's at this point

*/

#include <ShiftBrite.h>
#include <SoftwareSerial.h>
#include "ShiftRegister.h"

// ShiftBrite and ShiftRegister libraries only work
// with up to 4 wired in series, limits concurrent table users
#define maxUsers 4

String msg_rcv;

// Specifies user
ShiftBrite shiftbrite(4);
// Display's user's Emotional State
ShiftRegister shift_register(4);

//    XBEE VARS
SoftwareSerial xbee(2,5); // RX, TX
//These variables are initialized in setup()
String listenTo;     //  the ID this xbee will listen to for commands rather than
                     //    confirmations
String slaveID;      //  this xbee's unique ID
long timeout;        //  time spent waiting for message from listenTo
boolean registered;  //  tracks whether this slave is registered with master


// Tracks user data
int numUsers;
int heart_rates[maxUsers];    // holds heart rate for each HR
int thresholds[maxUsers];     // holds threshold for each HR
int levels[maxUsers];         // holds light indicator level for each HR
boolean flashing[maxUsers];   // determines whether to flash lights (if HR > thresh)
String ids[maxUsers];         // holds ids for each HR
String colors[maxUsers];      // holds colors for each HR

// debug
boolean ascend;      // for testing shift register output

void setup()
{
  // Start XBee
  xbee.begin(57600);
  xbee.println("starting");
  
  //  no HR's registered at start
  numUsers = 0;
  init_arrays();
  
  slaveID = "table";   // Table's identifier
  listenTo = "master"; // This is the ipad app
  timeout = 500;
  ascend = true;
  // shiftbrite.setColor(3,"red"); // debug 
}

void init_arrays()
{
  // intializes user data arrays
  for(int i = 0; i < maxUsers; i++){
   heart_rates[i] = 85; 
   thresholds[i] = 100;
   levels[i] = 0;
   flashing[i] = false;
   ids[i] = "";
   colors[i] = "";
  }
}

void loop()
{
  // check for new HR monitors
  newHRMonitors();
  // Ask for HR Values
  queryHeartRates();
  // Set indicator Light Levels
  setOutputs();
  // shiftbrite.setColor(3,"red");
  
  // Send Master user data, get commands
  // talking with master may need to be implemented differently
  talkToMaster();
  
  // msg_rcv = readXbee();
  // handleMsg(msg_rcv);
  delay(20);
}

boolean isValidID(String id)
{
  // checks if id matches with those registered with the table
  for(int i = 0; i < numUsers; i++){
   if(id == ids[i])
    return true;
  }
  return false; 
}

void setOutputs()
{
  //set light levels after querying heart rates
  //levels set relative to individual thresholds
  
  /*             CAUTION!!!
  **  Setting the shift register outputs
  **  may change output for the shiftbrite
  **  Reset shiftbrite after this function ends
  **    FIGURE OUT WHY THIS HAPPENS
  ***********************************************/
  double level;
  for (int i = 0; i < numUsers; i++)
  {
    // for each user, set ShiftRegister
    //Serial.print("HR: "); Serial.println(heart_rates[i]);
    //Serial.print("Thresh: "); Serial.println(thresholds[i]);
    int dif = heart_rates[i] - thresholds[i];
    if (dif >= 0){
      // over threshold
      flashing[i] = !flashing[i];
      if (dif > 10){
        // very high
        level = 6;
      }
      else if (dif > 5){
        // a little high
        level = 5;
      }
      else{
        // 0 <= dif < 5
        level = 4;
      }
    }
    else{
      // below threshold
      flashing[i] = false;
      if (dif < -10){
         // far below threshold
         level = 1;
      }
      else if (dif < -5){
        // a little below threshold
        level = 2;
      }
      else{
        // 0 > dif >= -5
        level = 3;
      }
    }
    boolean on = true;
    //Serial.print("Thresh: "); Serial.println(level);
    if (level > 3 && !flashing[i]){
      //Serial.println("FLASH");
      on = false;
    }
      
    for (int j = 0; j < 7; j++)
    {
      // set lights
      if ( j < level)
        shift_register.setRegisterPin(7*i + j, on);
      else
        shift_register.setRegisterPin(7*i + j, LOW);
    }
    
    /* 
    // Testing that Shift Registers work
    if (ascend){
      heart_rates[i]++;
      if (heart_rates[i] >= 115)
        ascend = false;
    }
    else{
      heart_rates[i]--;
      if (heart_rates[i] <= 85)
        ascend = true;
    }*/
  }
  
  // Tell shift registers to adjust their values
  shift_register.writeRegisters();
}
