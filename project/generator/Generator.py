import random
import math


class Instance:

    def __init__(self, hours=0):
        self.numNurses = 1
        self.hours = hours
        self.demand = [0] * hours
        self.minHours = 1
        self.maxHours = 1
        self.maxConsec = 1
        self.maxPresence = 1
        if hours > 0:
            self.random()

    def random(self):
        self.demand = [int(self.hours/1.5*random.random()) for i in range(self.hours)]
        self.maxHours = random.randrange(min(max(self.hours//4, 3), 10), min(self.hours // 1.5, 20))
        self.numNurses = int(max(self.demand) * self.hours / self.maxHours * 1.5)
        self.maxPresence = random.randrange(self.maxHours + 1, min(self.maxHours * 2 - 1, self.hours, 24))
        self.minHours = random.randrange(1, self.maxHours)
        self.maxConsec = random.randrange(max(math.ceil(self.minHours / (self.maxPresence - self.minHours)), 2), self.maxHours)


    def __str__(self):
        return ("numNurses = {0};\n"
                "hours = {1};\n" 
                "demand = {2};\n"
                "minHours = {3};\n"
                "maxHours = {4};\n"
                "maxConsec = {5};\n"
                "maxPresence = {6};").format(self.numNurses, self.hours, self.demand.__str__().replace(",", ""),
                                             self.minHours, self.maxHours, self.maxConsec, self.maxPresence)

    def __repr__(self):
        return self.__str__()
