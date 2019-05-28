import pygame
import sys
from Rocket import Rocket
from Grader import Grader
from GeneticTrainer import GeneticTrainer
from GameTickPacket import GameTickPacket
from Plotter import Plotter


class GameManager:
    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        self.ga = GeneticTrainer()
        self.bounds = (640, 480)
        self.fittest_index = 0
        self.screen = pygame.display.set_mode(self.bounds, 0, 32)
        self.pop = 10
        self.rockets = [Rocket(self.bounds, (self.bounds[0] / 2 - 35, 0)) for _ in range(self.pop)]
        self.tick = GameTickPacket(self.rockets)
        self.grader = Grader(self.tick)
        self.running = True
        self.clock = pygame.time.Clock()
        self.bot = 0
        self.num_best = 8
        self.gen = 0
        self.gen_cap = 1000
        self.timeout = 100
        self.running = True
        self.plotter = Plotter()

    def draw(self):

        self.pygame.display.update()
        self.clock.tick(60)
        # self.drawText("GEN: " + str(self.gen), 10, 10, 10)
        # self.drawText("BOT: " + str(self.bot), 10, 10, 10)

    def drawText(self, text, x, y, size):
        for char in text:
            charSprite = self.pygame.transform.scale(self.charSprites[char], (size, size))
            self.screen.blit(charSprite, (x, y))
            if char == " ":
                x += size // 2
            else:
                x += size

    def run(self):
        while self.running:
            while self.gen < self.gen_cap:

                self.bot = 0

                while self.bot < self.pop:
                    while not self.rockets[self.bot].isDead:
                        for event in self.pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()

                        x, y = self.rockets[self.bot].draw_rocket()
                        self.screen.fill((246, 246, 246))
                        self.screen.blit(self.rockets[self.bot].ball, (x, y))
                        self.draw()

                        self.tick.update(self.bot)

                        if self.tick.latest_tick > self.timeout:
                            self.rockets[self.bot].timeout()
                            break

                    #self.plotter.show(self.tick.rockets[self.fittest_index].thrust)
                    self.rockets[self.bot].fitness = self.grader.calc_fitness(self.bot)
                    self.tick.reset()

                    for i in self.rockets:
                        i.isDead = False

                    print(str(self.gen) + " | " + str(self.bot) + " | " + str(
                        sum(sum(self.rockets[self.bot].model.fc1.weight.data))) + " | " +
                          str(self.rockets[self.bot].fitness))

                    self.bot += 1

                print("-----------------")
                print("FITTEST: " + str(self.fittest_index) + " | " +
                      str(sum(sum(self.rockets[self.fittest_index].model.fc1.weight.data))))
                print("-----------------")
                self.fittest_index = self.grader.calc_fittest(self.rockets)
                self.ga.clone(self.rockets, self.fittest_index)
                self.ga.mutate(self.rockets, self.num_best)
                self.gen += 1
