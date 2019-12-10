import sys
import time
import serial

Dice = 7
buff = [1, 1, 1]
endFlag = False

if len(sys.argv) < 3:
    print(sys.argv[0] +" [Turn]")
    sys.exit(-1)
turn = sys.argv[1]
Flag_IR = int(sys.argv[2])

f = open("result", 'w')

ser = serial.Serial(port="COM8", baudrate=9600)
print(ser.portstr)

#def SendData(data):
#    packet = [0x02]
#    packet.append(data)
#    packet.append(0x03)

#    ser.write(packet)

#    print("Sent 0x{} {} 0x{}".format(0x02, hex(data), 0x03))

if __name__ == "__main__":
    while True:
        if Flag_IR == 1:
            ser.write("SEND PLESE")
            msg = ser.read()
            f.write(turn + '\n' + str(msg))
            sys.exit(0)

        time.sleep(0.3)
