import math
import random


def first_index_nonzero(numbers):
    for i, v in enumerate(numbers):
        if v:
            return i
    return -1


class Grasp:

    def __init__(self, config={}):
        self.numNurses, self.hours, self.demand, self.minHours, self.maxHours, self.maxConsec, self.maxPresence, self.combSize = (0,)*8
        if config:
            self.read_input(config)

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

    def read_input(self, config):
        self.numNurses = config["numNurses"]
        self.hours = config["hours"]
        self.demand = config["demand"]
        self.minHours = config["minHours"]
        self.maxHours = config["maxHours"]
        self.maxConsec = config["maxConsec"]
        self.maxPresence = config["maxPresence"]

    def fill_combinations(self, comb, remaning_size, remaining_consec, remaining_time, rest):
        candidates = []
        if not remaning_size:
            if self.maxHours - remaining_time > self.minHours:
                comb2 = comb[:]
                candidates.append(comb)
                if comb2[-1] == 0:
                    comb2.insert(0, comb2.pop())
                    candidates.append(comb2)
        elif not remaining_time:
            comb.extend([0] * remaning_size)
            candidates.append(comb[:])
            while comb[-1] == 0:
                comb.insert(0, comb.pop())
                candidates.append(comb[:])
        elif not remaining_consec:
            comb.append(0)
            candidates.extend(self.fill_combinations(comb, remaning_size-1, self.maxConsec, remaining_time, True))
        elif rest:
            comb.append(1)
            candidates.extend(self.fill_combinations(comb, remaning_size-1, remaining_consec-1, remaining_time-1, False))
        else:
            comb2 = comb[:]
            comb.append(0)
            candidates.extend(self.fill_combinations(comb, remaning_size-1, self.maxConsec, remaining_time, True))
            comb2.append(1)
            candidates.extend(self.fill_combinations(comb2, remaning_size-1, remaining_consec-1, remaining_time-1, False))

        return candidates

    @staticmethod
    def cost(schedule):
        if not schedule:
            return math.inf
        used = 0
        for nurse in schedule:
            for h in nurse:
                if h:
                    used += 1
                    break
        return used

    @staticmethod
    def evaluate_greedy_cost(nurse, demand):
        return sum([i * j for i, j in zip(nurse, demand)])

    @staticmethod
    def generate_rcl(costs, threshold):
        return [i for i, x in enumerate(costs) if x >= threshold]

    def generate_solution(self, schedule):
        return {"schedule": schedule, "cost": self.cost(schedule)}

    def evaluate_candidates(self, start, stop, candidates, demand):
        sub_demand = demand[start:stop]
        return [self.evaluate_greedy_cost(x, sub_demand) for x in candidates]

    def greedy_randomized_construction(self, candidates, alpha):
        schedule = []
        demand = self.demand[:]
        pos = first_index_nonzero(demand)
        while pos != -1:
            # Update greedy costs
            candidate_costs = self.evaluate_candidates(pos, pos + self.combSize, candidates, demand)
            smin = min(candidate_costs)
            smax = max(candidate_costs)
            rcl = self.generate_rcl(candidate_costs, smax - alpha*(smax - smin))
            assignment = candidates[random.choice(rcl)]
            schedule.append([0]*pos + assignment + [0]*(self.hours-pos-self.combSize))
            # Update remaining demand
            for i in range(pos, pos+self.combSize):
                if demand[i]:
                    demand[i] -= assignment[i-pos]

            # Update position
            pos = first_index_nonzero(demand)
            pos = min(pos, self.hours - self.combSize)

        return self.generate_solution(schedule)

    def local_search(self, solution):

        return solution

    def initialize_cantidates(self):
        self.combSize = min(self.maxPresence, (self.maxHours << 1) - 1)
        candidates = self.fill_combinations([1], self.combSize-1, self.maxConsec-1, self.maxHours-1, False)
        return candidates

    def solve(self, remaining_iterations=10000, alpha=0.25, seed=1, config={}):
        random.seed(seed)
        if config:
            self.read_input(config)
        candidates = self.initialize_cantidates()

        opt = {"cost": math.inf}
        while remaining_iterations:
            sol = self.greedy_randomized_construction(candidates, alpha)
            sol = self.local_search(sol)
            if sol["cost"] < opt["cost"]:
                opt = sol
            remaining_iterations -= 1
        opt["found"] = True if opt["cost"] <= self.numNurses else False
        return opt
