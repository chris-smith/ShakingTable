import serial, io, re, datetime, sys
from numpy import *

serRead = [serial.Serial('/dev/tty.usbmodem1d1111', 9600), serial.Serial('/dev/tty.usbmodem1d1121', 9600)]
serWrite = serial.Serial('/dev/tty.usbmodem1421', 9600)

def loop():
    threshold = [70, 70]
    motorPower = [0, 0]

    # for power P, the motor sees (P/255)*5 volts
    MAX_POWER = 120
    MID_POWER = 70
    for i, arg in enumerate(sys.argv):
        if arg.isdigit():
            threshold[i-1] = int(arg)
            print str(threshold)
            
    while True:
        for s in serRead:
            index = serRead.index(s)
            raw = s.readline()
            # print raw
            # if (raw is not None and raw.isdigit() and raw > 10):
            # raw = serRead.readline()
            # index = 0
            rawVal = int(filter(lambda x: x.isdigit(), raw))
            if rawVal > threshold[index]:
                motorPower[index] = MAX_POWER
            elif rawVal > threshold[index] - 5:
                motorPower[index] = MID_POWER
            else:
                motorPower[index] = 0
            print "{0},{1},{2},{3}".format(index, datetime.datetime.now(), rawVal, motorPower[index])
        print "motorPower: " + str(max(motorPower))
        serWrite.write(chr(max(motorPower)))

if __name__ == '__main__':
        loop()