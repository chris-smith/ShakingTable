import serial, io, re, datetime
from numpy import *

ser = [serial.Serial('/dev/tty.usbmodem1411', 9600, timeout=0), serial.Serial('/dev/tty.usbmodem1421', 9600, timeout=0)]

def loop():
        while True:
                for s in ser:
                        index = ser.index(s)
                        raw = s.readline()
                        # if (raw.isdigit()):
                        # 	print str(index) + ", " + raw
                        if (raw is not None and raw.isdigit() and raw > 10):
                            rawVal = int(filter(lambda x: x.isdigit(), raw))
                            if rawVal > 10:
                            	print "{0},{1},{2}".format(index, datetime.datetime.now(), rawVal)

if __name__ == '__main__':
        loop()