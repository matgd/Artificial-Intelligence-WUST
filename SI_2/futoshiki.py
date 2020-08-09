from random import shuffle

from futoshiki_field import FutoshikiField
from html_generator import futoshiki_to_html

# DEFAULT_FILE = '/home/mateusz/PWr/SI/SI_2/test_data/futoshiki_4_0.txt'
DEFAULT_FILE = '/home/mateusz/PWr/SI/SI_2/research_data/futoshiki_4_0.txt'


class Futoshiki:
    def __init__(self, data_path=DEFAULT_FILE):
        self.N, self.board, self.lt_relations = self.__loader(data_path)
        self.assign_constraints()
        self.steps = 0

        self.filled_cells = 0
        for row in self.board:
            for cell in row:
                if cell.value != 0:
                    self.filled_cells += 1

    def __loader(self, data_path):
        N = []  # list because functions need to operate on references
        board = []
        lt_relations = []

        def process_size(line):
            N.append(int(line))

        def process_board_section(line):
            board.append([FutoshikiField(int(val)) for val in line.strip().split(';')])

        def process_relations_section(line):
            lesser_field, greater_field = line.strip().split(';')
            lt_relations.append((lesser_field, greater_field))

        process_function = process_size

        with open(data_path) as file:
            for line in file:
                if line.startswith('START'):
                    process_function = process_board_section
                    continue
                elif line.startswith('REL'):
                    process_function = process_relations_section
                    continue
                else:
                    process_function(line)

        return N[0], board, lt_relations

    def assign_constraints(self):
        letters_to_rows = {'ABCDEFGHI'[i]: i + 1 for i in range(9)}

        for rel in self.lt_relations:
            first_row_index, first_col_index = int(letters_to_rows[rel[0][0]]) - 1, int(rel[0][1]) - 1
            second_row_index, second_col_index = int(letters_to_rows[rel[1][0]]) - 1, int(rel[1][1]) - 1

            first_cell = self.board[first_row_index][first_col_index]
            second_cell = self.board[second_row_index][second_col_index]

            if first_row_index > second_row_index:
                first_cell.bottom_constraint = ('LT', second_cell)
                second_cell.top_constraint = ('GT', first_cell)
            elif first_row_index < second_row_index:
                first_cell.top_constraint = ('LT', second_cell)
                second_cell.bottom_constraint = ('GT', first_cell)

            if first_col_index > second_col_index:
                first_cell.left_constraint = ('LT', second_cell)
                second_cell.right_constraint = ('GT', first_cell)
            elif first_col_index < second_col_index:
                first_cell.right_constraint = ('LT', second_cell)
                second_cell.left_constraint = ('GT', first_cell)

    def assign_domain_to_cell(self, row, column):
        cell_domain = {i + 1 for i in range(self.N)}
        chosen_cell = self.board[row][column]

        if chosen_cell.value != 0:
            return None

        # check column
        for c_row in range(self.N):
            value_in_cell = self.board[c_row][column].value
            if value_in_cell in cell_domain: cell_domain.remove(value_in_cell)

        # check row
        for r_column in range(self.N):
            value_in_cell = self.board[row][r_column].value
            if value_in_cell in cell_domain: cell_domain.remove(value_in_cell)

        if chosen_cell.has_constraints():
            constraint_cells = []
            if chosen_cell.top_constraint:
                # top_cell = self.board[row + 1][column]
                constraint_cells.append(chosen_cell.top_constraint)

            if chosen_cell.bottom_constraint:
                # bottom_cell = self.board[row - 1][column]
                constraint_cells.append(chosen_cell.bottom_constraint)

            if chosen_cell.left_constraint:
                # left_cell = self.board[row][column - 1]
                constraint_cells.append(chosen_cell.left_constraint)

            if chosen_cell.right_constraint:
                # right_cell = self.board[row][column + 1]
                constraint_cells.append(chosen_cell.right_constraint)

            for constraint_type, cell in constraint_cells:
                if cell.value != 0:
                    if constraint_type == 'LT':
                        cell_domain = cell_domain.difference({val for val in range(cell.value, self.N + 1)})
                    else:
                        cell_domain = cell_domain.difference({val for val in range(1, cell.value + 1)})

                if constraint_type == 'LT':
                    cell_domain -= {self.N}  # remove max
                else:
                    cell_domain -= {1}  # remove min

        return cell_domain

    def fill_known_fields(self):
        """ Fill fields where the size of domain is equal to 1 """
        for row in range(self.N):
            for column in range(self.N):
                current_cell = self.board[row][column]
                domain = self.assign_domain_to_cell(row, column)
                if domain is not None and len(domain) == 1:
                    current_cell.value = domain.pop()
                    self.filled_cells += 1

    def assign_value_to_cell(self, cell: FutoshikiField, value):
        cell.value = value
        # cell.domain = None
        self.filled_cells += 1

    def solve_what_is_known(self):
        last_iteration_filled = -1
        while last_iteration_filled != self.filled_cells:
            last_iteration_filled = self.filled_cells
            self.fill_known_fields()

    def board_is_filled(self):
        return self.filled_cells == self.N ** 2

    def board_valid_sumcheck(self):
        desired_sum = sum([i + 1 for i in range(self.N)])
        desired_sum *= self.N
        board_sum = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                board_sum += self.board[j][i].value
        return desired_sum == board_sum

    def board_is_valid(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                cell = self.board[row][column]
                if cell.value == 0 and self.assign_domain_to_cell(row, column) == set():
                    return False

        return True

    def solve_with_backtracking(self):
        if self.board_is_filled():
            return True

        start_row, start_col = self.__get_starting_point()
        start_cell = self.board[start_row][start_col]

        values_to_check = self.__get_starting_values(start_row, start_col)

        for start_value in values_to_check:
            self.steps += 1
            self.assign_value_to_cell(start_cell, start_value)

            if self.solve_with_backtracking():
                return True

            self.clear_cell(start_cell)

        return False

    def solve_with_look_forward(self):
        if self.board_is_filled():
            return True

        if not self.board_is_valid():
            return False

        start_row, start_col = self.__get_starting_point()
        start_cell = self.board[start_row][start_col]

        values_to_check = self.__get_starting_values(start_row, start_col)

        for start_value in values_to_check:
            self.steps += 1
            self.assign_value_to_cell(start_cell, start_value)

            if self.solve_with_look_forward():
                return True

            self.clear_cell(start_cell)

        return False

    def clear_cell(self, cell):
        cell.value = 0
        self.filled_cells -= 1

    def __get_starting_point(self, method: str = 'first'):
        """
        Choose starting point for backtracking.
        :param method:
            'most_constraints': the one with most constraints, then smallest domain
            'smallest_domain': the one with smallest domain, then most constraints
            'domain1': prioritize cells with len(domain) == 1, else 'most_constraints'
        :return: starting coordinates tuple, eg. (0, 0)
        """
        cell_row, cell_col = -1, -1
        constraint_count = -1
        domain_length = self.N + 1

        if method == 'most_constraints':
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    current_cell = self.board[row][column]
                    if current_cell.has_constraints() and self.assign_domain_to_cell(row, column) is not None:
                        curr_constraints = 4 - [current_cell.top_constraint,
                                                current_cell.bottom_constraint,
                                                current_cell.left_constraint,
                                                current_cell.right_constraint].count(None)
                        if curr_constraints > constraint_count:
                            cell_row, cell_col = row, column
                            constraint_count = curr_constraints
                            domain_length = len(self.assign_domain_to_cell(cell_row, cell_col))

                        elif curr_constraints == constraint_count:
                            curr_domain_length = len(self.assign_domain_to_cell(cell_row, cell_col))
                            if curr_domain_length < domain_length:
                                cell_row, cell_col = row, column
                                domain_length = curr_domain_length

            if cell_row == -1:
                # find any available without constraints
                for row in range(len(self.board)):
                    for column in range(len(self.board[row])):
                        if self.board[row][column].value == 0:
                            return row, column

        elif method == 'smallest_domain':
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    cell_domain = self.assign_domain_to_cell(row, column)
                    if cell_domain is not None and len(cell_domain) < domain_length:
                        if len(cell_domain) == 1:
                            return row, column
                        cell_row, cell_col = row, column
                        domain_length = len(cell_domain)

            if cell_row == -1:
                # find any available without constraints
                for row in range(len(self.board)):
                    for column in range(len(self.board[row])):
                        if self.board[row][column].value == 0:
                            return row, column

        elif method == 'domain1':
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    current_cell = self.board[row][column]
                    cell_domain = self.assign_domain_to_cell(row, column)
                    if cell_domain is not None:
                        if len(cell_domain) == 1:
                            return row, column
                        elif current_cell.has_constraints():
                            curr_constraints = 4 - [current_cell.top_constraint,
                                                    current_cell.bottom_constraint,
                                                    current_cell.left_constraint,
                                                    current_cell.right_constraint].count(None)

                            if curr_constraints > constraint_count:
                                cell_row, cell_col = row, column
                                constraint_count = curr_constraints
                                domain_length = len(self.assign_domain_to_cell(cell_row, cell_col))

                            elif curr_constraints == constraint_count:
                                curr_domain_length = len(self.assign_domain_to_cell(cell_row, cell_col))
                                if curr_domain_length < domain_length:
                                    cell_row, cell_col = row, column
                                    domain_length = curr_domain_length

            if cell_row == -1:
                # find any available without constraints
                for row in range(len(self.board)):
                    for column in range(len(self.board[row])):
                        if self.board[row][column].value == 0:
                            return row, column

        elif method == 'first':
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    if self.board[row][column].value == 0:
                        return row, column

        else:
            raise Exception(f'Method {method} is not supported!')

        return cell_row, cell_col

    def __get_starting_values(self, row, column, method: str = 'ascending'):
        """
        Choose from which value to start first from field.
        :param cell: cell to choose value for
        :param method:
            'least_constraining': the one constraining the least, eg. when it has
                                  bigger than other then choose max from domain
        :return: value to assign
        """
        cell_domain = self.assign_domain_to_cell(row, column)
        current_cell = self.board[row][column]

        if method == 'least_constraining':
            def constraint_score(cell: FutoshikiField):
                domain_size_sum = 0

                if cell.top_constraint:
                    constraint_domain = self.assign_domain_to_cell(row + 1, column)
                    if constraint_domain != set() and constraint_domain != None:
                        domain_size_sum += len(constraint_domain)
                    if constraint_domain == set():
                        return None

                if cell.bottom_constraint:
                    constraint_domain = self.assign_domain_to_cell(row - 1, column)
                    if constraint_domain != set() and constraint_domain != None:
                        domain_size_sum += len(constraint_domain)
                    if constraint_domain == set():
                        return None

                if cell.left_constraint:
                    constraint_domain = self.assign_domain_to_cell(row, column - 1)
                    if constraint_domain != set() and constraint_domain != None:
                        domain_size_sum += len(constraint_domain)
                    if constraint_domain == set():
                        return None

                if cell.right_constraint:
                    constraint_domain = self.assign_domain_to_cell(row, column + 1)
                    if constraint_domain != set() and constraint_domain != None:
                        domain_size_sum += len(constraint_domain)
                    if constraint_domain == set():
                        return None

                return domain_size_sum

            value_domain_count = {}
            for candidate_value in cell_domain:
                current_cell = self.board[row][column]
                self.assign_value_to_cell(current_cell, candidate_value)
                c_score = constraint_score(current_cell)
                if c_score is None:
                    self.clear_cell(current_cell)
                    continue
                value_domain_count[candidate_value] = c_score
                self.clear_cell(current_cell)

            return [k for _, k in sorted([(v, k) for k, v in value_domain_count.items()], reverse=True)]

        elif method == 'ascending':
            return sorted(list(cell_domain))

        elif method == 'least_constraining_row_col':
            def constraint_score(cell: FutoshikiField):
                domain_size_sum = 0

                for x in range(self.N):
                    constraint_domain = self.assign_domain_to_cell(x, column)
                    if constraint_domain != set() and constraint_domain != None:
                        domain_size_sum += len(constraint_domain)
                    if constraint_domain == set():
                        return None

                    constraint_domain = self.assign_domain_to_cell(row, x)
                    if constraint_domain != set() and constraint_domain != None:
                        domain_size_sum += len(constraint_domain)
                    if constraint_domain == set():
                        return None

                return domain_size_sum

            value_domain_count = {}
            for candidate_value in cell_domain:
                current_cell = self.board[row][column]
                self.assign_value_to_cell(current_cell, candidate_value)
                c_score = constraint_score(current_cell)
                if c_score is None:
                    self.clear_cell(current_cell)
                    continue
                value_domain_count[candidate_value] = c_score
                self.clear_cell(current_cell)

            return [k for _, k in sorted([(v, k) for k, v in value_domain_count.items()], reverse=True)]
        elif method == 'least_constraining_old':
            if current_cell.has_constraints():
                constraint_types = []
                if current_cell.top_constraint: constraint_types.append(current_cell.top_constraint[0])
                if current_cell.bottom_constraint: constraint_types.append(current_cell.bottom_constraint[0])
                if current_cell.left_constraint: constraint_types.append(current_cell.left_constraint[0])
                if current_cell.right_constraint: constraint_types.append(current_cell.right_constraint[0])

                if constraint_types.count('LT') > constraint_types.count('GT'):
                    return sorted(list(cell_domain))
                elif constraint_types.count('LT') < constraint_types.count('GT'):
                    return sorted(list(cell_domain), reverse=True)
                else:
                    list_domain = sorted(list(cell_domain))
                    return list_domain

            return list(cell_domain)

        elif method == 'random':
            list_domain = list(cell_domain)
            shuffle(list_domain)
            return list_domain

        raise Exception('Invalid method!')

    def save_to_html(self, filename='../futoshiki.html'):
        futoshiki_to_html(self.board, filename)
