import math
import random
from timeit import default_timer as timer
from Nurse_Scheduling import NurseScheduling


def first_index_nonzero(numbers):
    for i, v in enumerate(numbers):
        if v > 0:
            return i
    return -1


class Grasp(NurseScheduling):

    def __init__(self, data=None):
        super().__init__(data)

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

    def evaluate_candidates(self, start, stop, candidates, demand):
        sub_demand = demand[start:stop]
        return [self.evaluate_greedy_cost(x, sub_demand) for x in candidates]

    def construct_schedule(self, demand, candidates, alpha):
        schedule = []
        pivot = first_index_nonzero(demand)
        pivot = min(pivot, self.hours - self.combSize)
        while pivot != -1:
            # Update greedy costs
            candidate_costs = self.evaluate_candidates(pivot, pivot + self.combSize, candidates, demand)
            smin = min(candidate_costs)
            smax = max(candidate_costs)
            rcl = self.generate_rcl(candidate_costs, smax - alpha * (smax - smin))

            assignment = candidates[random.choice(rcl)]
            schedule.append([0] * pivot + assignment + [0] * (self.hours - pivot - self.combSize))
            # Update remaining demand
            for i in range(pivot, pivot + self.combSize):
                demand[i] -= assignment[i - pivot]
            #if self.verbose:
                #print(demand)

            # Update position
            pivot = first_index_nonzero(demand)
            pivot = min(pivot, self.hours - self.combSize)
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
        new_schedule, new_demand = self.construct_neighbor(solution['schedule'], solution['demand'], alpha/2)
        # Do greedy construction with removed demand and merge
        new_schedule.extend(self.construct_schedule(new_demand, candidates, 0))

        new_solution = self.clear_solution(new_schedule, new_demand)
        # If new solution has better cost, then update
        if new_solution['cost'] < solution['cost']:
            return new_solution
        else:
            return solution

    def initialize_candidates(self):
        self.combSize = min(self.maxPresence, (self.maxHours << 1) - 1)
        candidates = self.generate_combinations([1], self.combSize - 1, self.maxConsec - 1, self.maxHours - 1, False)
        return candidates

    def solve(self, remaining_iterations=1000, alpha=0.25, seed=1, data=None, timeout=math.inf, verbose=False):
        start_process = timer()

        self.verbose = verbose
        random.seed(seed)
        if data:
            self.read_input(data)
        candidates = self.initialize_candidates()
        if self.verbose:
            print("candidates size: ", len(candidates))

        opt = {"cost": math.inf}
        while remaining_iterations and ('schedule' not in opt or timer() - start_process < timeout):
            sol = self.greedy_randomized_construction(candidates, alpha)
            sol = self.local_search(candidates, sol, alpha)
            if sol["cost"] < opt["cost"]:
                opt = sol
            if self.verbose:
                print(remaining_iterations, ': sol=', sol['cost'], ' opt=', opt['cost'])
            remaining_iterations -= 1
        opt["found"] = True if opt["cost"] <= self.numNurses else False

        end_process = timer()
        opt['time'] = round(end_process - start_process, 3)

        return opt
