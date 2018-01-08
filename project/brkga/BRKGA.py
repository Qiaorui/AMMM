import math
import numpy as np
import matplotlib.pyplot as plt
from Nurse_Scheduling import NurseScheduling
from timeit import default_timer as timer


def first_index_nonzero(numbers):
    for i, v in enumerate(numbers):
        if v > 0:
            return i
    return -1


class Brkga(NurseScheduling):

    def __init__(self, data=None):
        super().__init__(data)

    """
    ************************ Problem Independent Part ************************
    """

    @staticmethod
    def initialize_population(num_individuals, chr_length):
        population = []
        for i in range(num_individuals):
            chromosome = list(np.random.rand(chr_length))
            population.append({'chr': chromosome, 'solution': {}, 'fitness': None})
        return population
        
    @staticmethod
    def classify_individuals(population, num_elite):
        fitness = np.array([e['fitness'] for e in population])
        order = sorted(range(len(fitness)), key=lambda k: fitness[k])
        which_elite = order[0:num_elite]
        which_non_elite = order[num_elite:(len(fitness))]
        population = np.array(population)
        elite = population[which_elite]
        non_elite = population[which_non_elite]
        return list(elite), list(non_elite)
    
    @staticmethod
    def generate_mutant_individuals(num_mutants, chr_length):
        mutants = []
        for i in range(num_mutants):
            chromosome = list(np.random.rand(chr_length))
            mutants.append({'chr': chromosome, 'solution': {}, 'fitness': None})
        return mutants

    @staticmethod
    def do_crossover(elite, non_elite, ro, num_crossover):
        crossover = []
        for i in range(num_crossover):
            index_elite = int(math.floor(np.random.rand()*len(elite)))
            index_non_elite = int(math.floor(np.random.rand() * len(non_elite)))
            chr_elite = elite[index_elite]['chr']
            chr_non_elite = non_elite[index_non_elite]['chr']
            rnd = list(np.random.rand(len(chr_elite)))
            chr_cross = [chr_elite[i] if rnd[i] <= ro else chr_non_elite[i] for i in range(len(chr_elite))]
            crossover.append({'chr': chr_cross, 'solution': {}, 'fitness': None})
        return crossover

    @staticmethod
    def get_best_fitness(population):
        fitness = np.array([e['fitness'] for e in population])
        order = sorted(range(len(fitness)), key=lambda k: fitness[k])
        return population[order[0]]

    def solve(self, max_generations=100, num_individuals=10, elite_prop=0.1, mutant_prop=0.2,
              inheritance_prop=0.7, timeout=math.inf, verbose=False):
        start_process = timer()
        self.verbose = verbose

        # initializations
        num_elite = int(math.ceil(num_individuals * elite_prop))
        num_mutants = int(math.ceil(num_individuals * mutant_prop))
        num_crossover = max(num_individuals - num_elite - num_mutants, 0)

        self.combSize = min(self.maxPresence, (self.maxHours << 1) - 1)
        candidates = self.generate_combinations([1], self.combSize - 1, self.maxConsec - 1, self.maxHours - 1, False)
        candidates.sort(reverse=True)

        evol = []

        # Main body
        chr_length = self.get_chromosome_length(self.raw_data)

        population = self.initialize_population(num_individuals, chr_length)

        i = 0
        while i < max_generations and (i == 0 or timer() - start_process < timeout):
            if self.verbose:
                print(i)
            population = self.decode(population, self.raw_data, candidates)
            evol.append(self.get_best_fitness(population)['fitness'])
            if num_elite > 0:
                elite, non_elite = self.classify_individuals(population, num_elite)
            else:
                elite = []
                non_elite = population
            if num_mutants > 0:
                mutants = self.generate_mutant_individuals(num_mutants, chr_length)
            else:
                mutants = []
            if num_crossover > 0:
                crossover = self.do_crossover(elite, non_elite, inheritance_prop, num_crossover)
            else:
                crossover = []
            population = elite + crossover + mutants
            i += 1

        population = self.decode(population, self.raw_data, candidates)
        best_individual = self.get_best_fitness(population)
        if self.verbose:
            plt.plot(evol)
            plt.xlabel('number of generations')
            plt.ylabel('Fitness of best individual')
            plt.axis([0, len(evol), 0, self.numNurses * 1.1])
            plt.show()

        end_process = timer()
        solution = best_individual['solution']
        solution["found"] = True if solution["cost"] <= self.numNurses else False
        solution['time'] = end_process - start_process
        return solution

    """
    ************************ Problem Dependent Part: Decoder ************************
    """

    @staticmethod
    def get_chromosome_length(data):
        return data['numNurses'] * 2

    def decode(self, population, data, candidates):
        for ind in population:
            solution, fitness = self.decoder_assignment(data, ind['chr'], candidates)
            ind['solution'] = solution
            ind['fitness'] = fitness
        return population

    @staticmethod
    def update_demand(schedule, demand):
        new_demand = demand[:]
        for i, nurse in enumerate(schedule):
            for j, works in enumerate(nurse):
                if works:
                    new_demand[j] -= 1
        return new_demand

    def decoder_assignment(self, data, chromosome, candidates):
        chr_candidates = chromosome[0:self.numNurses]
        chr_pivot = chromosome[self.numNurses:]

        schedule = []
        candidates_size = len(candidates)
        comb_size = min(data['maxPresence'], (data['maxHours'] << 1) - 1)
        max_pivot = max(data['hours'] - comb_size, 0)
        pivot_segment = 1/self.hours
        candidate_segment = 1/candidates_size

        # schedule - chr_candidates - chr_pivot   They share same INDEX
        for c, p in zip(chr_candidates, chr_pivot):
            pivot = int(min(max(math.floor(p / pivot_segment) - comb_size/2, 0), max_pivot))
            s = int(min(math.floor(c / candidate_segment), candidates_size-1))
            schedule.append([0]*pivot + candidates[s] + [0] * (data['hours'] - pivot - comb_size))

        demand = self.update_demand(schedule, data['demand'])

        solution = self.clear_solution(schedule, demand)
        if sum([i for i in demand if i > 0]) > 0:
            solution['cost'] += self.numNurses

        return solution, solution['cost']

