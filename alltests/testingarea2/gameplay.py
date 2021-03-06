import pygame, math, time, random
from pygame.locals import *

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
badguys = [[-35, 100]]
healthvalue = 194
dead = False
gamestatus = 0
accuracy = 0

player = pygame.image.load('resources/PNG/Soldier1/soldier1_gun.png')
grass = pygame.image.load('resources/PNG/Tiles/tile_01.png')
castle1 = pygame.image.load('resources/PNG/towerDefense_tile205.png')
castle = pygame.transform.rotate(castle1, -90)
arrow1 = pygame.image.load('resources/PNG/Tiles/tile_533.png')
arrow = pygame.transform.scale(arrow1, (32, 32))
badguyimg1 = pygame.image.load('resources/PNG/Robot1/robot1_hold.png')
badguyimg = badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

class GamePlay():
    while 1:
        #exitcode = 1
        badtimer -= 1

        screen.fill(0)
        for x in range(width//grass.get_width() + 1):
            for y in range(height//grass.get_height() + 1):
                screen.blit(grass,(x * 60, y * 60))
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
            badguys.append([-35, random.randint(50, 430)])
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
            badrect = pygame.Rect(badguyimg.get_rect())
            badrect.top = badguy[1]
            badrect.right = badguy[0]
            if badrect.right > 531:
                healthvalue -= random.randint(5, 20)
                print(healthvalue)
                badguys.pop(index)
            index1 = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[1]
                bullrect.top = bullet[2]
                if badrect.colliderect(bullrect):
                    acc[0] += 1
                    badguys.pop(index)
                    arrows.pop(index1)
                index1 += 1
            index += 1
        for badguy in badguys:
            screen.blit(badguyimg, badguy)

        #font = pygame.font.Font(None, 24)
        #survivedtext = font.render(str((90000 - pygame.time.get_ticks())/60000) + ':' + str((90000 - pygame.time.get_ticks())/1000%60).zfill(2), True, (0, 0, 0))
        #textRect = survivedtext.get_rect()
        #textRect.topright = [635, 5]
        #screen.blit(survivedtext, textRect)

        screen.blit(healthbar, (5, 5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1 + 8, 8))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    exit(0)

                if event.key == K_w:
                    keys[0] = True
                if event.key == K_a:
                    keys[1] = True
                if event.key == K_s:
                    keys[2] = True
                if event.key == K_d:
                    keys[3] = True

                if event.key == K_SPACE:
                    position = pygame.mouse.get_pos()
                    acc[1] += 1
                    arrows.append([math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)), playerpos1[0] + 32, playerpos1[1] + 32])

            if event.type == pygame.KEYUP:
                if event.key == K_w:
                    keys[0] = False
                if event.key == K_a:
                    keys[1] = False
                if event.key == K_s:
                    keys[2] = False
                if event.key == K_d:
                    keys[3] = False

        if keys[0]:
            playerpos[1] -= 5
        elif keys[2]:
            playerpos[1] += 5
        if keys[1]:
            playerpos[0] -= 5
        elif keys[3]:
            playerpos[0] += 5

        if healthvalue < 0:
            #exitcode = 0
            dead = True
            print("hello ladies")
            gamestatus = 1
            break
        if acc[1] != 0:
            accuracy = acc[0] * 1.0 / acc[1] * 100
        else:
            accuracy = 0

        #if dead == True:
        #    gamestatus = 1