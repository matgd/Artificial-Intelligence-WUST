import logging

from nmm_pawn_types import NMM_Pawn
from nmm_board import NMM_Board


class NMM_Player:
    def __init__(self, board: NMM_Board, pawn_color: NMM_Pawn, name):
        self.board = board
        self.pawn_color = pawn_color
        self.name = name
        self.opponent = None
        self.pawns_to_deploy = 9
        self.pawns_owned = 9
        self.pawns_taken = 0
        self.pawns_coordinates = []
        self.move_history = []

    def assign_opponent(self, opponent):
        self.opponent = opponent

    def can_move_pawn_freely(self):
        return self.pawns_owned == 3

    def lose_pawn(self, coordinates):
        self.pawns_owned -= 1
        self.pawns_coordinates.remove(coordinates)
        # if self.pawns_owned == 2:
        #     self.print_game_lost_message()

    def remove_opponents_pawn(self, coordinates):
        self.board.remove_pawn(coordinates)
        self.opponent.lose_pawn(coordinates)
        self.move_history.append(('REMOVED', coordinates,))
        self.pawns_taken += 1

    def print_game_lost_message(self):
        print(f'Player {self.name} has lost the game!')

    def print_game_won_message(self):
        print(f'Player {self.name} has won!')

    def place_pawn(self, coordinates):
        self.board.place_pawn(coordinates, self.pawn_color)
        self.pawns_coordinates.append(coordinates)
        self.pawns_to_deploy -= 1
        self.move_history.append((coordinates,))

    def move_pawn(self, start_coordinates, destination_coordinates):
        self.board.move_pawn(start_coordinates, destination_coordinates)
        self.pawns_coordinates.remove(start_coordinates)
        self.pawns_coordinates.append(destination_coordinates)
        self.move_history.append((start_coordinates, destination_coordinates,))

    def prompt_player_for_move(self):
        command_prompt = f'[{self.name} | on board: {self.pawns_owned - self.pawns_to_deploy}]'

        try:
            if self.pawns_to_deploy > 0:
                free_fields_coordinates = self.board.free_fields_coordinates()

                print(f'[DEPLOY]{command_prompt} Please provide coordinates: ')
                # print(free_fields_coordinates)
                print(f'[DEPLOY]{command_prompt} >>> ', end='')
                coordinates = str(input()).upper()
                self.place_pawn(coordinates)

            elif self.pawns_owned > 3:
                print(f'[ SHIFT]{command_prompt} Select one of the pawns to move: ')
                movable_pawns = [crds for crds in self.pawns_coordinates if
                                 self.board.board[crds].get_empty_adjacent_fields()]
                if not movable_pawns:
                    return False
                print(movable_pawns)
                print(f'[ SHIFT]{command_prompt} >>> ', end='')
                start_crds = str(input()).upper()
                if start_crds not in movable_pawns:
                    raise KeyError
                print(f'[ SHIFT]{command_prompt} Choose destination: ')
                adjacent_fields = [field.coordinates for field in
                                   self.board.board[start_crds].get_empty_adjacent_fields()]
                print(f'[ SHIFT]{command_prompt} >>> ', end='')
                destination_crds = str(input()).upper()
                if destination_crds not in adjacent_fields:
                    raise KeyError
                self.move_pawn(start_crds, destination_crds)

            elif self.pawns_owned == 3:
                print(f'[LAST_3]{command_prompt} Select one of the pawns to move: ')
                # print(self.pawns_coordinates)
                print(f'[LAST_3]{command_prompt} >>> ', end='')
                start_crds = str(input()).upper()
                print(f'[LAST_3]{command_prompt} Choose destination: ')
                # print(self.board.free_fields_coordinates())
                print(f'[LAST_3]{command_prompt} >>> ', end='')
                destination_crds = str(input()).upper()
                self.move_pawn(start_crds, destination_crds)

            elif self.pawns_owned < 3:
                return False

            return True

        except KeyError:
            print('Try again.')
            self.prompt_player_for_move()
            return True

    def prompt_player_for_remove(self):
        command_prompt = f'[REMOVE][{self.name} | on board: {self.pawns_owned - self.pawns_to_deploy}]'

        try:
            print(f'{command_prompt} Select one of the pawns to remove: ')
            # print(self.board.color_fields_coordinates(self.opponent.pawn_color))
            print(f'{command_prompt} >>> ', end='')
            crds = str(input()).upper()
            self.remove_opponents_pawn(crds)

            return True

        except KeyError:
            print('Try again.')
            self.prompt_player_for_remove()

    def get_free_fields_to_deploy(self):
        return self.board.free_fields_coordinates()

    def get_available_pawns_to_move(self):
        movable_pawns = [crds for crds in self.pawns_coordinates if self.board.board[crds].get_empty_adjacent_fields()]
        return movable_pawns
