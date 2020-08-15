import pylab
import pygame
import random
import numpy as np
from pygame.locals import *
from agent import Agent

#=================================================Param==============================================#

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
GREEN = (  0,255,  0)
RED   = (255,  0,  0)
GREY  = (128,128,128)

TILE_SIZE = (30,30)
ROW = 9
COL = 9
WIDTH = 20+30*COL
HEIGHT = 20+30*ROW

LEFT  = 0
UP    = 1
RIGHT = 2
DOWN  = 3

EPISODE = 10000

#================================================Init================================================#

size = [WIDTH,HEIGHT]
screen = pygame.display.set_mode(size)
screen2 = pygame.display.set_mode(size)

pygame.init()
pygame.display.set_caption("Snake Game")
done = False
clock = pygame.time.Clock()

FPS = 7
render = True
train = True

#============================================Class, Function========================================#

def get_xy(pos):
    return (pos%COL, pos//COL)

def get_pos(x, y):
    return x * COL + y

class Environment:
    def __init__(self):
        self.direction = RIGHT
        self.body = [ROW * COL // 4 + 2]
        self.length = len(self.body)
        self.die = False
        self.win = False
        self.eat = False
        self.done = self.win or self.die
        self.food_pos = ROW*COL//3
        self.flag = False
    
    def reset(self):
        self.direction = RIGHT
        self.body = [ROW*COL // 4 + 2]
        self.length = len(self.body)
        self.die = False
        self.win = False
        self.eat = False
        self.done = self.win or self.die
        self.food_pos = ROW*COL//3
    
    def draw(self, pos, color):
        (x, y) = get_xy(pos)
        pygame.draw.rect(screen, color, [10+30*x,10+30*y,31,31])
    
    def draw_body(self):
        for i in self.body:
            self.draw(i, GREEN)
    
    def step(self, action):
        if train:
            if action == 0:
                self.turn_side("left")
            elif action == 1:
                self.turn_side("none")
            elif action == 2:
                self.turn_side("right")
        else:
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
        
        reward = 0
        if self.die:
            reward = -0.5
        elif self.eat:
            reward = 1
        elif self.win:
            pass
        else:
            reward = -0.05
            
        return self.get_state(), reward, self.done        
        
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
                
    def turn_side(self, key):
        if key == "none":
            return
        elif key == "left":
            self.direction -= 1
            if self.direction < 0:
                self.direction = DOWN
        elif key == "right":
            self.direction = (self.direction+1)%4
        
    def isEat(self):
        if self.body[-1] == self.food_pos:
            pos = random.randrange(0,ROW*COL)
            while pos in self.body:
                pos = random.randrange(0,ROW*COL)
            self.food_pos = pos
            self.eat = True
    
    def render(self):
        for i in range(COL):
            pygame.draw.line(screen, GREY, [10+i*30,0],[10+i*30,HEIGHT])
        
        for i in range(ROW):
            pygame.draw.line(screen, GREY, [0,10+i*30],[WIDTH,10+i*30])
            
        pygame.draw.rect(screen, BLACK, [0,0,10,HEIGHT])
        pygame.draw.rect(screen, BLACK, [0,0,WIDTH, 10])
        pygame.draw.rect(screen, BLACK, [0,HEIGHT-10,WIDTH,10])
        pygame.draw.rect(screen, BLACK, [WIDTH-10,0,10,HEIGHT])
        self.draw(self.food_pos, BLUE)
        self.draw_body()
        
    def get_state(self):
        state = np.zeros((ROW,COL))
        for i in range(len(self.body)):
            if self.body[i]>=ROW*COL:
                self.body[i] = ROW*COL-1
            y, x = get_xy(self.body[i])
            if i==1:
                state[y][x] = self.direction + 2
            else:
                state[y][x] = 1
        y, x = get_xy(self.food_pos)

        state[y][x] = 6
        state = np.expand_dims(state, 2)
        #direction_state = np.ones((ROW,COL)) * (self.direction + 1)
        #state = np.expand_dims(state, 2)
        #direction_state = np.expand_dims(direction_state,2)
        #state = np.concatenate((state, direction_state),2)
        
        return state
        
#=============================================Main Loop==============================================#

env = Environment()
ai = Agent((ROW, COL), 3)

for ep in range(EPISODE):
    scores, episodes = [], []
    env.reset()
    score = 0
    
    state = env.get_state()
    state = np.reshape(state, [1,state.shape[0],state.shape[1],state.shape[2]])
    
    while not env.done:
        if not train:
            for event in pygame.event.get():
                if event.type == KEYDOWN and not env.flag:
                    if event.key == K_LEFT:
                        action = LEFT
                    elif event.key == K_RIGHT:
                        action = RIGHT
                    elif event.key == K_UP:
                        action = UP
                    elif event.key == K_DOWN:
                        action = DOWN
            
        screen.fill(WHITE)
        
        action = ai.get_action(state)
        next_state, reward, done = env.step(action)
        next_state = np.reshape(next_state, [1,next_state.shape[0],next_state.shape[1],next_state.shape[2]])
        
        ai.append_sample(state, action, reward, next_state, done)
        
        if len(ai.memory) >= ai.train_start:
            ai.train_model()
        
        score+=reward
        state = next_state
        
        if render:
            env.render()
                
        pygame.display.update()
        clock.tick(FPS)
        
    ai.update_target_model()
    scores.append(score)
    episodes.append(ep)
    pylab.plot(episodes, scores, 'b')
    pylab.savefig("graph/snake.png")
    print("episode:",ep," score:",score, " memory length:",len(ai.memory)," epsilon:",ai.epsilon)
    ai.model.save_weights("model.h5")
    
    #if env.die:
    #    print("good bye")
    #elif env.win:
    #    print("you win")