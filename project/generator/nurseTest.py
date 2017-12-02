
import random

class Instance:
    """
    numNurses = 20
    hours
    demand = [2 2 1 1 1 2 2 3 4 6 6 7 5 8 8 7 6 6 4 3 4 3 3 3];
    minHours = 5;
    maxHours = 9;
    maxConsec = 3;
    maxPresence = 14;
    """

    def __init__(self, numNurses = 1, hours = 1):
        self.numNurses = numNurses
        self.hours = hours
        self.demand = [0] * hours
        self.minHours = 1
        self.maxHours = 1
        self.maxConsec = 1
        self.maxPresence = 1

    def random(self):
        self.demand = [int(self.numNurses*random.random()) for i in range(self.hours)]

    def print(self):
        print("numNurses =", self.numNurses)
        print("hours =", self.hours)
        print("demand =", self.demand)
        print("minHours =", self.minHours)
        print("maxHours =", self.maxHours)
        print("maxConsec =", self.maxConsec)
        print("maxPresence =", self.maxPresence)
