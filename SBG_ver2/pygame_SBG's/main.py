import os
import sys
import time
import pygame
import traceback
import threading
import serial

from Character import *
from BG import *

flag_END = False
flag_START = False
flag_turn = 0

dice = -1
wait = 0
turn = 0
index = 0
state = 0
nowTurn = 0

players = []

#os.system("sudo ./AudioRepeat.sh BGM/Egypt_Theme.mp3 &")
pygame.init()

crashed = False

ser = serial.Serial(port="COM8", baudrate=9600) 

# 새로운 컴퓨터에서 작동할때 첫번째 인자 수정해야 할 가능성 높음(HC-05 가상 com port(송신))


def GetDice(ser):
    print ('start getdice')
    global dice
    global nowTurn
    while 1:
        if wait == 1:
            if dice == 0:
                print("in 1")
                nowTurn = (nowTurn + 1) % index
                player.CheckTurn(nowTurn)

                ser.write('SEND PLESE'.encode())
                dice = int(ser.read())

                time.sleep(1)
            else:
                print("in 2")
                ser.write('SEND PLESE'.encode())
                dice = int(ser.read())
                time.sleep(1)
        


print ('start program')
thread = threading.Thread(target=GetDice, args=(ser,))
thread.daemon = True
thread.start()
print ('trhead start')


def GetTraceBackStr():
    lines = traceback.format_exc().strip().split("\n")
    rl = [lines[-1]]
    lines = lines[1:-1]
    lines.reverse()

    for i in range(0, len(lines), 2):
        rl.append("^\t%s at %s" % (lines[i].strip(), lines[i+1].strip()))

    return '\n'.join(rl)

try:
    InitBackground()
    SetDoor(0)
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

#--------------------------------GAME SETTING-------------------------#

            if event.type is pygame.KEYDOWN:

                if event.key == pygame.K_f:
                    ChangeFULL()

                if event.key == pygame.K_q:
                    crashed = True

                if event.key == pygame.K_d:
                    for j in range(-4, 5):
                        SetDoor(j)
                        for k in range(0, 7):
                            Frame(players)

                if not flag_START:
                    if event.key == pygame.K_r:
                        if not flag_RED:
                            flag_RED = True
                            players.append(Player(index, "Red"))
                            index = index + 1
                    if event.key == pygame.K_b:
                        if not flag_BLUE:
                            flag_BLUE = True
                            players.append(Player(index, "Blue"))
                            index = index + 1

                    if event.key == pygame.K_g:
                        if not flag_GREEN:
                            flag_GREEN = True
                            players.append(Player(index, "Green"))
                            index = index + 1

                    if event.key == pygame.K_p:
                        if not flag_PURPLE:
                            flag_PURPLE = True
                            players.append(Player(index, "Purple"))
                            index = index + 1

                if event.key == pygame.K_s:
                    flag_START = True

#----------------------------------GAME LOGIC---------------------------------#

        if flag_START:
            if index < 1:
                print("We Need More Player")
                flag_START = False
            else:
                if players[nowTurn].now_pos == players[nowTurn].dst_pos:
                    #if wait == 1:
                    #    print("we wait\n")


                    #elif dice == 0:
                    #    nowTurn = (nowTurn + 1) % index
                    #    player.CheckTurn(nowTurn)
                    #    wait = 1
                    #print("in")

                    if 0 < dice < 7:
                        if state != "End":
                            gameDisplay.blit(pygame.image.load("./Source/Dice/" + str(dice) + ".png"), (825, 50))
                            state = players[nowTurn].AddBlock(dice)

                        if state == "End":
                            SetDoor(2)
                            for j in range(0, 7):
                                Frame(players)
                            players[nowTurn].SetNowPos(510, 218)
                            Frame(players)

                            players[nowTurn].SetDstPos(715, 218)
                            for j in range(0, 41):
                                Frame(players)

                            players[nowTurn].SetNowPos(594, 85)
                            Frame(players)

                            gameDisplay.blit(pygame.image.load("./Source/End.png"), (0, 0))
                            while True:
                                a = 1

                        elif state != 0:
                            SetDoor(state)
                            for j in range(0, 8):
                                Frame(players)

                            SetDoor(state * -1)
                            for j in range(0, 7):
                                Frame(players)

                        dice = 0

                    else:
                        #print("in communication")
                        wait = 1


#--------------------------------DISPLAY UPDATE--------------------------------#

        Frame(players)

        for player in players:
            player.CheckTurn(nowTurn)

except Exception as e:
    print(GetTraceBackStr())

finally:
    os.system("sudo killall AudioRepeat.sh")
    os.system("sudo killall mpg123")
    os.system("sudo killall python3")
    pygame.quit()
