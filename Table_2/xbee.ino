/* THIS CONTAINS XBEE IMPLEMENTATION FOR THE TABLE

    IN SOME INSTANCES, MULTIPLE CALL/RESPONSE
    ARE MADE FOR SAME COMMAND IN ORDER TO CUT
    DOWN ON MESSAGE LENGTH FOR HR SLAVES
        Messages need to be sent fast enough to ensure they aren't 
        interrupted by HR sampling interrupt, causes garbled message
        Xbee currently talks at 57600 -- if you get 115200 to be stable, it
        may be possible to change this.

Functions:
  handleRegister() - called when register request is received from master
  handleHeartRate() - called when heartrate request is received from master
  handleColor() - called when color change request is received from master
  
  handleMsg() - processes received messages and makes callbacks to appropriate handlers
  
  waitForXbee() - waits for a reply to a command. will timeout 
  readXbee() - reads characters at xbee until termination char (\n) or until
                xbee is empty. does not timeout.
*/

void newHRMonitors()
{
  // looks for new HR monitors
  
  // if we can add more users
  if(numUsers < maxUsers)
  {
    // format request message -- "R-table-"
    String msg = "R-"+slaveID+"-";
    xbee.println(msg);
    // wait for a reply
    msg = waitForXbee('R');
    if (msg != "TIMEOUT"){
      // get the id of the HR monitor
      String id = getToken(msg, 1);
      // check if duplicate id
      if ( !isValidID(id) ){
        // get color of HR monitor
        String color = getToken(msg, 2);
        ids[numUsers] = id;
        colors[numUsers] = color;
        
        // this shouldn't do anything anymore
        //int* rgb = stringToRGB(color);
        
        // increment number of users
        numUsers++;
      }
    }
  }
}

void queryHeartRates()
{
  // asks registered HR monitors for their HR data
  String msg;
  int bpm;
  for(int i = 0; i < numUsers; i++)
  {
    // format message -- "H-table-hr_id"
    msg = "H-"+slaveID+"-"+ids[i];
    xbee.println(msg);
    // wait for reply
    msg = waitForXbee('H');
    // get id of sender
    String id = getToken(msg, 1);
    if (id == ids[i])
    {
      // if the right HR monitor replied, set heart_rate data
      heart_rates[i] = getToken(msg, 2).toInt();
    }
  }
}

void talkToMaster()
{
   // Message to master is formatted
   // M-table-numUsers-id-color-hr-thresh-id-color-hr-thresh-...
   
   // Format message
   String msg = "M-" + slaveID + "-" + byteLen(numUsers);
   for(int i = 0; i < numUsers; i++){
    msg += "-" +ids[i] + "-" + colors[i] + "-";
    msg += byteLen(heart_rates[i]) + "-" + byteLen(thresholds[i]);
   }
   xbee.println(msg);
   // wait for reply from master 
   //  - message can be long since no hardware interrupts
   // formatted as "M-master-commandCode-slaveId-msg"
   msg = waitForXbee('M');
   String id = getToken(msg, 1);
   if (id == "master")
   {
     // get the rest of the message
     msg = getTokenToEnd(msg, 2); 
     handleMsg(msg);
   }
}

void handleColor(String msg)
{ /*
    Color message needs to be broken into two parts when communicating with
    HR monitor due to interrupts on HR -- otherwise it's too long
    Message from Master is C-slaveId-color
    Message to HR monitor is C-table-slaveId
    HR monitor with slaveId responds C-slaveId-
    2nd message to HR is slaveId-table-color
    
    color is string formatted from struct Color as seen in strings.ino
  ****************************************************************************/
  // msg is "hr_id-colorString"
  String id = getToken(msg, 0);
  if(!isValidID(id))
    return;
  // get color
  String color = getToken(msg, 1);
  // format message to send
  //  "C-table-hr_id"
  msg = "C-"+slaveID+"-"+id;
  // send message
  xbee.println(msg);
  // wait for reply
  // msg should look like "C-sender-"
  msg = waitForXbee('C');
  
  // check that reply is from correct HR
  if(id != getToken(msg, 1))
    return;
  
  // respond with new color
  //  msg format is "hr_id-table-colorString"
  msg = id+"-"+slaveID+"-"+color;
  xbee.println(msg);
}

void handleMsg(String msg)
{
  // Message handler for table 
  //  should only be called for messages from Master
  char code = getToken(msg, 0).charAt(0);
  String id = getToken(msg, 1);
  String data = getTokenToEnd(msg, 1);
  String reply = "";
  // only called if msg is from master
  switch(code)
  {
    /*  These not implemented
    case 'U':
      // Unregister HR monitor
      break;
    case 'T':
      // Change threshold for HR monitor
      break;
    */
    // Should add case for Master asking to unregister HR monitor
    case 'C':
      // Change color
      handleColor(data);
      break;
    default:
      reply = "";
      break;
  }
  
  // I don't think I need this anymore
  if(reply != "")
    xbee.println(reply);
}

String waitForXbee(char code)
{
  // waits until a response for the code is received
  // returns message
  long start = millis();
  String msg;
  String sender;
  while(millis() - start < timeout)
  {
    msg = readXbee();
    char rcv = getToken(msg, 0).charAt(0); // msg format is commandChar-sender-data
    if (code == rcv)
      return msg;
  }
  return "TIMEOUT";
}

String readXbee(){
  //  Reads and returns message at Xbee port
  //  Messages should terminate should newline -- '\n'
  String msg = "";
  boolean breakRead = false;
  String err = "";
  char c;
  // if there is something at the xbee's port, read it
  while (xbee.available() > 0){
    // get the next character
    c = xbee.read();
    delay(1);
    switch(c){
      case '\n':
        // message termination
        breakRead = true;
        msg += "new line";
        break;
      case -1:
        // Nothing at port anymore, but message was never terminated
        breakRead = true;
        msg = "No termination char (\\n)"; //DO SOMETHING WITH THIS??
        break;
      default:
        // character is part of message
        msg += c;
        break;
    }
    // if message is done, stop reading
    if(breakRead){
      break;
    }
  }
  return msg;
}
