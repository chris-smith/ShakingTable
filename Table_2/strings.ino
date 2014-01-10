// For strings formatted as ___-____-___, returns the numth member
// Zero indexed
/* Example Usage
    token = getToken("this-is-a-test", 1)
    token == "is"
**********************************************************/
String getToken(String msg, const int num)
{
  //xbee.print("num: ");xbee.println(num);
  String token = "";
  int index = -1;
  int to = 0;
  int i = 0;
  while(i <= num)
  {
    //xbee.println(msg);
    //xbee.print("i: ");xbee.println(i);
    index = msg.indexOf("-", 1);
    //xbee.print("index: ");xbee.println(index);
    if (index + i < 0)
    {
      //error
      token = "ERROR: No Such Token";
      return token;
    }
    else if(index < 0)
    {
      token = msg;
      return token;
    }
    else if(i == num)
    {
      //this is the token to get
      //xbee.println("grab this token");
      token = msg.substring(0,index);
      return token;
    }
    msg = msg.substring(index+1);
    i++;
  }
  return token;
}

//Once the numth token is reached, returns rest of the string
/* Example Usage
    rest = getTokenToEnd("this-is-a-test", 2)
    rest == "a-test"
**********************************************************/
String getTokenToEnd(String msg, const int num)
{
  //xbee.print("num: ");xbee.println(num);
  String token = "";
  int index = -1;
  int to = 0;
  int i = 0;
  while(i <= num)
  {
    //xbee.println(msg);
    //xbee.print("i: ");xbee.println(i);
    index = msg.indexOf("-", 1);
    //xbee.print("index: ");xbee.println(index);
    if (index + i < 0)
    {
      //error
      token = "ERROR: No Such Token";
      return token;
    }
    else if(index < 0)
    {
      token = msg;
      return token;
    }
    else if(i == num)
    {
      //this is the token to get
      //xbee.println("grab this token");
      token = msg;
      return token;
    }
    msg = msg.substring(index+1);
    i++;
  }
  return token;
}

int getLen(String x){
 return x.toInt(); 
}

//returns a 4-byte string corresponding to the value of x
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

//string is 3 concatenated 4byte strings
//e.g (255,50,105) is 025500500105
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
  String tmp = "";
  tmp += byteLen(a.r);
  tmp += byteLen(a.g);
  tmp += byteLen(a.b);
  a.name = tmp;
  return a;
}

/*----------------------------------
  THESE SHOULD NO LONGER BE NEEDED
  ----------------------------------*/
//string is 3 concatenated 4byte strings
//e.g (255,50,105) is 025500500105
int* stringToRGB(String str){
  int rgb[3];
  String tmp;
  for(int i = 0; i < 3; i++){
   tmp = str.substring(0, 4);
   rgb[i] = tmp.toInt();
   str = str.substring(4);
  }
  return rgb;
}

String rgbToString(int* rgb){
  String tmp = "";
  for(int i = 0; i < 3; i++){
    tmp +=  byteLen(rgb[i]);
  }
  return tmp;
}
