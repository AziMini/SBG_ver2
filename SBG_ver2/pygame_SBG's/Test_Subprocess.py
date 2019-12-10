import time
import subprocess

path = "/home/pi/SmartBoardGame/Board/RF.py"

Turn = 0

while True:
    subprocess.run(['python3', path, str(Turn)])

    Turn = (Turn + 1) % 4

    f = open("result", 'r')
    print(f.readlines())
    time.sleep(1)
