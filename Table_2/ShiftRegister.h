#ifndef ShiftRegister_h
#define ShiftRegister_h

#include "Arduino.h" //It is very important to remember this!

//MAX NUMBER OF SHIFT REGISTERS IS 4

// After setting register pins, you'll need to call
//  writeRegisters() to see the changes

class ShiftRegister {
public:
        ShiftRegister(); //Default Constructor. Defaults to 4 shift registers
        ShiftRegister(int registers); //Overloaded Constructor. Registers is number of shift registers
        ~ShiftRegister(); //Destructor
	void clearRegisters(); //set all register pins to LOW
	void writeRegisters(); //Set and display registers
        void setRegisterPin(int index, int value); //set an individual pin HIGH or LOW
        void setRegisters(); //DEPRECATED??
        void setDefaults(); //Sets default num of shiftregisters
        void initArrays(); //Initializes registers[] and regVals[]
        
private:
        int _number_of_74hc595s;
        int _numOfRegisterPins;
        boolean registers[32];
        int regVals[32];
};

#endif
