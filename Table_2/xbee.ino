/* THIS CONTAINS XBEE IMPLEMENTATION FOR THE TABLE

IN SOME INSTANCES, MULTIPLE CALL/RESPONSE
ARE MADE FOR SAME COMMAND IN ORDER TO CUT
DOWN ON MESSAGE LENGTH FOR HR SLAVES

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
  if(numUsers < maxUsers)
  {
    String msg = "R-"+slaveID+"-";
    xbee.println(msg);
    msg = waitForXbee('R');
    if (msg != "TIMEOUT"){
      String id = getToken(msg, 1);
      if (!isValidID(id)){
        // not a duplicate id
        String color = getToken(msg, 2);
        ids[numUsers] = id;
        colors[numUsers] = color;
        int* rgb = stringToRGB(color);
        numUsers++;
      }
    }
  }
}

void queryHeartRates()
{
  String msg;
  int bpm;
  for(int i = 0; i < numUsers; i++)
  {
    msg = "H-"+slaveID+"-"+ids[i];
    xbee.println(msg);
    msg = waitForXbee('H');
    String id = getToken(msg, 1);
    if (id == ids[i])
    {
      heart_rates[i] = getToken(msg, 2).toInt();
    }
  }
}

void talkToMaster()
{
    // Message to master is formatted
    // M-table-numUsers-id-color-hr-thresh-id-color-hr-thresh-...
   String msg = "M-" + slaveID + "-" + byteLen(numUsers);
   for(int i = 0; i < numUsers; i++){
    msg += "-" +ids[i] + "-" + colors[i] + "-";
    msg += byteLen(heart_rates[i]) + "-" + byteLen(thresholds[i]);
   }
   xbee.println(msg);
   msg = waitForXbee('M');
   String id = getToken(msg, 1);
   if (id == "master")
   {
     msg = getTokenToEnd(msg, 2); 
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
  String id = getToken(msg, 0);
  if(!isValidID(id))
    return;
  String color = getToken(msg, 1);
  msg = "C-"+slaveID+"-"+id;
  xbee.println(msg);
  msg = waitForXbee('C');
  //reply should look like "C-sender-"
  if(id != getToken(msg, 1))
    return;
  msg = id+"-"+slaveID+"-"+color;
  xbee.println(msg);
}

void handleMsg(String msg)
{
  char code = getToken(msg, 0).charAt(0);
  String id = getToken(msg, 1);
  String data = getTokenToEnd(msg, 2);
  String reply = "";
  if(id == listenTo)
  {
    switch(code)
    {
      case 'R':
        //reply = "registered with " + assignUniqueID();
        break;
      case 'H':
        //reply = "here's my heart rate: " + data;
        break;
      case 'C':
        //reply = "changing my color to " + data;
        handleColor(data);
        break;
      default:
        reply = "";
        break;
    }
  }
  if(reply != "")
    xbee.println(reply);
}

String waitForXbee(char code)
{
  //waits until a response for the code is received
  //returns message
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
  String msg = "";
  boolean breakRead = false;
  String err = "";
  char c;
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
