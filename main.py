import os
import random

import pygame
import time


WIN = pygame.display.set_mode((800,700))
pygame.display.set_caption("FISHING :3")
pygame.font.init()
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (135,206,235)
YELLOW = (255,215,0)


FONT = pygame.font.SysFont('comicsans',40,)
ADD_IMAGE = pygame.image.load(os.path.join('Assets', 'add.png'))
SUBTRACT_IMAGE = pygame.image.load(os.path.join('Assets', 'minus.png'))
class Button:
    def __init__(self,x,y,image):
        width = image.get_width()
        height = image.get_height()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        action = False
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                action = True
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Progress_Bar:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.current_progress = 200



    def draw(self):
        if self.current_progress>self.height:
            self.current_progress=self.height
        progress = self.current_progress/self.height
        pygame.draw.rect(WIN, WHITE,(self.x, self.y, self.width, self.height))
        pygame.draw.rect(WIN, GREEN, (self.x, (self.y + self.height) - (self.height * progress), self.width, self.height * progress))
        pygame.draw.rect(WIN, BLACK, (self.x, self.y, self.width, self.height), 5)
        pygame.display.update()

class Fishing_Bar():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


    def draw(self):
        pygame.draw.rect(WIN, WHITE,(self.x,self.y,self.width,self.height))
        pygame.draw.rect(WIN, BLACK, (self.x, self.y, self.width, self.height), 5)
        pygame.display.update()


class Fish():
    def __init__(self,speed,x,y,width,height):
        self.spawned = False
        self.caught=False
        self.speed=speed
        self.fishy = pygame.Rect(x,y,width,height)
    def spawn_fishy(self):
        pygame.draw.rect(WIN, YELLOW,(self.fishy.x,self.fishy.y,self.fishy.width,self.fishy.height))
        pygame.display.update()
        self.spawned = True

    def fishy_move(self):
        num = random.randrange(1,100)
        if self.spawned and num<40:
            if self.fishy.y-self.speed > 30:
                self.fishy.y-=self.speed
            else:
                pass
        elif self.spawned and num> 60:
            if self.fishy.y + self.speed < 590:
                self.fishy.y += self.speed
            else:
                pass






class Fishing_Region():
    def __init__(self,screen,x,y,width,height):
        self.screen= screen
        self.height=height
        self.region = pygame.Rect(x,y,width,height)
        self.fishing = True


    def draw(self):
        pygame.draw.rect(WIN, GREEN,(self.region.x+5,self.region.y,self.region.width-10,self.height))
        pygame.display.update()

    def move_bar(self,max):
         if not self.region.y-5<=max-5:
            self.region.y-=10
    def drop_bar(self,min):
        if self.region.y+self.height+10<min:
            self.region.y+=10


def draw_text(text,x,y):
    draw_text = FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (x, y - draw_text.get_height() // 2))
    pygame.display.update()

addSpeed = Button(450,150,ADD_IMAGE)
subtractSpeed = Button(650,150,SUBTRACT_IMAGE)

addSize = Button(450,300,ADD_IMAGE)
subtractSize = Button(650, 300, SUBTRACT_IMAGE)
def main():
    SPEED = 35
    SIZE = 80
    run = True
    bar = Progress_Bar(250,20,20,600)
    fishingBar = Fishing_Bar(100,20,70,600)
    fish = Fish(SPEED,120,60,30,30)
    fishing_region = Fishing_Region(WIN,100,200,70,SIZE)
    WIN.fill(BLUE)



    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if bar.current_progress == bar.height:
            pygame.time.delay(5000)
            bar.current_progress=0
        if fishing_region.region.colliderect(fish.fishy):
            bar.current_progress+=15
        elif not fishing_region.region.colliderect(fish.fishy) and bar.current_progress-10>=0:
            bar.current_progress-=10



        bar.draw()
        fishingBar.draw()
        fishing_region.draw()
        addSpeed.draw()
        subtractSpeed.draw()
        addSize.draw()
        subtractSize.draw()

        draw_text("Speed",510,160)
        draw_text("Size", 520, 310)

        if addSpeed.draw():

            fish.speed +=5

        if subtractSpeed.draw() and fish.speed>10:
            fish.speed-=5


        if addSize.draw()and SIZE<150:
            SIZE+=10
            fishing_region = Fishing_Region(WIN,100,200,70,SIZE)


        if subtractSize.draw() and SIZE>30:
            SIZE-=10
            fishing_region = Fishing_Region(WIN,100,200,70,SIZE)

        if pygame.mouse.get_pressed()[0] and not addSpeed.draw() and not subtractSpeed.draw() and not subtractSize.draw() and not addSize.draw():
            fishing_region.move_bar(fishingBar.y)
        else:
            fishing_region.drop_bar(fishingBar.height+25)


        fish.spawn_fishy()
        fish.fishy_move()
        time.sleep(0.1)





if __name__ == "__main__":
    main()