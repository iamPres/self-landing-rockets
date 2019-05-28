import os
import sys, pygame
import torch
from Model import Model
import math
import numpy as np

class Rocket:
    def __init__(self, bounds, pos):
        self.model = Model().share_memory()
        self.pos = pos
        self.pygame = pygame
        self.size = self.width, self.height = bounds[0], bounds[1]
        self.x, self.y = self.pos
        self.fitness = 0
        self.ball = pygame.transform.scale(pygame.image.load('rocket.png'), (70, 70))
        self.gravityAcceleration = 0.3
        self.horizontalAcceleration = 0
        self.verticalSpeed = [0, 0]
        self.horizontalSpeed = [0, 0]
        self.ballrect = self.ball.get_rect()
        self.isDead = False
        self.thrust_direction = 0
        self.thrust_power = 0

    def thrust(self, out):
        self.thrust_direction = out[0]
        self.thrust_power = out[1]
        self.verticalSpeed[1] -= np.float(math.fabs(self.thrust_power))

    def get_inputs(self):
        inputs = [self.x, self.y, self.verticalSpeed[0], self.horizontalSpeed[0], self.horizontalAcceleration]
        return inputs

    def run_net(self):
        return self.model.forward(torch.FloatTensor(self.get_inputs()))

    def physics(self):
        self.verticalSpeed[0] = self.gravityAcceleration + self.verticalSpeed[1]
        self.y += self.verticalSpeed[0]
        self.verticalSpeed[1] = self.verticalSpeed[0]

        self.horizontalSpeed[0] = self.horizontalAcceleration + self.horizontalSpeed[1]
        self.x += self.horizontalSpeed[0]
        self.horizontalSpeed[1] = self.horizontalSpeed[0]

    def draw_rocket(self):
        self.physics()
        self.thrust(self.run_net())

        if self.y > self.height-70 or self.y < -70:
            self.die()

        return self.x, self.y

    def timeout(self):
        self.x = self.pos[0]
        self.y = 0
        self.verticalSpeed = [0, 0]
        self.horizontalSpeed = [0, 0]
        self.gravityAcceleration = 0.3
        self.horizontalAcceleration = 0

    def die(self):
        self.timeout()
        self.isDead = True
