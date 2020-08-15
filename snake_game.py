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
ROW = 10
COL = 10
WIDTH = 20+30*COL
HEIGHT = 20+30*ROW

LEFT  = 0
UP    = 1
RIGHT = 2
DOWN  = 3

#================================================Init================================================#

size = [2 * WIDTH,HEIGHT+300]
screen = pygame.display.set_mode(size)
screen2 = pygame.display.set_mode(size)

pygame.init()
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

FPS = 15
start = False

#============================================Class, Function========================================#

def get_xy(pos):
    return (pos%COL, pos//COL)

def get_pos(x, y):
    return x * COL + y

class Environment:
    def __init__(self, human = False):
        self.direction = RIGHT
        self.body = [ROW * COL // 4 + 2]
        self.die = False
        self.win = False
        self.eat = False
        self.done = self.win or self.die
        self.food_pos = random.randrange(0,ROW*COL)
        self.flag = False
        self.human = human
    
    def reset(self):
        self.direction = RIGHT
        self.body = [ROW*COL // 4 + 2]
        self.die = False
        self.win = False
        self.eat = False
        self.done = self.win or self.die
        self.food_pos = random.randrange(0,ROW*COL)
    
    def draw(self, pos, color):
        dx = 0
        if self.human:
            dx = WIDTH
        (x, y) = get_xy(pos)
        pygame.draw.rect(screen, color, [dx + 10+30*x,10+30*y,31,31])
    
    def draw_body(self):
        for i in self.body:
            if self.human:
                self.draw(i, GREEN)
            else:
                self.draw(i, RED)
    
    def step(self, action):
        if not self.human:
            self.turn(action)
        self.eat = False
        pos = self.body[-1]
        next_pos = 0
        if self.direction == LEFT:
            next_pos = pos-1
            if abs(next_pos // COL - pos // COL):
                self.die = True
        elif self.direction == UP:
            next_pos = pos-COL
            if next_pos < 0:
                self.die = True
        elif self.direction == RIGHT:
            next_pos = pos+1
            if abs(next_pos // COL - pos // COL):
                self.die = True
        elif self.direction == DOWN:
            next_pos = pos+COL
            if next_pos > COL * ROW:
                self.die = True
        if next_pos in self.body:
            self.die = True
        
        self.body.append(next_pos)
        self.isEat()
        
        if not self.eat:
            del self.body[0]
        
        if len(self.body) == ROW*COL:
            self.win = True
        self.done = self.win or self.die
        self.flag = False
        
    def simulate(self, action, body, direction):
        body = body.copy()
        pos = body[-1]
        die = False
        next_pos = 0
        if direction == LEFT:
            next_pos = pos-1
            if abs(next_pos // COL - pos // COL):
                die = True
        elif direction == UP:
            next_pos = pos-COL
            if next_pos < 0:
                die = True
        elif direction == RIGHT:
            next_pos = pos+1
            if abs(next_pos // COL - pos // COL):
                die = True
        elif direction == DOWN:
            next_pos = pos+COL
            if next_pos > COL * ROW:
                die = True
        if next_pos in body:
            die = True
        if die:
            return None, None, None, -1
        body.append(next_pos)
        if not die:
            del body[0]
        x1, y1 = get_xy(next_pos)
        x2, y2 = get_xy(self.food_pos)
        return body, direction, action, self.get_score(x1, x2, y1, y2)
    
    def astar(self):
        directions = []
        actions = [(self.turn_side("none", self.direction),"none"),(self.turn_side("left", self.direction),"left"),(self.turn_side("right", self.direction),"right")]
        body = self.body.copy()
        while True:
            items = [self.simulate(action[1], body, action[0]) for action in actions]
            items = sorted(items, key = lambda x:x[3])
            
            if items[0][3] == -1 and items[1][3] == -1 and items[2][3] == -1:
                return directions
            
            for item in items:
                if item[3] == -1:
                    continue
                directions.append(item[2])
                if item[3] <= 0:
                    return directions
                actions = [(self.turn_side("none", item[1]),"none"),(self.turn_side("left", item[1]),"left"),(self.turn_side("right", item[1]),"right")]
                body = item[0]
                break
        
    # recursive version
    def astar2(self, body, direction, directions = []):
        actions = [(self.turn_side("none", direction),"none"),(self.turn_side("left", direction),"left"),(self.turn_side("right", direction),"right")]
        body = body.copy()
        
        items = [self.simulate(action[1], body, action[0]) for action in actions]
        items = sorted(items, key = lambda x:x[3])
            
        if items[0][3] == -1 and items[1][3] == -1 and items[2][3] == -1:
            del directions[-1]
            return False
            
        for item in items:
            if item[3] == -1:
                continue
            directions.append(item[2])
            if item[3] == 0:
                return True
            result = self.astar2(item[0], item[1], directions)
            if result:
                return True
            
        try:
            del directions[-1]
        except:
            return True
        
        return False
    
    def get_score(self, x1, x2, y1, y2):
        return 2 * (abs(x1-x2) + abs(y1-y2))
        
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
        self.flag = True
                
    def turn_side(self, key, direction):
        if key == "none":
            return direction
        elif key == "left":
            return (direction+3)%4
        elif key == "right":
            return (direction+1)%4
        
    def isEat(self):
        if self.body[-1] == self.food_pos:
            pos = random.randrange(0,ROW*COL)
            while pos in self.body:
                pos = random.randrange(0,ROW*COL)
            self.food_pos = pos
            self.eat = True
    
    def render(self):
        dx = 0
        if self.human:
            dx = WIDTH
        for i in range(COL):
            pygame.draw.line(screen, GREY, [dx + 10+i*30,0],[dx + 10+i*30,HEIGHT])
        
        for i in range(ROW):
            pygame.draw.line(screen, GREY, [dx + 0,10+i*30],[dx + WIDTH,10+i*30])
            
        pygame.draw.rect(screen, BLACK, [dx + 0,0,10,HEIGHT])
        pygame.draw.rect(screen, BLACK, [dx + 0,0,WIDTH, 10])
        pygame.draw.rect(screen, BLACK, [dx + 0,HEIGHT-10,WIDTH,10])
        pygame.draw.rect(screen, BLACK, [dx + WIDTH-10,0,10,HEIGHT])
        self.draw(self.food_pos, BLUE)
        self.draw_body()
        score = font.render("length : " + str(len(self.body)),True,(28,0,0))
        screen.blit(score, (WIDTH//2+dx, HEIGHT + 100))
        
#=============================================Main Loop==============================================#

env = Environment()
human = Environment(True)
env.reset()
human.reset()

font = pygame.font.Font(None,30)

action = 0
directions = []
while not env.done and not human.done:
    if not directions:
        #directions = env.astar()
        env.astar2(env.body, env.direction, directions)
        print(directions)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                human.turn(LEFT)
            elif event.key == K_RIGHT:
                human.turn(RIGHT)
            elif event.key == K_UP:
                human.turn(UP)
            elif event.key == K_DOWN:
                human.turn(DOWN)
            elif event.key == K_SPACE:
                start = True
                
    screen.fill(WHITE)
    if not start:
        continue
    try:
        action = directions[0]
    except:
        break
    del directions[0]
    d = env.turn_side(action, env.direction)
    
    env.step(d)
    #human.step(-1)
        
    env.render()
    human.render()
        
    pygame.display.update()
    clock.tick(FPS)
    
if human.done:
    print("Computer win")
else:
    print("Human win")