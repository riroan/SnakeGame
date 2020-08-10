import pygame
import random
from pygame.locals import *

#=================================================Param==============================================#

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
RED   = (255,  0,  0)
GREY  = (128,128,128)

TILE_SIZE = (30,30)
ROW = 20   
COL = 15
WIDTH = 20+30*COL
HEIGHT = 20+30*ROW

LEFT  = 0
UP    = 1
RIGHT = 2
DOWN  = 3

#================================================Init================================================#

size = [WIDTH+500,HEIGHT]
screen = pygame.display.set_mode(size)

pygame.init()
pygame.display.set_caption("Snake Game")
done = False
clock = pygame.time.Clock()

FPS = 4

#============================================Class, Function========================================#

def get_xy(pos):
    return (pos%COL, pos//COL)

def get_pos(x, y):
    return x * COL + y

class Player:
    def __init__(self):
        self.direction = RIGHT
        self.body = [ROW * COL // 4 + 2]
        self.length = len(self.body)
        self.die = False
        self.eat = False
        self.food_pos = ROW*COL//3
    
    def draw(self, pos, color):
        (x, y) = get_xy(pos)
        pygame.draw.rect(screen, color, [10+30*x,10+30*y,31,31])
    
    def draw_body(self):
        for i in self.body:
            self.draw(i, GREEN)
    
    def move(self):
        self.eat = False
        pos = self.body[-1]
        next_pos = 0
        if self.direction == LEFT:
            next_pos = pos-1
            if abs(next_pos // COL - pos // COL):
                self.die = True
        elif self.direction == UP:
            next_pos = pos-COL
            if abs(next_pos % COL - pos % COL):
                self.die = True
        elif self.direction == RIGHT:
            next_pos = pos+1
            if abs(next_pos // COL - pos // COL):
                self.die = True
        elif self.direction == DOWN:
            next_pos = pos+COL
            if abs(next_pos % COL - pos % COL):
                self.die = True
        if next_pos in self.body:
            self.die = True
                
        self.body.append(next_pos)
        
        self.isEat()
        self.draw(self.food_pos, BLUE)
        
        if not self.eat:
            del self.body[0]
        
    def turn(self, key):
        if key == LEFT:
            if self.direction == UP or self.direction == DOWN:
                self.direction = LEFT
        elif key == RIGHT:
            if self.direction == UP or self.direction == DOWN:
                self.direction = RIGHT
        elif key == UP:
            if self.direction == LEFT or self.direction == RIGHT:
                self.direction = UP
        elif key == DOWN:
            if self.direction == LEFT or self.direction == RIGHT:
                self.direction = DOWN
        
    def isEat(self):
        if self.body[-1] == self.food_pos:
            pos = random.randrange(0,ROW*COL)
            while pos in self.body:
                pos = random.randrange(0,ROW*COL)
            self.food_pos = pos
            self.eat = True
        
#=============================================Main Loop==============================================#

player = Player()

while not player.die:
    
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.turn(LEFT)
            elif event.key == K_RIGHT:
                player.turn(RIGHT)
            elif event.key == K_UP:
                player.turn(UP)
            elif event.key == K_DOWN:
                player.turn(DOWN)
    
    screen.fill(WHITE)
    
    for i in range(COL):
        pygame.draw.line(screen, GREY, [10+i*30,0],[10+i*30,HEIGHT])
    
    for i in range(ROW):
        pygame.draw.line(screen, GREY, [0,10+i*30],[WIDTH,10+i*30])
        
    pygame.draw.rect(screen, BLACK, [0,0,10,HEIGHT])
    pygame.draw.rect(screen, BLACK, [0,0,WIDTH, 10])
    pygame.draw.rect(screen, BLACK, [0,HEIGHT-10,WIDTH,10])
    pygame.draw.rect(screen, BLACK, [WIDTH-10,0,10,HEIGHT])
    
    pygame.draw.rect(screen, BLACK, [700,500,50,50])
    pygame.draw.rect(screen, BLACK, [650,500,50,50])
    pygame.draw.rect(screen, BLACK, [750,500,50,50])
    pygame.draw.rect(screen, BLACK, [700,450,50,50])
    
    player.draw_body()
    player.move()
    
    pygame.display.update()
    clock.tick(FPS)
    
    
    
print("good bye")
