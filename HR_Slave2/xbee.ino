/* THIS CONTAINS XBEE IMPLEMENTATION FOR THE HR SLAVE

IN SOME INSTANCES, MULTIPLE CALL/RESPONSE
ARE MADE FOR SAME COMMAND IN ORDER TO CUT
DOWN ON MESSAGE LENGTH FOR HR SLAVES

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
  //xbee.println("register");
  //msg is "" if asking for new HR's
  //otherwise msg is confirming slaveID for another HR
  if(registered || (msg != ""))
    return;
  //xbee.println("continue");
  slaveID = assignUniqueID();
  color = shift.getColor(); //get this color from ShiftBrite in future
  color = setName(color);
  slaveID = "12465";
  String reply = "R-"+slaveID+"-"+color.name;
  xbee.println(reply);
  msg = waitForXbee();
  String confirmedID = getToken(msg, 2);
  if (confirmedID == slaveID)
  {
    registered = true;
    shift.setColor(0, color);
  }
}

void handleHeartRate(String msg)
{
  if (msg != slaveID)
    return;
  String reply = "H-" + slaveID + "-" + byteLen(BPM);
  xbee.println(reply);
}

void handleVariability(String msg)
{
  if (msg != slaveID)
    return;
  String reply = "V-" + slaveID + "-" + byteLen(HRV);
  xbee.println(reply);
}

void handleColor(String msg)
{
  if (msg != slaveID)
    return;
  //Need to reply to ask for color
  String reply = "C-"+ slaveID + "-";
  xbee.println(reply);
  msg = waitForXbee();
  //msg reply is slaveID-sender-color
  String id = getToken(msg, 0);
  if(id != slaveID)
    return;
  String color = getToken(msg, 2);
  Color col = stringToRGB(color);
  shift.setColor(0,col);
}

void handleMsg(String msg)
{
  char code = getToken(msg, 0).charAt(0);
  String data = getToken(msg, 2);
  String reply = "";
  switch(code)
  {
    case 'R':
      //reply = "registered with " + assignUniqueID();
      handleRegister(data);
      break;
    case 'H':
      //reply = "here's my heart rate: " + data;
      handleHeartRate(data);
      break;
    case 'C':
      //reply = "changing my color to " + data;
      handleColor(data);
      break;
    case 'V':
      //reply = "here's my heart rate variability" + data;
      handleVariability(data);
    default:
      reply = "";
      break;
  }
  if(reply != "")
    xbee.println(reply);
}

String waitForXbee()
{
  // ENSURES MESSAGE IS FROM SOMEBODY IT WANTS TO LISTEN TO
  //waits until it a message for this xbee is received
  //returns message
  long start = millis();
  String msg;
  String sender;
  while(millis() - start < timeout)
  {
    msg = readXbee();
    sender = getToken(msg, 1); // msg format is commandChar-sender-data
    if (sender == listenTo)
      return msg;
  }
  return "TIMEOUT";
}

String readXbee(){
  String msg = "";
  boolean breakRead = false;
  String err = "";
  while (xbee.available() > 0){
    c = xbee.read();
    //Serial.print("character: ");
    //Serial.println(c);
    delay(1);
    switch(c){
      case '\n':
        breakRead = true;
        msg += "new line";
        break;
      case -1:
        breakRead = true;
        msg = "No termination char (\\n)"; //DO SOMETHING WITH THIS??
        break;
      default:
        msg += c;
        break;
    }
    //msg_rcv += c;
    if(breakRead){
      break;
    }
  }
  //Serial.println("xbee done");
  return msg;
}
