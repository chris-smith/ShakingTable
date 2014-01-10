 /* 

  This code used by xbee.ino for 
      - deserializing messages
      - converting between strings and objects
      - padding strings      
      
 */


// For strings formatted as ___-____-___, returns the numth member
// Zero indexed
//   Example:  getToken("this-is-an-example", 2) returns "an"
String getToken(String msg, const int num)
{
  String token = "";
  int index = -1;
  int to = 0;
  int i = 0;
  while(i <= num)
  {
    index = msg.indexOf("-", 1);
    if (index + i < 0)
    {
      // Error -- I don't think code currently cares if it gets error
      token = "ERROR: No Such Token";
      return token;
    }
    else if(index < 0)
    {
      // Never found a '-' character -- return remaining message
      token = msg;
      return token;
    }
    else if(i == num)
    {
      // This is the token we want
      token = msg.substring(0,index);
      return token;
    }
    // Remove earlier part of message, if not the token we want
    msg = msg.substring(index+1);
    i++;
  }
  return token;
}

//Once the numth token is reached, returns rest of the string
// Ex) For string "how-does-this-work",
//      asking for 3rd token returns "this-work"s
String getTokenToEnd(String msg, const int num)
{
  String token = "";
  int index = -1;
  int to = 0;
  int i = 0;
  while(i <= num)
  {
    index = msg.indexOf("-", 1);
    if (index + i < 0)
    {
      // Error -- I don't think code currently cares if it gets error
      token = "ERROR: No Such Token";
      return token;
    }
    else if(index < 0)
    {
      // Never found a '-' character -- return remaining message
      token = msg;
      return token;
    }
    else if(i == num)
    {
      // This is the token we want
      token = msg;
      return token;
    }
    // Remove earlier part of message, if not the token we want
    msg = msg.substring(index+1);
    i++;
  }
  return token;
}

int getLen(String x){
   // returns the String interpreted as an integer
   // I don't think I use this anymore...
   return x.toInt(); 
}

// returns a 4-byte string corresponding to the value of x
// Used for padding integer values to a fixed length
//   Example: byteLen(53) returns "0053"
String byteLen(int x){
  String str = String(x);
  switch(str.length()){
    case 1:
      str = "000" + str;
      break;
    case 2:
      str = "00" + str;
      break;
    case 3:
      str = "0" + str;
      break;
    case 4:
      break;
    case 5:
      str = "0000";
      break;
  }
  return str;
}

// string is 3 concatenated 4byte strings
// e.g (255,50,105) is 025500500105
// Converts that string to a Color -- defined in Shiftbrite.h
Color stringToRGB(String str){
  int rgb[3];
  Color ret;
  ret.name = str;
  String tmp;
  for(int i = 0; i < 3; i++){
   tmp = str.substring(0, 4);
   rgb[i] = tmp.toInt();
   str = str.substring(4);
  }
  ret.r = rgb[0];
  ret.g = rgb[1];
  ret.b = rgb[2];
  return ret;
}

Color setName(Color a)
{
  // Sets the name of the color to it's rgb values
  //  Example: For Color with rgb (255,50,105)
  //                name becomes "025500500105"
  String tmp = "";
  tmp += byteLen(a.r);
  tmp += byteLen(a.g);
  tmp += byteLen(a.b);
  a.name = tmp;
  return a;
}

String rgbToString(int* rgb){
  // Converts integer array to String
  // I don't think I use this anymore
  String tmp = "";
  for(int i = 0; i < 3; i++){
    tmp +=  byteLen(rgb[i]);
  }
  return tmp;
}
