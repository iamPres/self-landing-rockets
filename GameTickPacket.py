class GameTickPacket:
    def __init__(self, bots):
        self.bots = bots
        self.rockets = [rockets()] * len(self.bots)
        self.bounds = bounds()
        self.latest_tick = 0
        self.attributes = [None, None]

    def update(self, index):
        self.rockets[index].verticalSpeed.append(self.bots[index].verticalSpeed[0])
        self.rockets[index].horizontalSpeed.append(self.bots[index].horizontalSpeed[0])
        self.rockets[index].x.append(self.bots[index].x)
        self.rockets[index].y.append(self.bots[index].y)
        self.rockets[index].isDead.append(self.bots[index].isDead)
        self.rockets[index].thrust.append(self.bots[index].thrust_power)
        self.attributes[0] = self.bounds.attributes
        self.attributes[1] = self.rockets[index].attributes
        # print(self.attributes)
        self.latest_tick += 1

    def reset(self):
        self.__init__(self.bots)


class rockets:
    def __init__(self):
        self.verticalSpeed = []
        self.x = []
        self.y = []
        self.horizontalSpeed = []
        self.thrust = []
        self.isDead = []
        self.attributes = [self.verticalSpeed, self.x, self.y, self.horizontalSpeed, self.thrust, self.isDead]


class bounds:
    def __init__(self):
        self.x = 640
        self.y = 480
        self.attributes = (self.x, self.y)
