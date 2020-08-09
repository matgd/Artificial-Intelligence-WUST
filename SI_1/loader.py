from node import Node
from item import Item

DATA_PATH = 'student/trivial_1.ttp'

metadata = {}  # CEIL_2D, int zaokrąglany do liczby całkowitej
nodes = {}
items = {}


def __process_metadata(line):
    attribute, value = line.split(':')
    metadata[attribute] = value.strip()


def __process_node_cord_section(line):
    line = line.strip()
    index, x, y = line.split('\t')

    nodes[int(index)] = Node(int(index), float(x), float(y))


def __process_items_section(line):
    index, profit, weight, assigned_node_number = line.split('\t')
    int_assigned_node_number = int(assigned_node_number.strip())
    read_item = Item(int(index), int(profit), int(weight), int_assigned_node_number)

    if int_assigned_node_number in items:
        items[int_assigned_node_number].append(read_item)
    else:
        items[int_assigned_node_number] = [read_item]


def load_data(data_path):
    process_function = __process_metadata

    with open(data_path) as file:
        for line in file:
            if line.startswith('NODE_COORD_SECTION'):
                process_function = __process_node_cord_section
                continue
            elif line.startswith('ITEMS SECTION'):
                process_function = __process_items_section
                continue
            else:
                process_function(line)

    return metadata, nodes, items


def flush_loader():
    metadata.clear()
    nodes.clear()
    items.clear()
