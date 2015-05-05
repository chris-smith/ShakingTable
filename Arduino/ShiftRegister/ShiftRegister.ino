/*
  This is a very basic example program to show use of the shift register
    https://www.sparkfun.com/products/733
  Pinout is specified in ShiftRegister.cpp
*/

#include "ShiftRegister.h"
ShiftRegister shift;

void setup()
{
 // nothing to do 
}

void loop()
{
  // Set register values for 1 shift register
  shift.setRegisterPin(2, HIGH);
  shift.setRegisterPin(3, LOW);
  shift.setRegisterPin(4, HIGH);
  shift.setRegisterPin(5, LOW);
  shift.setRegisterPin(7, HIGH); 
  // If there are 2 shift registers, you might call
  //   shift.setRegisterPin(10, HIGH);
  
  // Write register
  shift.writeRegisters();
}
