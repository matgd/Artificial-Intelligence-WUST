from random import shuffle, randint, random

import functions
import greedy_algorithm
from selection import *


# Wybieramy tylko jeden przedmiot w każdym mieście (albo żaden)
# Px [0,5; 1] - można spróbować -> [0,2; 1]
# Pm [0,01; 0,1] - dla odważnych -> [0,3; 0,6]
# Po krzyżowaniu i mutowaniu zbieramy przedmioty


class GeneticAlgorithm:
    def __init__(self, metadata: dict, nodes: dict, items: dict):
        self.metadata = metadata
        self.KNAPSACK_CAPACITY = int(metadata['CAPACITY OF KNAPSACK'])
        self.MIN_SPEED = float(metadata['MIN SPEED'])
        self.MAX_SPEED = float(metadata['MAX SPEED'])
        self.knapsack_free_space = int(metadata['CAPACITY OF KNAPSACK'])
        self.nodes = nodes
        self.items = items
        self.population = []

    def generate_random_node_specimen(self):
        specimen = [*self.nodes.values()]
        shuffle(specimen)
        return specimen

    def generate_specimen_with_score(self):
        generated_specimen = self.generate_random_node_specimen()
        items_assigned = self.assign_items_to_specimen(generated_specimen)
        specimen_score = self.G(generated_specimen, items_assigned)
        return specimen_score, generated_specimen

    def assign_score_to_specimen(self, specimen):
        items_assigned = self.assign_items_to_specimen(specimen)
        specimen_score = self.G(specimen, items_assigned)
        return specimen_score, specimen

    def generate_node_population(self, population_size=100):
        for i in range(population_size):
            self.population.append(self.generate_specimen_with_score())

    def assign_items_to_specimen(self, specimen):
        return greedy_algorithm.execute(specimen, self)

    def G(self, x, y):
        """
        Function that should be maximized.
        :param x: list of Nodes: Specimen
        :param y: dict: Items to take by specimen
        :return: float: Function value
        """
        return functions.func_g(y) - functions.genetic_func_f(x, self)

    def order_1_crossover(self, parent_1, parent_2, elitarism=False):
        """ http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/Order1CrossoverOperator.aspx """
        parent_1_copy = parent_1.copy()
        parent_2_copy = parent_2.copy()

        specimen_length = len(parent_1)

        cut_points = [randint(0, specimen_length - 1), randint(0, specimen_length - 1)]
        cut_point_1 = min(cut_points)
        cut_point_2 = max(cut_points)

        child_1 = [None for _ in range(specimen_length)]
        child_2 = [None for _ in range(specimen_length)]

        parent_1_swath = parent_1[cut_point_1:cut_point_2]
        parent_2_swath = parent_2[cut_point_1:cut_point_2]

        child_1[cut_point_1:cut_point_2] = parent_1_swath
        child_2[cut_point_1:cut_point_2] = parent_2_swath

        for node in parent_1_swath:
            parent_2_copy.remove(node)

        for node in parent_2_swath:
            parent_1_copy.remove(node)

        for i in range(0, cut_point_1):
            child_1[i] = parent_2_copy[i]
            child_2[i] = parent_1_copy[i]

        for i in range(cut_point_2, specimen_length):
            child_1[i] = parent_2_copy[i - len(parent_1_swath)]
            child_2[i] = parent_1_copy[i - len(parent_1_swath)]

        return child_1, child_2

    def swap_mutation(self, specimen):
        # index_1 = randint(0, len(specimen) - 1)
        # index_2 = randint(index_1 + 1, len(specimen))

        index_1 = randint(0, len(specimen) - 1)
        index_2 = index_1
        while index_2 == index_1:
            index_2 = randint(0, len(specimen) - 1)

        specimen[index_1], specimen[index_2] = specimen[index_2], specimen[index_1]

        return specimen

    def execute(self, selection, pop_size=100, gen=100, Px=0.7, Pm=0.01, verbose=False,
                return_chart_data=False):
        """
        Execute Genetic Algorithm.
        :param pop_size: Population size
        :param gen: Number of generations
        :param Px: Crossover propability
        :param Pm: Mutation propability
        :param selection: Selection algorithm
        :param verbose: Print output
        :return: Best solution, tuple of chart data
        """
        self.population.clear()
        self.generate_node_population(pop_size)
        if return_chart_data:
            chart_data_gen = []
            chart_data_best = []
            chart_data_avg = []
            chart_data_worst = []

        if verbose: print(f'Generated population of {pop_size}')

        best_solution = None
        for i in range(gen):
            if verbose: print(f'Generation number: {i + 1}', end=', ')
            if return_chart_data: chart_data_gen.append(i + 1)

            survivors = selection(self.population)

            self.repopulate_from_survivors(pop_size, survivors, Px, Pm, selection=selection)
            best_solution = max(self.population)

            if verbose: print(f'best specimen score: {best_solution[0]}', end=', ')
            if return_chart_data: chart_data_best.append(best_solution[0])
            if return_chart_data: chart_data_worst.append(min(self.population)[0])

            if verbose or return_chart_data:
                sum = 0
                for score, node in self.population:
                    sum += score

                average = sum / pop_size
                if verbose: print(f'average score: {average}')
                if return_chart_data: chart_data_avg.append(average)

        return best_solution, (chart_data_gen, chart_data_best, chart_data_avg, chart_data_worst)

    def repopulate_from_survivors(self, pop_size, survivors, Px, Pm, selection):
        if selection == tournament or selection == roulette:
            self.population.clear()
            for i in range(0, len(survivors), 2):
                if random() <= Px:
                    child_1, child_2 = self.order_1_crossover(survivors[i][1], survivors[i + 1][1])
                    if random() <= Pm: child_1 = self.swap_mutation(child_1)
                    if random() <= Pm: child_2 = self.swap_mutation(child_2)
                    self.population.append(self.assign_score_to_specimen(child_1))
                    self.population.append(self.assign_score_to_specimen(child_2))
                else:
                    self.population.append(survivors[i])
                    self.population.append(survivors[i + 1])
            # while len(self.population) < pop_size:
            #     self.population.append(self.generate_specimen_with_score())
        elif selection == ranking:
            self.population.clear()
            for survivor in survivors:
                self.population.append(survivor)

            for i in range(4):
                for i in range(0, len(survivors), 2):
                    if random() <= Px:
                        child_1, child_2 = self.order_1_crossover(survivors[i][1], survivors[i + 1][1])
                        if random() <= Pm: child_1 = self.swap_mutation(child_1)
                        if random() <= Pm: child_2 = self.swap_mutation(child_2)
                        self.population.append(self.assign_score_to_specimen(child_1))
                        self.population.append(self.assign_score_to_specimen(child_2))

            while len(self.population) < pop_size:
                self.population.append(self.generate_specimen_with_score())
