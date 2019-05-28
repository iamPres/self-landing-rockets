class Grader:
    def __init__(self, tick):
        self.tick = tick
        self.threshold = ((0, 1), (self.tick.bounds.x/2-10, self.tick.bounds.x/2 + 10), self.tick.bounds.y - 10, False)
        self.Pass = False

    def calc_fitness(self, index):
        if self.tick.rockets[index].isDead[self.tick.latest_tick-1]:
            return 0
        else:
            fitness = self.tick.rockets[index].y[self.tick.latest_tick-1]
            return fitness

    @staticmethod
    def satisfy(data, _range):
        count = 0
        for i in data:
            if _range[0] < i < _range[1]:
                count += 1
        if count == len(data):
            return True

    @staticmethod
    def calc_fittest(mario):
        fitness = [i.fitness for i in mario]
        fittest = fitness.index(max(fitness))
        return fittest

    def complete(self):
        self.Pass = self.satisfy(self.tick.attributes[1], self.threshold)
        return self.Pass
