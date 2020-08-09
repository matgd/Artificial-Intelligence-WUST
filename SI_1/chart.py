from matplotlib import pyplot as plt

def draw_chart(x_axis_tuple, y_axis_tuple_list, title):
    """
    Draw chart.
    :param x_axis_tuple: eg. [1, 2, 3], 'First 3 letters'
    :param y_axis_tuple_list: eg.
        [([1, 2, 3, 4], '4 letters', 'blue'), ([6, 2, 6, 2], 'Another 4 letters', 'red')]
    :return:
    """
    plt.title(title)
    plt.xlabel('Generation')
    plt.ylabel('Score')

    for y_axis, label, color in y_axis_tuple_list:
        if color:
            plt.plot(x_axis_tuple[0], y_axis, label=label, color=color)
        else:
            plt.plot(x_axis_tuple[0], y_axis, label=label)
        plt.legend()

    plt.show()
