import os
import sys
import time
import pygame

flag_FULL = False; pre_flag_FULL = False
flag_TURN = 1; pre_flag_TURN = 1
flag_DOOR = 0; pre_flag_DOOR = 0

backgroundSize = (1280, 720)
frame = 1
i = 0

gameDisplay = pygame.display.set_mode(backgroundSize, pygame.DOUBLEBUF)
pygame.display.set_caption('SMART BOARD GAME')

Door_Squares = [587, 708, 503, 362, 849, 981, 230, 107]
Door_Floors = [90, 223, 223, 356, 356, 489, 489, 622]

def InitBackground():
    gameDisplay.blit(pygame.image.load("./Source/BG.png"),(0,0))
    for i in range(0, 8):
        gameDisplay.blit(pygame.image.load("./Source/Open_Door/1.png"), (Door_Squares[i], Door_Floors[i]))

    gameDisplay.blit(pygame.image.load("./Source/Dice/1.png"), (114, 612))
    gameDisplay.blit(pygame.image.load("./Source/Dice/2.png"), (119, 612))
    gameDisplay.blit(pygame.image.load("./Source/Dice/3.png"), (124, 612))

    gameDisplay.blit(pygame.image.load("./Source/Dice/4.png"), (988, 479))
    gameDisplay.blit(pygame.image.load("./Source/Dice/5.png"), (993, 479))
    gameDisplay.blit(pygame.image.load("./Source/Dice/6.png"), (998, 479))

    gameDisplay.blit(pygame.image.load("./Source/Dice/1.png"), (374, 346))

def SetDoor(door):
    global flag_DOOR

    flag_DOOR = door

def Frame(players):
    first = -1

    global flag_DOOR
    global pre_flag_DOOR
    global frame

    global i

    gameDisplay.blit(pygame.image.load("./Source/BG.png"),(0,0))
    for j in range(0, 8):
        if flag_DOOR == 0 and pre_flag_DOOR != 0:
            if j == (abs(pre_flag_DOOR) - 1 ) * 2:
                pass
            elif j == (abs(pre_flag_DOOR) - 1 ) * 2 + 1:
                pass
        gameDisplay.blit(pygame.image.load("./Source/Open_Door/1.png"), (Door_Squares[j], Door_Floors[j]))

    if flag_DOOR == None:
        print("None")
        pass

    if flag_DOOR != 0:
        if flag_DOOR != pre_flag_DOOR:
            if flag_DOOR < 0:
                i = 7
##                  os.system("mpg123 -q Close_Door.mp3 &")
            elif flag_DOOR > 0:
                i = 1
##                  os.system("mpg123 -q Open_Door.mp3 &")
            pre_flag_DOOR = flag_DOOR

        gameDisplay.blit(pygame.image.load("./Source/Open_Door/" + str(i) + ".png"),(Door_Squares[(abs(flag_DOOR) - 1) * 2], Door_Floors[(abs(flag_DOOR) - 1) * 2]))
        gameDisplay.blit(pygame.image.load("./Source/Open_Door/" + str(i) + ".png"),(Door_Squares[(abs(flag_DOOR) - 1) * 2 + 1], Door_Floors[(abs(flag_DOOR) - 1) * 2 + 1]))

        if flag_DOOR < 0:
            i = i - 1
            if i == 1:
                flag_DOOR = 0
        elif flag_DOOR > 0:
            i = i + 1
            if i == 7:
                flag_DOOR = 0

    for player in players:
        action = player.action
        if player.turn == True:
            first = players.index(player)
        else:
            path = player.path[0].replace('N', str(action))
            gameDisplay.blit(pygame.image.load(path), tuple(player.now_pos))
        player.action = (player.action % 8) + 1

        if player.now_pos[1] != player.dst_pos[1]:
            if player.now_pos[0] == player.Block_x[player.now_pos[1]][-1]:
                player.now_pos[1] = player.Block_y[(player.Block_x.index(player.now_pos[1]) + 1)]
                player.now_pos[0] = player.Block_x[player.now_pos[1]][0]
        if player.now_pos[0] != player.dst_pos[0]:
            player.CheckDirection()
            if player.direction == "Left":
                if player.now_pos[0] - 10 < player.dst_pos[0]:
                    player.now_pos[0] = player.dst_pos[0]
                else:
                    player.now_pos[0] = player.now_pos[0] - 10
            elif player.direction == "Right":
                if player.now_pos[0] + 10 > player.dst_pos[0]:
                    player.now_pos[0] = player.dst_pos[0]
                else:
                    player.now_pos[0] = player.now_pos[0] + 10


    if first >= 0:
        path = players[first].path[1].replace('N', players[first].direction + str(players[first].action))
        gameDisplay.blit(pygame.image.load(path), tuple(players[first].now_pos))
##          print("Running now_pos", players[first].now_pos)
##          print("Running dst_pos", players[first].dst_pos)

    frame = frame + 1
    pygame.display.update()

def ChangeFULL():
    global flag_FULL

    if flag_FULL == 1:
        gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        flag_FULL = 0
    else:
        gameDisplay = pygame.display.set_mode(backgroundSize, pygame.DOUBLEBUF)
        flag_FULL = 1
