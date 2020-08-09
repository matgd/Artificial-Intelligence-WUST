import loader
from genetic_algorithm import GeneticAlgorithm
import functions
from node import Node
from item import Item
import greedy_algorithm
from selection import *
from chart import draw_chart

if __name__ == '__main__':
    from pprint import pprint

    GA = GeneticAlgorithm(*loader.load_data('student/hard_0.ttp'))
    repetitions = 3

    gen = 100
    Pm = 0.01
    Px = 0.7

    pop_size = 100
    selection = roulette
    # result = GA.execute(gen=100, Pm=0.01, Px=0.7, pop_size=100, selection=tournament, verbose=True, return_chart_data=True)
    result = [
        GA.execute(gen=gen, Pm=Pm, Px=Px, pop_size=pop_size, selection=selection, verbose=True, return_chart_data=True)
        for _ in range(repetitions)
    ]
    #
    result_as = [0 for _ in range(gen)]
    result_bs = [0 for _ in range(gen)]
    result_ws = [0 for _ in range(gen)]
    for i in range(repetitions):
        for j in range(gen):
            result_as[j] += result[i][1][2][j] / repetitions
            result_bs[j] += result[i][1][1][j] / repetitions
            result_ws[j] += result[i][1][3][j] / repetitions

    draw_chart((result[0][1][0], 'Generations'),
               [(result_bs, 'Best score', 'blue'),
                (result_as, 'Average score', 'red'),
                (result_ws, 'Worst score', 'orange')],
               f"Score by generation\nPm={Pm}, Px={Px}, pop_size={pop_size}, selection={selection.__name__}")

    # draw_chart((result[1][0], 'Generations'),
    #            [(result[1][2], 'Average score', 'red'),
    #             (result[1][1], 'Best score', 'blue'),
    #             (result[1][3], 'Worst score', 'orange')])
