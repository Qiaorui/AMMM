import math
import random
from timeit import default_timer as timer


def first_index_nonzero(numbers):
    for i, v in enumerate(numbers):
        if v > 0:
            return i
    return -1


class Grasp:

    def __init__(self, config=None):
        self.numNurses, self.hours, self.demand, self.minHours, self.maxHours, self.maxConsec, self.maxPresence, \
            self.combSize = (0,)*8
        self.verbose = False
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

    def fill_combinations(self, comb, remaining_size, remaining_consec, remaining_time, rest):
        candidates = []
        if not remaining_size:
            if self.maxHours - remaining_time >= self.minHours:
                comb2 = comb[:]
                candidates.append(comb)
                if comb2[-1] == 0:
                    comb2.insert(0, comb2.pop())
                    candidates.append(comb2)
        elif not remaining_time:
            comb.extend([0] * remaining_size)
            candidates.append(comb[:])
            while comb[-1] == 0:
                comb.insert(0, comb.pop())
                candidates.append(comb[:])
        elif not remaining_consec:
            comb.append(0)
            candidates.extend(
                self.fill_combinations(comb, remaining_size - 1, self.maxConsec, remaining_time, True))
        elif rest:
            comb.append(1)
            candidates.extend(
                self.fill_combinations(comb, remaining_size - 1, remaining_consec - 1, remaining_time - 1, False))
        else:
            comb2 = comb[:]
            comb.append(0)
            candidates.extend(
                self.fill_combinations(comb, remaining_size - 1, self.maxConsec, remaining_time, True))
            comb2.append(1)
            candidates.extend(
                self.fill_combinations(comb2, remaining_size - 1, remaining_consec - 1, remaining_time - 1, False))

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
        acc = 0
        for i, works in enumerate(nurse):
            if works and demand[i] > 0:
                acc += demand[i]
        return acc

    @staticmethod
    def generate_rcl(costs, threshold):
        return [i for i, x in enumerate(costs) if x >= threshold]

    def clear_solution(self, schedule, demand):
        surplus = []
        for i, nurse in enumerate(schedule):
            found = all([k < 0 for j, k in zip(nurse, demand) if j])
            if found:
                for j, works in enumerate(nurse):
                    if works:
                        demand[j] += 1
                surplus.append(i)
        surplus.sort(reverse=True)
        for index in surplus:
            del schedule[index]
        return self.generate_solution(schedule, demand)

    def generate_solution(self, schedule, demand):
        return {"schedule": schedule, "cost": self.cost(schedule), "demand": demand}

    def evaluate_candidates(self, start, stop, candidates, demand):
        sub_demand = demand[start:stop]
        return [self.evaluate_greedy_cost(x, sub_demand) for x in candidates]

    def construct_schedule(self, demand, candidates, alpha):
        schedule = []
        pos = first_index_nonzero(demand)
        pos = min(pos, self.hours - self.combSize)
        while pos != -1:
            # Update greedy costs
            candidate_costs = self.evaluate_candidates(pos, pos + self.combSize, candidates, demand)
            smin = min(candidate_costs)
            smax = max(candidate_costs)
            rcl = self.generate_rcl(candidate_costs, smax - alpha * (smax - smin))

            assignment = candidates[random.choice(rcl)]
            schedule.append([0] * pos + assignment + [0] * (self.hours - pos - self.combSize))
            # Update remaining demand
            for i in range(pos, pos + self.combSize):
                demand[i] -= assignment[i - pos]
            if self.verbose:
                print(demand)

            # Update position
            pos = first_index_nonzero(demand)
            pos = min(pos, self.hours - self.combSize)
        return schedule

    def greedy_randomized_construction(self, candidates, alpha):
        demand = self.demand[:]
        schedule = self.construct_schedule(demand, candidates, alpha)
        return self.generate_solution(schedule, demand)

    @staticmethod
    def construct_neighbor(old_schedule, old_demand, alpha):
        schedule = [x[:] for x in old_schedule]
        demand = old_demand[:]

        # Evaluate efficiency for each assignment
        schedule_costs = [0] * len(schedule)
        for i, nurse in enumerate(schedule):
            schedule_costs[i] = sum([k == 0 for j, k in zip(nurse, demand) if j])

        smin = min(schedule_costs)
        smax = max(schedule_costs)
        threshold = smin + alpha * (smax - smin)

        # Remove assignment which are less efficient and update remaining demand
        remove_list = []
        for i, x in enumerate(schedule_costs):
            if x > threshold:
                remove_list.append(i)
        remove_list.sort(reverse=True)
        for index in remove_list:
            for i, works in enumerate(schedule[index]):
                if works:
                    demand[i] += 1
            del schedule[index]

        return schedule, demand

    def local_search(self, candidates, solution, alpha):
        # Remove less efficient assignment
        new_schedule, new_demand = self.construct_neighbor(solution['schedule'], solution['demand'], alpha)
        # Do greedy construction with removed demand and merge
        new_schedule.extend(self.construct_schedule(new_demand, candidates, alpha))

        new_solution = self.clear_solution(new_schedule, new_demand)
        # If new solution has better cost, then update
        if new_solution['cost'] < solution['cost']:
            return new_solution
        else:
            return solution

    def initialize_candidates(self):
        self.combSize = min(self.maxPresence, (self.maxHours << 1) - 1)
        candidates = self.fill_combinations([1], self.combSize-1, self.maxConsec-1, self.maxHours-1, False)
        return candidates

    def solve(self, remaining_iterations=1000, alpha=0.25, seed=1, config=None, timeout=math.inf, verbose=False):
        start_process = timer()

        self.verbose = verbose
        random.seed(seed)
        if config:
            self.read_input(config)
        candidates = self.initialize_candidates()
        if self.verbose:
            print("candidates size: ", len(candidates))

        opt = {"cost": math.inf}
        while remaining_iterations and ('schedule' not in opt or timer() - start_process < timeout):
            sol = self.greedy_randomized_construction(candidates, alpha)
            sol = self.local_search(candidates, sol, alpha/2)
            if sol["cost"] < opt["cost"]:
                opt = sol
            remaining_iterations -= 1
        opt["found"] = True if opt["cost"] <= self.numNurses else False

        end_process = timer()
        opt['time'] = round(end_process - start_process, 3)

        return opt
