import numpy as np
import random
from collections import deque
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from keras.optimizers import RMSprop, Adam
from keras.models import Sequential

class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        self.discount_factor = 0.99
        self.learning_rate = 0.001
        self.epsilon = 0.29952413540366546
        self.epsilon_decay = 0.9999
        self.epsilon_min = 0.01
        self.batch_size = 128
        self.train_start = 500
        
        self.memory = deque(maxlen = 2000)
        
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.model.load_weights("model.h5")
        self.target_model.load_weights("model.h5")
        
    def build_model(self):
        model = Sequential()
        model.add(Conv2D(32,(3,3),input_shape = (self.state_size[0], self.state_size[1], 1), kernel_initializer="he_uniform"))
        model.add(Dropout(0.5))
        model.add(Conv2D(32,(3,3), kernel_initializer="he_uniform"))
        model.add(Dropout(0.5))
        model.add(Flatten())
        model.add(Dense(256, kernel_initializer="he_uniform"))
        model.add(Dense(256,kernel_initializer="he_uniform"))
        model.add(Dense(self.action_size, activation = "linear"))
        model.summary()
        model.compile(loss = "mse", optimizer = Adam(lr = self.learning_rate))
        return model
    
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())
        
    def get_action(self, state):
        if np.random.randn() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            q_value = self.model.predict(state)
            return np.argmax(q_value[0])
        
    def append_sample(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def train_model(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        mini_batch = random.sample(self.memory, self.batch_size)
        
        states = np.zeros((self.batch_size, self.state_size[0], self.state_size[1],1))
        next_states = np.zeros((self.batch_size, self.state_size[0],self.state_size[1],1))
        actions, rewards, dones = [], [], []
        
        for i in range(self.batch_size):
            states[i] = mini_batch[i][0][0]
            actions.append(mini_batch[i][1])
            rewards.append(mini_batch[i][2])
            next_states[i] = mini_batch[i][3][0]
            dones.append(mini_batch[i][4])
            
        target = self.model.predict(states)
        target_val = self.target_model.predict(next_states)
        
        for i in range(self.batch_size):
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                target[i][actions[i]] = rewards[i] + self.discount_factor * (np.amax(target_val[i]))
                
        self.model.fit(states, target, batch_size=self.batch_size, epochs=1,verbose = 0)
