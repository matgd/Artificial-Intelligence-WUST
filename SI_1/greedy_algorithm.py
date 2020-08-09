def highest_value_strategy(location_items):
    return max(location_items)


def ligthest_weight_strategy(location_items):
    return min(location_items, key=lambda x: x.weight)


def max_profit_weight_ratio(location_items):
    return max(location_items, key=lambda x: x.profit / x.weight)


def execute(specimen, genetic_algorithm, strategy=highest_value_strategy):
    """
    g(y)
    Execute greedy algorithm for specimen containing road.
    :param specimen: list of Nodes: Specimen
    :param genetic_algorithm: Genetic Algorithm of TTP
    :param strategy: function: Function processing list of Items and returning one Item
    :return: dict: Dictionary containing pairs (Node: Item)
    """
    knapsack_free_space = genetic_algorithm.knapsack_free_space

    items_to_take = {}
    for node in specimen:
        if node.index in genetic_algorithm.items.keys():
            candidate_item = strategy(genetic_algorithm.items[node.index])
        else:
            continue

        if knapsack_free_space - candidate_item.weight > 0:
            knapsack_free_space -= candidate_item.weight
            items_to_take[node.index] = candidate_item
        else:
            break

    return items_to_take
