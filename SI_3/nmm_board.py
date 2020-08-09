import logging

from nmm_field import NMM_Field
from nmm_pawn_types import NMM_Pawn


class NMM_Board:
    def __init__(self):
        self.board = self.__create_board()
        self.__assign_fields_neighbourhood()
        self.lines = self.__create_lines()
        self.move_history = []
        self.last_filled_field_coordinates = None

    def __create_board(self):
        fields_coordinates = [
            'A1',             'A4',             'A7',

                  'B2',       'B4',       'B6',

                        'C3', 'C4', 'C5',

            'D1', 'D2', 'D3',       'D5', 'D6', 'D7',

                        'E3', 'E4', 'E5',

                  'F2',       'F4',       'F6',

            'G1',             'G4',             'G7'
        ]

        return {crds: NMM_Field(crds) for crds in fields_coordinates}

    def __assign_fields_neighbourhood(self):
        self.board['A1'].add_adjacent_fields(self.board['A4'], self.board['D1'])
        self.board['A4'].add_adjacent_fields(self.board['A1'], self.board['A7'], self.board['B4'])
        self.board['A7'].add_adjacent_fields(self.board['A4'], self.board['D7'])
        self.board['B2'].add_adjacent_fields(self.board['B4'], self.board['D2'])
        self.board['B4'].add_adjacent_fields(self.board['A4'], self.board['B2'], self.board['B6'], self.board['C4'])
        self.board['B6'].add_adjacent_fields(self.board['B4'], self.board['D6'])
        self.board['C3'].add_adjacent_fields(self.board['C4'], self.board['D3'])
        self.board['C4'].add_adjacent_fields(self.board['C3'], self.board['B4'], self.board['C5'])
        self.board['C5'].add_adjacent_fields(self.board['C4'], self.board['D5'])
        self.board['D1'].add_adjacent_fields(self.board['A1'], self.board['D2'], self.board['G1'])
        self.board['D2'].add_adjacent_fields(self.board['D1'], self.board['B2'], self.board['F2'], self.board['D3'])
        self.board['D3'].add_adjacent_fields(self.board['D2'], self.board['C3'], self.board['E3'])
        self.board['D5'].add_adjacent_fields(self.board['C5'], self.board['D6'], self.board['E5'])
        self.board['D6'].add_adjacent_fields(self.board['D5'], self.board['B6'], self.board['F6'], self.board['D7'])
        self.board['D7'].add_adjacent_fields(self.board['A7'], self.board['D6'], self.board['G7'])
        self.board['E3'].add_adjacent_fields(self.board['D3'], self.board['E4'])
        self.board['E4'].add_adjacent_fields(self.board['E3'], self.board['F4'], self.board['E5'])
        self.board['E5'].add_adjacent_fields(self.board['E4'], self.board['D5'])
        self.board['F2'].add_adjacent_fields(self.board['D2'], self.board['F4'])
        self.board['F4'].add_adjacent_fields(self.board['F2'], self.board['E4'], self.board['G4'], self.board['F6'])
        self.board['F6'].add_adjacent_fields(self.board['F4'], self.board['D6'])
        self.board['G1'].add_adjacent_fields(self.board['D1'], self.board['G4'])
        self.board['G4'].add_adjacent_fields(self.board['G1'], self.board['F4'], self.board['G7'])
        self.board['G7'].add_adjacent_fields(self.board['G4'], self.board['D7'])

    def __create_lines(self):
        lines = {
            coordinates: [
                [crds for crds in self.board.keys() if crds.startswith(coordinates[0])],
                [crds for crds in self.board.keys() if crds.endswith(coordinates[1])]
            ] for coordinates in self.board.keys()
        }

        # Fixes for 'D' row and '4' column
        for i in range(1, 4):
            lines[f'D{i}'][0] = lines[f'D{i}'][0][:3]

        for i in range(5, 8):
            lines[f'D{i}'][0] = lines[f'D{i}'][0][3:]

        for c in 'ABC':
            lines[f'{c}4'][1] = lines[f'{c}4'][1][:3]

        for c in 'EFG':
            lines[f'{c}4'][1] = lines[f'{c}4'][1][3:]

        return lines

    def place_pawn(self, coordinates: str, pawn_type: NMM_Pawn):
        if self.board[coordinates].value is not None:
            logging.error('Placing pawn on occupied place.')

        self.board[coordinates].value = pawn_type
        self.last_filled_field_coordinates = coordinates
        self.move_history.append((coordinates,))

    def move_pawn(self, start_coordinates: str, destination_coordinates: str):
        if self.board[start_coordinates].value is None:
            logging.error('Trying to move non-existing pawn.')

        if self.board[destination_coordinates].value is not None:
            logging.error('Moving the pawn on already occupied place.')

        self.board[destination_coordinates].value = self.board[start_coordinates].value
        self.board[start_coordinates].value = None
        self.last_filled_field_coordinates = destination_coordinates
        self.move_history.append((start_coordinates, destination_coordinates,))

    def remove_pawn(self, coordinates):
        if self.board[coordinates].value is None:
            logging.error('Place is not occupied.')

        self.board[coordinates].value = None
        self.move_history.append(('REMOVED', coordinates,))

    def check_for_mill(self):
        if self.last_filled_field_coordinates is None:
            return 0

        last_placed_pawn_color = self.board[self.last_filled_field_coordinates].value
        mills = 0
        for line in self.lines[self.last_filled_field_coordinates]:
            if all([self.board[crds].value is last_placed_pawn_color for crds in line]):
                mills += 1

        return mills

    def free_fields_coordinates(self):
        return [crds for crds, field in self.board.items() if field.value is None]

    def color_fields_coordinates(self, color: NMM_Pawn):
        return [crds for crds, field in self.board.items() if field.value is color]
