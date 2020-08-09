from math import sqrt, ceil

from node import Node


def func_d(x1: Node, x2: Node) -> float:
    """
    Distance between two nodes.
    :param x1: First node
    :param x2: Second node
    :return: Distance
    """
    return ceil(sqrt((x1.x - x2.x) ** 2 + (x1.y - x2.y) ** 2))


def func_t(d: float, v: float) -> float:
    """
    Time between visiting two nodes.
    :param d: Distance between nodes
    :param v: Velocity
    :return: Time
    """
    return d / v


def func_f(x: list) -> float:
    """
    Total road time.
    :param x: Road, list of nodes' indexes
    :return: Time
    """
    velocity = 1  # TODO: Get rid off magic number
    total_time = 0

    for i in range(len(x) - 1):
        total_time += func_t(func_d(x[i], x[i + 1]), velocity)

    total_time += func_t(func_d(x[0], x[-1]), velocity)  # Return time

    return total_time


def func_v(v_max: float, v_min: float, w_c: int, w: int):
    """
    Velocity function.
    :param v_max: Max speed
    :param v_min: Min speed
    :param w_c: Knapsack weight occupied
    :param w: Knapsack capacity
    :return: Velocity
    """
    return v_max - w_c * ((v_max - v_min) / w)


def genetic_func_f(x: list, genetetic_algorithm):
    """ f(x,y) """
    max_speed = genetetic_algorithm.MAX_SPEED
    min_speed = genetetic_algorithm.MIN_SPEED
    knapsack_free_space = genetetic_algorithm.knapsack_free_space
    items_to_take = genetetic_algorithm.assign_items_to_specimen(x)

    velocity = max_speed
    total_time = 0

    for i in range(len(x) - 1):
        if x[i].index in items_to_take.keys():
            knapsack_free_space -= items_to_take[x[i].index].weight
        velocity = func_v(max_speed,
                          min_speed,
                          genetetic_algorithm.KNAPSACK_CAPACITY - knapsack_free_space,
                          genetetic_algorithm.KNAPSACK_CAPACITY)
        total_time += func_t(func_d(x[i], x[i + 1]), velocity)

    if x[len(x) - 1].index in items_to_take.keys():
        knapsack_free_space -= items_to_take[x[len(x) - 1].index].weight
    velocity = func_v(max_speed,
                      min_speed,
                      genetetic_algorithm.KNAPSACK_CAPACITY - knapsack_free_space,
                      genetetic_algorithm.KNAPSACK_CAPACITY)

    total_time += func_t(func_d(x[-1], x[0]), velocity)  # Return time

    return total_time


def func_g(y):
    """
    Sum of items in knapsack
    :param y: dict: Generated dict of items to take
    :return: int: Knapsack value
    """
    return sum([item.profit for item in y.values()])
