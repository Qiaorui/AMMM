
import random
import math

class Instance:
    """
    numNurses = 20;
    hours = 24;
    demand = [2 2 1 1 1 2 2 3 4 6 6 7 5 8 8 7 6 6 4 3 4 3 3 3];
    minHours = 5;
    maxHours = 9;
    maxConsec = 3;
    maxPresence = 14;
    hours >= maxHours >= minHours

hours >= maxPresence  >= maxHours >= maxConsec
minHours means nothing
mininium Nurse = demand.max * (hours / maxHours )
nurse * maxHours = demand.max * hours
20 * 9 = 8 * 24
hours >= demand.max * 2
demand.max * 2  -> MAX

maxPresence <= maxHours*2-2
    """

    def __init__(self, hours = 0):
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
        self.maxHours = random.randrange(max(self.hours//4, 3), self.hours // 1.5)
        self.numNurses = math.ceil(self.hours / 1.5) * math.ceil(self.hours / self.maxHours)
        self.maxPresence = random.randrange(self.maxHours + 1, min(self.maxHours * 2 - 1, self.hours))
        self.maxConsec = random.randrange(2, self.maxHours)
        self.minHours = random.randrange(1, self.maxHours)

    def __str__(self):
        return ("numNurses = {0};\n"
            "hours = {1};\n"
             "demand = {2};\n"
             "minHours = {3};\n"
             "maxHours = {4};\n"
             "maxConsec = {5};\n"
             "maxPresence = {6}").format(self.numNurses, self.hours, self.demand.__str__().replace(",", ""), self.minHours, self.maxHours,
                                         self.maxConsec, self.maxPresence)


    def __repr__(self):
        return self.__str__()
