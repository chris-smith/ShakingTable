/* THIS CONTAINS XBEE IMPLEMENTATION FOR THE HR SLAVE

  IN SOME INSTANCES, MULTIPLE CALL/RESPONSE
  ARE MADE FOR SAME COMMAND IN ORDER TO CUT
  DOWN ON MESSAGE LENGTH
      Messages need to be sent fast enough to ensure they aren't 
      interrupted by HR sampling interrupt, causes garbled message
      Xbee currently talks at 57600 -- if you get 115200 to be stable, it
      may be possible to change this. 
      
  
  Messaging format is generally "c-sender-msg" where
    c = command code
    sender = ID of message sender
    msg = contains further information

Functions:
  handleRegister() - called when register request is received from master
  handleHeartRate() - called when heartrate request is received from master
  handleVariability() - called when variability data is requested by master
  handleColor() - called when color change request is received from master
  
  handleMsg() - processes received messages and makes callbacks to appropriate handlers
  
  waitForXbee() - waits for a message from master. will timeout 
  readXbee() - reads characters at xbee until termination char (\n) or until
                xbee is empty. does not timeout.
*/


void handleRegister(String msg)
{
  // Table has asked for new HR monitors, or is confirming registration
  
  // msg is "" if asking for new HR's
  // otherwise msg is confirming slaveID for another HR
  // Don't do anything if registered or if message is confirming registration
  if(registered || (msg != ""))
    return;
  // get a slaveID for identification with table
  slaveID = assignUniqueID();
  // Get a color to identify HR monitor
  color = shift.getColor(); 
  color = setName(color);
  // slaveID = "12465";  // debugging
  
  //Format reply message
  String reply = "R-"+slaveID+"-"+color.name;
  xbee.println(reply);
  // wait for confirmation
  msg = waitForXbee();
  // get confirmed id
  String confirmedID = getToken(msg, 2);
  if (confirmedID == slaveID)
  {
    // Table has confirmed this HR's registration
    registered = true;
    shift.setColor(0, color);
  }
}

void handleHeartRate(String msg)
{
  // Table has asked for HR data
  
  // check if message is for you
  if (msg != slaveID)
    return;
  
  // format reply
  String reply = "H-" + slaveID + "-" + byteLen(BPM);
  xbee.println(reply);
}

void handleVariability(String msg)
{
  // Table has asked for HR Variability data
  
  // check if message is for you
  if (msg != slaveID)
    return;
  
  // format reply
  String reply = "V-" + slaveID + "-" + byteLen(HRV);
  xbee.println(reply);
}

void handleColor(String msg)
{
  // Table wants to change HR's color
  
  // check if message is for you
  if (msg != slaveID)
    return;
    
  //Need to reply to ask for color due to message length
  String reply = "C-"+ slaveID + "-";
  xbee.println(reply);
  msg = waitForXbee();
  //msg reply format is slaveID-sender-color
  String id = getToken(msg, 0);
  
  // this check is probably unnecessary
  if(id != slaveID)
    return;
  
  // Set Color to new value
  String color = getToken(msg, 2);
  Color col = stringToRGB(color);
  shift.setColor(0,col);
}

void handleMsg(String msg)
{
  // Generic Message Handler
  
  // get command code
  char code = getToken(msg, 0).charAt(0);
  // get message
  String data = getToken(msg, 2);
  String reply = "";
  switch(code)
  {
    case 'R':
      // Register
      handleRegister(data);
      break;
    case 'H':
      // HR Data
      handleHeartRate(data);
      break;
    case 'C':
      // Color Change
      handleColor(data);
      break;
    case 'V':
      // HR Variability Data
      handleVariability(data);
      break;
    default:
      // unknown command - do nothing
      reply = "";
      break;
  }
  
  // I don't think I need this anymore
  if(reply != "")
    xbee.println(reply);
}

String waitForXbee()
{
  // Waits for a message from somebody it has been told to listen to
  //   listenTo was set in setup() to "table"
  //waits until a message for this xbee is received
  //returns message
  long start = millis();
  String msg;
  String sender;
  while(millis() - start < timeout)
  {
    // read message from Xbee
    msg = readXbee();
    // Check the sender
    sender = getToken(msg, 1); // msg format is commandChar-sender-data
    // if you've been told to listen to this sender, return message
    if (sender == listenTo)
      return msg;
  }
  // if you didn't get a relevant message in time
  return "TIMEOUT";
}

String readXbee(){
  //  Reads and returns message at Xbee port
  //  Messages should terminate should newline -- '\n'
  String msg = "";
  boolean breakRead = false;
  String err = "";
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
