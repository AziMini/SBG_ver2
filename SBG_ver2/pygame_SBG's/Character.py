#!/usr/bin/python3
import os
import time
import pygame

flag_RED = False
flag_BLUE = False
flag_GREEN = False
flag_PURPLE = False

Block_x  =  ((1032, 898, 764, 631, 494, 360, 226, 99),
            (222, 352, 491, 630, 767, 973),
            (841, 629, 498, 354),
            (495, 700),
            (579, 0))
Block_y  =  (617, 484, 351, 218, 85)

LEFT = 1
RIGHT = 2

DEFAULT_PATH = "./Source/Character/"

class Player:
    def __init__(self, Index, Color):
        self.index = Index
        self.color = Color

        self.action = 1
        self.direction = 'Left'
        self.turn = False

        self.now_pos = [Block_x[0][0] + (self.index * 35), Block_y[0]]
        self.dst_pos = [Block_x[0][0] + (self.index * 35), Block_y[0]]
        self.path = [DEFAULT_PATH + "Stand/" + Color + "/N.png",
                     DEFAULT_PATH + "Run/" + Color + "/N.png"]

##          print("index: ", self.index)
##          print("now_pos: ", self.now_pos)
##          print("dst_pos: ", self.dst_pos)
##          print("character_a", self.path[0])
##          print("character_u", self.path[1])

    def AddBlock(self, dice):
        now_index = [0, 0]
        for listx in Block_x:
            for x in listx:
                if x == self.now_pos[0] - (self.index * 35):
                    now_index[0] = listx.index(x)

        if now_index[0] == 0:
            for j in Block_x:
                if j[-1] == self.now_pos[0]:
                    now_index[0] = j.index(j[-1])


        for y in Block_y:
            if y == self.now_pos[1]:
                now_index[1] = Block_y.index(y)

        print("Before now_index: ", now_index)

        if now_index[1] == 4:
            now_index[0] = now_index[0] + 20

        elif now_index[1] == 3:
            now_index[0] = now_index[0] + 18

        elif now_index[1] == 2:
            now_index[0] = now_index[0] + 14

        elif now_index[1] == 1:
            now_index[0] = now_index[0] + 8

        now_index[0] = now_index[0] + dice
        print("Added now_index: ", now_index)

        result = 0

        if now_index[0] > 17:
            now_index[0] = 0
            if dice == 1 and now_index[1] == 2:
                result = "End"
                now_index[1] = 3
            else:
                if now_index[1] != 3:
                    now_index[0] = 3
                    now_index[1] = 2
        elif now_index[0] > 13:
            now_index[0] = now_index[0] - 14
            if dice < 4 and now_index[1] == 1:
                result = 3
                now_index[1] = 2
            else:
                if now_index[1] != 2:
                    now_index[0] = 5
                    now_index[1] = 1
        elif now_index[0] > 7:
            now_index[0] = now_index[0] - 8
            if dice > 3 and now_index[1] == 0:
                result = 4
                now_index[1] = 1
            else:
                if now_index[1] != 1:
                    now_index[0] = 7
                    now_index[1] = 0

        print("result: ", result)
        print("After now_index: ", now_index)

        self.SetDstPos(now_index[0], now_index[1])

        return result

    def SetNowPos(self, x, y):
        self.now_pos[0] = x
        self.now_pos[1] = y

    def SetDstPos(self, square, floor):
        if self.now_pos[1] != Block_y[floor]:
            self.now_pos[1] = Block_y[floor]
            self.now_pos[0] = Block_x[floor][0]

        self.dst_pos[0] = Block_x[floor][square]
        self.dst_pos[1] = Block_y[floor]

        if Block_x[floor][square] != Block_x[floor][0] and Block_x[floor][square] != Block_x[floor][-1]:
            self.dst_pos[0] = self.dst_pos[0] + (self.index * 35)

        print("now_pos", self.now_pos)
        print("dst_pos", self.dst_pos)

        self.CheckDirection()

    def CheckTurn(self, nowTurn):
        if self.index == nowTurn:
            self.turn = True
        else :
            self.turn = False

    def CheckDirection(self):
        if self.now_pos[1] in [617, 351]:
            self.direction = "Left"
        elif self.now_pos[1] in [484, 218, 85]:
            self.direction = "Right"
        else:
            os.exit(1)

