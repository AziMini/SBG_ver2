##  import time
##  from GIFImage import *
##  
##  test = GIFImage("./Source/Charictor/GIF/Charictor_Blue_A.gif")
##  
##  pygame.init()
##  
##  pygame.display.set_mode((500, 500))
##  
##  test.play()
##  
##  pygame.display.update()
##  
##  
##  while 1:
##      for event in pygame.event.get():
##          if event.type == pygame.QUIT:
##              exit()


##  import os
##  import sys
##  import time
##  import pygame
##  
##  pygame.init()
##  
##  gameDisplay = pygame.display.set_mode((1280, 720))
##  
##  crashed = False
##  num = 1
##  
##  Red = "/home/pi/SmartBoardGame/Board/Source/Character/Stand/Red/N.png"
##  Blue = "/home/pi/SmartBoardGame/Board/Source/Character/Stand/Blue/N.png"
##  Green = "/home/pi/SmartBoardGame/Board/Source/Character/Stand/Green/N.png"
##  Purple = "/home/pi/SmartBoardGame/Board/Source/Character/Stand/Purple/N.png"
##  
##  while not crashed:
##      for event in pygame.event.get():
##          if event.type == pygame.QUIT:
##              chrashed = True
##              pygame.quit()
##          if event.type == pygame.KEYDOWN:
##              if event.key == pygame.K_q:
##                  chrashed = True
##                  pygame.quit()
##  
##      gameDisplay.blit(pygame.image.load(Red.replace('N', str(num))), (0, 0))
##      gameDisplay.blit(pygame.image.load(Blue.replace('N', str(num))), (50, 50))
##      gameDisplay.blit(pygame.image.load(Green.replace('N', str(num))), (100, 100))
##      gameDisplay.blit(pygame.image.load(Purple.replace('N', str(num))), (150, 150))
##  
##      pygame.display.update()
##  
##      num = num + 1
##      if num > 8:
##          num = 1
##  
##      time.sleep(0.1);
##  
##  pygame.quit()

##  try:
##      listss = ((100, 200, 300), (10, 20), (1, 2))
##      answer = 0
##  
##      for lists in listss:
##          print(lists)
##          for lis in lists:
##              print(lis)
##              answer = lis
##  
##  except ValueError:
##      pass

now = [1, 2]
dst = [3, 4]

print(1 in now)
print(now == dst)
print(now)
print(dst)
