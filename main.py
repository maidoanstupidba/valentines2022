$ heroku buildpacks:set heroku/python
heroku create --buildpack https://github.com/heroku/heroku-buildpack-python.git
    
import pygame
import random
import math
from pygame import mixer

pygame.init()

FPS = 60
fpsclock = pygame.time.Clock()

screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('background.jpg')

# bangokngek
maiImg = []
maiX = []
maiY = []
maiX_change = []
maiY_change = []
num_of_mai = 5

for i in range(num_of_mai):
    maiImg.append(pygame.image.load('bangokngek.jpg'))
    maiX.append(random.randint(0,735))
    maiY.append(random.randint(20,150))
    maiX_change.append(0.2)
    maiY_change.append(20)

    def mai(x,y,i):
        screen.blit(maiImg[i],(x,y))

# mylove
myloveImg = pygame.image.load('mylove.jpg')
myloveX = 380
myloveY = 500
myloveX_change = 0
myloveY_change = 0

def mylove(x,y):
    screen.blit(myloveImg,(x,y))

# heart
heartImg = pygame.image.load('heart.png')
heartX = 0
heartY = myloveY
heartX_change = 0
heartY_change = 0.4

heart_state = "ready"

def heart(x,y):
    global heart_state
    heart_state = "fire"
    screen.blit(heartImg,(x+16,y+10))

# icon and title
title = pygame.display.set_caption("Happy Valentines's Day to my H")
icon = pygame.image.load('heart.png')
pygame.display.set_icon(icon)

# check collision
def iscollision(bangokngekX,bangokngekY,heartX,heartY):
    distance = math.sqrt(math.pow(bangokngekX - heartX,2)+math.pow(bangokngekY - heartY,2))

    if distance < 27:
        return True
    else:
        return False

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Yêu Mai x " + str(score_value),True, (150,150,255))
    screen.blit(score,(x,y))

# Game over
over_font = pygame.font.SysFont('Segoe UI',40)

def game_over_text():
    over_text_1 = over_font.render("Bảo iêu mình mà lại Game over!!" ,True, (150,150,255))
    over_text_2 = over_font.render("Thế là ghét mình dzồi >.< " ,True, (150,150,255))
    over_image = pygame.image.load('gameover.jpg')
    screen.blit(over_text_1,(60,150))
    screen.blit(over_text_2,(100,220))
    screen.blit(over_image,(300,300))

# sound and musicque
mixer.music.load("lovinyou.wav")
mixer.music.play(-1) #infinitely repeat: -1

running = True
while running:

    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                myloveX_change = 1
            if event.key == pygame.K_LEFT:
                myloveX_change = -1
            if event.key == pygame.K_UP:
                myloveY_change = -1
            if event.key == pygame.K_DOWN:
                myloveY_change = 1
            if event.key == pygame.K_SPACE:
                if heart_state == "ready":
                    heartX = myloveX
                    heartY = myloveY
                    heart(heartX,heartY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                myloveX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                myloveY_change = 0

    mylove(myloveX,myloveY)
    myloveX += myloveX_change
    myloveY += myloveY_change

    if myloveX <=0:
        myloveX = 0 
    elif myloveX >=736:
        myloveX = 736

    if myloveY <= 400: 
        myloveY = 400
    elif myloveY >=530:
        myloveY = 529

    for i in range(num_of_mai):
        # game over
        if maiY[i] > 200:
            for j in range(num_of_mai):
                maiY[j] =2000
            game_over_text()
            break

        mai(maiX[i],maiY[i],i)

        if maiX[i] <= 0:
            maiX_change[i] = 0.2
            maiY[i] += maiY_change[i]
        if maiX[i] >= 736:
            maiX_change[i] = -0.2
            maiY[i] += maiY_change[i] 

        maiX[i] += maiX_change[i] #Mai quay xe
           
        collision = iscollision(maiX[i],maiY[i],heartX,heartY)
        if collision:
            heart_state = "ready"
            maiY[i] = random.randint(50,150)
            maiX[i] = random.randint(0,735)
            score_value += 1
            explosion_sound = mixer.Sound('tick.wav')
            explosion_sound.play()

    if heartY <= 0:
        heartY = myloveY
        heart_state ="ready" 
    if heart_state == "fire":
        heartY -= heartY_change
        heart(heartX,heartY)

    show_score(textX,textY)
    fpsclock.tick()
    pygame.display.flip()
