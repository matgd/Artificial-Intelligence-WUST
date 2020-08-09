from random import randint, choices, shuffle


def ranking(population, number_of_winners=20):
    """
    Ranking - take 'number_of_winners' best specimens.
    :param number_of_winners: Surviving specimens
    :param population: Population, list of tuples -> score, specimen
    :return: Winners
    """
    survivors = sorted(population, reverse=True)[:number_of_winners]
    shuffle(survivors)
    return survivors


def tournament(population, Tour=5):
    """
    Tournament - take 'Tour' random specimens, the best one surivives, repeat till filling population
    :param population: Population, list of tuples -> score, specimen
    :param Tour: Tournament size
    :return: Winners
    """
    survivors = []
    for i in range(len(population)):
        random_indexes = []
        while len(random_indexes) < Tour:
            chosen_number = randint(0, len(population) - 1)
            # if chosen_number not in random_indexes: random_indexes.append(chosen_number)
            random_indexes.append(chosen_number)
        tournament_group = [population[index] for index in random_indexes]
        survivors.append(max(tournament_group))

    return survivors


def roulette(population):
    survivors = []
    min_score_offset = min(population)[0]
    max_score = max(population)[0]
    if min_score_offset > 0:
        min_score_offset = 0
    if max_score == min_score_offset:
        min_score_offset = 1
    population_score_sum = sum([score - min_score_offset for score, specimen in population])
    if population_score_sum == 0:
        population_score_sum = 1
    roulette_odds = [(score - min_score_offset) / population_score_sum for score, specimen in population]
    for i in range(len(population)):
        survivors.append(choices(population, roulette_odds)[0])

    return survivors
