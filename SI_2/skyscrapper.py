from random import shuffle

from html_generator import skyscrapper_to_html

DEFAULT_FILE = '/home/mateusz/PWr/SI/SI_2/test_data/skyscrapper_4_0.txt'


class Skyscrapper:
    def __init__(self, data_path=DEFAULT_FILE):
        self.N, self.constraints = self.__loader(data_path)
        self.board = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.filled_cells = 0
        self.steps = 0
        for row in self.board:
            for cell in row:
                if cell != 0:
                    self.filled_cells += 1

    def __loader(self, data_path):
        N = []  # list because functions need to operate on references
        constraints = {}

        def process_size(line):
            N.append(int(line))

        def process_constraints_section(line):
            val_list = line.strip().split(';')
            constraints[val_list[0]] = [int(val) for val in val_list[1:]]

        process_function = process_size

        with open(data_path) as file:
            for line in file:
                if line.startswith('G'):
                    process_function = process_constraints_section
                    process_function(line)
                else:
                    process_function(line)

        return N[0], constraints

    def __cell_is_on_border(self, row, column):
        return row == 0 or row == self.N - 1 or column == 0 or column == self.N - 1

    def assign_domain_to_cell(self, row, column, if_filled_none=True):
        cell_domain = {i + 1 for i in range(self.N)}
        chosen_cell_value = self.board[row][column]

        if if_filled_none:
            if chosen_cell_value != 0:
                return None

        # check border
        if self.__cell_is_on_border(row, column):
            if row == 0:  # TOP
                if self.constraints['G'][column] == self.N:
                    return {1}
                elif self.constraints['G'][column] == 1:
                    return {self.N}
                else:
                    constraint = self.constraints['G'][column]
                    cell_domain = cell_domain.difference({i for i in range(self.N, self.N - constraint + 1, -1)})

            if row == self.N - 1:  # BOTTOM
                if self.constraints['D'][column] == self.N:
                    cell_domain -= {i for i in range(2, self.N + 1)}
                elif self.constraints['D'][column] == 1:
                    cell_domain -= {i for i in range(1, self.N)}
                else:
                    constraint = self.constraints['D'][column]
                    cell_domain = cell_domain.difference({i for i in range(self.N, self.N - constraint + 1, -1)})

            if column == 0:  # LEFT
                if self.constraints['L'][row] == self.N:
                    cell_domain -= {i for i in range(2, self.N + 1)}
                elif self.constraints['L'][row] == 1:
                    cell_domain -= {i for i in range(1, self.N)}
                else:
                    constraint = self.constraints['L'][row]
                    cell_domain = cell_domain.difference({i for i in range(self.N, self.N - constraint + 1, -1)})

            if column == self.N - 1:  # RIGHT
                if self.constraints['P'][row] == self.N:
                    cell_domain -= {i for i in range(2, self.N + 1)}
                elif self.constraints['P'][row] == 1:
                    cell_domain -= {i for i in range(1, self.N)}
                else:
                    constraint = self.constraints['P'][row]
                    cell_domain = cell_domain.difference({i for i in range(self.N, self.N - constraint + 1, -1)})

        # check column values
        for c_row in range(self.N):
            value_in_cell = self.board[c_row][column]
            if value_in_cell in cell_domain: cell_domain.remove(value_in_cell)

        # check row values
        for r_column in range(self.N):
            value_in_cell = self.board[row][r_column]
            if value_in_cell in cell_domain: cell_domain.remove(value_in_cell)

        left_constraint = self.constraints['L'][row]
        right_constraint = self.constraints['P'][row]
        top_constraint = self.constraints['G'][column]
        bottom_constraint = self.constraints['D'][column]

        if left_constraint != 0:
            in_sight = 0
            highest_seen = 0
            for left_row_value in self.board[row][:column]:
                if left_row_value > highest_seen:
                    highest_seen = left_row_value
                    in_sight += 1
            if in_sight > left_constraint:
                cell_domain = cell_domain.difference({i for i in range(highest_seen, self.N + 1)})  # cannot be higher
                # if in_sight > left_constraint:
                #     return set()

        if right_constraint != 0:
            in_sight = 0
            highest_seen = 0
            for right_row_value in self.board[row][-1:column:-1]:
                if right_row_value > highest_seen:
                    highest_seen = right_row_value
                    in_sight += 1
            if in_sight > right_constraint:
                cell_domain = cell_domain.difference({i for i in range(highest_seen, self.N + 1)})
                # if in_sight > right_constraint:
                #     return set()

        if top_constraint != 0:
            in_sight = 0
            highest_seen = 0
            for i in range(row):
                top_column_value = self.board[i][column]
                if top_column_value > highest_seen:
                    highest_seen = top_column_value
                    in_sight += 1
            if in_sight > top_constraint:
                cell_domain = cell_domain.difference({i for i in range(highest_seen, self.N + 1)})
                # if in_sight > top_constraint:
                #     return set()

        if bottom_constraint != 0:
            in_sight = 0
            highest_seen = 0
            for i in range(self.N - 1, row, -1):
                bottom_column_value = self.board[i][column]
                if bottom_column_value > highest_seen:
                    highest_seen = bottom_column_value
                    in_sight += 1
            if in_sight > bottom_constraint:
                cell_domain = cell_domain.difference({i for i in range(highest_seen, self.N + 1)})
                # if in_sight > bottom_constraint:
                #     return set()

        return cell_domain

    def fill_known_fields(self):
        """ Fill fields where the size of domain is equal to 1 """
        for row in range(self.N):
            for column in range(self.N):
                domain = self.assign_domain_to_cell(row, column)
                if domain is not None and len(domain) == 1:
                    self.board[row][column] = domain.pop()
                    self.filled_cells += 1

    def solve_what_is_known(self):
        last_iteration_filled = -1
        while last_iteration_filled != self.filled_cells:
            last_iteration_filled = self.filled_cells
            self.fill_known_fields()

    def board_is_filled(self):
        return self.filled_cells == self.N ** 2

    def assign_value_to_cell(self, row, col, value):
        self.board[row][col] = value
        self.filled_cells += 1

    def validate_after_assign(self, row, column):
        left_constraint = self.constraints['L'][row]
        right_constraint = self.constraints['P'][row]
        top_constraint = self.constraints['G'][column]
        bottom_constraint = self.constraints['D'][column]

        filled_row = 0
        filled_col = 0
        for left_row_value in self.board[row]:
            if left_row_value != 0:
                filled_row += 1

        for i in range(self.N):
            column_value = self.board[i][column]
            if column_value != 0:
                filled_col += 1

        if filled_row == self.N:
            if left_constraint != 0:
                in_sight = 0
                highest_seen = 0
                for left_row_value in self.board[row]:
                    if left_row_value > highest_seen:
                        highest_seen = left_row_value
                        in_sight += 1
                if in_sight != left_constraint:
                    return False

            if right_constraint != 0:
                in_sight = 0
                highest_seen = 0
                for right_row_value in self.board[row][::-1]:
                    if right_row_value > highest_seen:
                        highest_seen = right_row_value
                        in_sight += 1
                if in_sight != right_constraint:
                    return False

        if filled_col == self.N:
            if top_constraint != 0:
                in_sight = 0
                highest_seen = 0
                for i in range(self.N):
                    top_column_value = self.board[i][column]
                    if top_column_value > highest_seen:
                        highest_seen = top_column_value
                        in_sight += 1
                if in_sight != top_constraint:
                    return False

            if bottom_constraint != 0:
                in_sight = 0
                highest_seen = 0
                for i in range(self.N - 1, -1, -1):
                    bottom_column_value = self.board[i][column]
                    if bottom_column_value > highest_seen:
                        highest_seen = bottom_column_value
                        in_sight += 1
                if in_sight != bottom_constraint:
                    return False

        return True

    def board_is_valid(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == 0 and self.assign_domain_to_cell(row, column) == set():
                    return False

        return True

    def solve_with_backtracking(self):
        if self.board_is_filled():
            return True

        start_row, start_col = self.__get_starting_point()

        values_to_check = self.__get_starting_values(start_row, start_col)

        for start_value in values_to_check:
            self.steps += 1
            self.assign_value_to_cell(start_row, start_col, start_value)

            if self.validate_after_assign(start_row, start_col) and self.solve_with_backtracking():
                return True

            self.clear_cell(start_row, start_col)

        return False

    def solve_with_look_forward(self):
        if self.board_is_filled():
            return True

        if not self.board_is_valid():
            return False

        start_row, start_col = self.__get_starting_point()

        values_to_check = self.__get_starting_values(start_row, start_col)

        for start_value in values_to_check:
            self.steps += 1
            self.assign_value_to_cell(start_row, start_col, start_value)

            if self.validate_after_assign(start_row, start_col) and self.solve_with_look_forward():
                return True

            self.clear_cell(start_row, start_col)

        return False

    def clear_cell(self, row, col):
        self.board[row][col] = 0
        self.filled_cells -= 1

    def __get_starting_point(self, method: str = 'domain1'):
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
            def buildings_on_the_way(cell_row, cell_column):
                buildings = 0

                for i in range(len(self.board)):
                    if self.board[cell_row][i] != 0:
                        buildings += 1
                    if self.board[i][cell_column] != 0:
                        buildings += 1

                return buildings

            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    if self.board[row][column] == 0:
                        current_constraint = buildings_on_the_way(row, column)
                        if current_constraint > constraint_count:
                            cell_row = row
                            cell_col = column

        elif method == 'smallest_domain':
            for row in range(self.N):
                for column in range(self.N):
                    cell_domain = self.assign_domain_to_cell(row, column)
                    if cell_domain is not None and len(cell_domain) < domain_length:
                        cell_row, cell_col = row, column
                        domain_length = len(cell_domain)

            if cell_row == -1:
                # find any available without constraints
                for row in range(len(self.board)):
                    for column in range(len(self.board[row])):
                        if self.board[row][column] == 0:
                            return row, column

        elif method == 'domain1':
            for row in range(self.N):
                for column in range(self.N):
                    cell_domain = self.assign_domain_to_cell(row, column)
                    if cell_domain is not None and len(cell_domain) == 1:
                        return row, column

            return self.__get_starting_point('most_constraints')

        elif method == 'first':
            for row in range(len(self.board)):
                for column in range(len(self.board[row])):
                    if self.board[row][column] == 0:
                        return row, column

        else:
            raise Exception(f'Method {method} is not supported!')

        return cell_row, cell_col

    def __get_starting_values(self, row, column, method: str = 'least_constraining'):
        """
        Choose from which value to start first from field.
        :param cell: cell to choose value for
        :param method:
            'least_constraining': the one constraining the least, eg. when it has
                                  bigger than other then choose max from domain
        :return: value to assign
        """
        cell_domain = self.assign_domain_to_cell(row, column)

        if method == 'least_constraining':
            def constraint_score(cell_row, cell_column):
                domain_score = 0

                for i in range(self.N):
                    iter_domain = self.assign_domain_to_cell(cell_row, i)
                    if iter_domain != set() and iter_domain != None:
                        domain_score += len(iter_domain)
                    if iter_domain == set():
                        return None

                for i in range(self.N):
                    iter_domain = self.assign_domain_to_cell(i, cell_column)
                    if iter_domain != set() and iter_domain != None:
                        domain_score += len(iter_domain)
                    if iter_domain == set():
                        return None

                return domain_score

            value_domain_count = {}
            for candidate_value in cell_domain:
                self.assign_value_to_cell(row, column, candidate_value)
                c_score = constraint_score(row, column)
                if c_score is None:
                    self.clear_cell(row, column)
                    continue
                value_domain_count[candidate_value] = c_score
                self.clear_cell(row, column)

            return [k for _, k in sorted([(v, k) for k, v in value_domain_count.items()], reverse=True)]

        elif method == 'random':
            list_domain = list(cell_domain)
            shuffle(list_domain)
            return list_domain

        elif method == 'ascending':
            return sorted(list(cell_domain))

        raise Exception('Invalid method!')

    def board_valid_sumcheck(self):
        desired_sum = sum([i + 1 for i in range(self.N)])
        desired_sum *= self.N
        board_sum = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                board_sum += self.board[j][i]
        return desired_sum == board_sum

    def save_to_html(self):
        skyscrapper_to_html(self.board, self.constraints)
