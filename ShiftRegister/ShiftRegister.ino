#include "ShiftRegister.h"
ShiftRegister shift;

void setup()
{
  
}

void loop()
{
  shift.setRegisterPin(2, HIGH);
  shift.setRegisterPin(3, LOW);
  shift.setRegisterPin(4, HIGH);
  shift.setRegisterPin(5, LOW);
  shift.setRegisterPin(7, HIGH); 
  shift.writeRegisters();
}
