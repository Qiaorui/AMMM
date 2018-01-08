import math
import numpy as np
import matplotlib.pyplot as plt
from Nurse_Scheduling import NurseScheduling
from timeit import default_timer as timer


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

    def solve(self, max_generations=100, num_individuals=50, elite_prop=0.1, mutant_prop=0.2,
              inheritance_prop=0.7, timeout=math.inf, verbose=False):
        start_process = timer()
        self.verbose = verbose

        # initializations
        num_elite = int(math.ceil(num_individuals * elite_prop))
        num_mutants = int(math.ceil(num_individuals * mutant_prop))
        num_crossover = max(num_individuals - num_elite - num_mutants, 0)

        self.combSize = min(self.maxPresence, (self.maxHours << 1) - 1)
        candidates = self.generate_combinations([1], self.combSize - 1, self.maxConsec - 1, self.maxHours - 1, False)

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
        candidates_size = len(candidates)
        comb_size = self.combSize
        max_pivot = max(self.hours - comb_size, 0)
        pivot_segment = 1/self.hours
        candidate_segment = 1/candidates_size

        for ind in population:
            solution, fitness = self.decoder_assignment(ind['chr'], candidates, pivot_segment, comb_size, max_pivot,
                                                        candidate_segment, candidates_size)
            ind['solution'] = solution
            ind['fitness'] = fitness
        return population

    def decoder_assignment(self, chromosome, candidates, pivot_segment, comb_size, max_pivot,
                           candidate_segment, candidates_size):
        chr_candidates = chromosome[0:self.numNurses]
        chr_pivot = chromosome[self.numNurses:]
        demand = self.demand[:]

        schedule = []

        for c, p in zip(chr_candidates, chr_pivot):
            pivot = int(min(max(math.floor(p / pivot_segment) - comb_size/2, 0), max_pivot))
            s = int(min(math.floor(c / candidate_segment), candidates_size-1))
            assignment = candidates[s]
            for i in range(comb_size):
                demand[pivot + i] -= assignment[i]
            schedule.append([0]*pivot + assignment + [0] * (self.hours - pivot - comb_size))

        solution = self.generate_solution(schedule, demand)
        remaining_demand = sum([i for i in demand if i > 0])
        if remaining_demand > 0:
            solution['cost'] += remaining_demand
        else:
            solution = self.clear_solution(schedule, demand)

        return solution, solution['cost']

