import pygame
from pygame.locals import *
import math
import time
import random

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos = [300, 240]
pi = math.pi
acc = [0, 0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[-64, 100]]
healthvalue = 194

player = pygame.image.load('resources/images/dude.png')
grass = pygame.image.load('resources/images/grass.png')
castle = pygame.image.load('resources/images/castle.png')
arrow = pygame.image.load('resources/images/bullet.png')
badguyimg1 = pygame.image.load('resources/images/badguy.png')
badguyimg = pygame.transform.flip(badguyimg1, True, False)

while 1:
    badtimer -= 1

    screen.fill(0)
    for x in range(width//grass.get_width() + 1):
        for y in range(height//grass.get_height() + 1):
            screen.blit(grass,(x * 100, y * 100))
    screen.blit(pygame.transform.flip(castle, True, False), (531, 30))
    screen.blit(pygame.transform.flip(castle, True, False), (531, 135))
    screen.blit(pygame.transform.flip(castle, True, False), (531, 240))
    screen.blit(pygame.transform.flip(castle, True, False), (531, 345))
	
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - (playerpos[0] + 26))
    playerrot = pygame.transform.rotate(player, 360-angle * (360 / (2 * pi)))
    playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
    screen.blit(playerrot, playerpos1)

    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))

    if badtimer == 0:
        badguys.append([-64, random.randint(50, 430)])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index = 0
    for badguy in badguys:
        if badguy[0] > 640:
            badguys.pop(index)
        badguy[0] += 7
        index += 1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)

    pygame.display.flip()
	
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()			
            exit(0)
	    
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                    
            if event.key == K_w:
                keys[0] = True
            if event.key == K_a:
                keys[1] = True
            if event.key == K_s:
                keys[2] = True
            if event.key == K_d:
                keys[3] = True
	    
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            if event.key == K_a:
                keys[1] = False
            if event.key == K_s:
                keys[2] = False
            if event.key == K_d:
                keys[3] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)), playerpos1[0] + 32, playerpos1[1] + 32])

    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5
