from nmm_player import NMM_Player
from nmm_board import NMM_Board
from nmm_pawn_types import NMM_Pawn


class NMM_AI(NMM_Player):
    def __init__(self, board: NMM_Board, pawn_color: NMM_Pawn, algorithm_name: str, heuristic, name=None):
        super().__init__(board, pawn_color, name)

        assert algorithm_name == 'mini-max' or algorithm_name == 'alpha-beta'
        self.algorithm_name = algorithm_name
        self.heuristic = heuristic

    def prompt_ai_for_move(self, coords):

        command_prompt = f'[{self.name} | on board: {self.pawns_owned - self.pawns_to_deploy}]'

        if self.pawns_to_deploy > 0:
            free_fields_coordinates = self.board.free_fields_coordinates()

            print(f'[DEPLOY]{command_prompt} Please provide coordinates: ')
            # print(free_fields_coordinates)
            print(f'[DEPLOY]{command_prompt} >>> ', end='')
            coordinates = coords[0]
            print(coordinates)
            self.place_pawn(coordinates)

        elif self.pawns_owned > 3:
            print(f'[ SHIFT]{command_prompt} Select one of the pawns to move: ')
            movable_pawns = [crds for crds in self.pawns_coordinates if
                             self.board.board[crds].get_empty_adjacent_fields()]
            if not movable_pawns:
                return False
            # print(movable_pawns)
            print(f'[ SHIFT]{command_prompt} >>> ', end='')
            start_crds = coords[0]
            if start_crds not in movable_pawns:
                raise KeyError(start_crds)
            print(start_crds)
            print(f'[ SHIFT]{command_prompt} Choose destination: ')
            # print([crds for crds in self.board.board[start_crds].get_empty_adjacent_fields()])
            print(f'[ SHIFT]{command_prompt} >>> ', end='')
            destination_crds = coords[1]
            print(destination_crds)
            self.move_pawn(start_crds, destination_crds)

        elif self.pawns_owned == 3:
            print(f'[LAST_3]{command_prompt} Select one of the pawns to move: ')
            # print(self.pawns_coordinates)
            print(f'[LAST_3]{command_prompt} >>> ', end='')
            start_crds = coords[0]
            print(start_crds)
            print(f'[LAST_3]{command_prompt} Choose destination: ')
            # print(self.board.free_fields_coordinates())
            print(f'[LAST_3]{command_prompt} >>> ', end='')
            destination_crds = coords[1]
            print(destination_crds)
            self.move_pawn(start_crds, destination_crds)

        return True

    def prompt_ai_for_remove(self, coords):
        # TODO: Change human-way interaction to AI-way
        command_prompt = f'[REMOVE][{self.name} | on board: {self.pawns_owned - self.pawns_to_deploy}]'

        assert coords[0] == 'REMOVED'

        try:
            print(f'{command_prompt} Select one of the pawns to remove: ')
            # print(self.board.color_fields_coordinates(self.opponent.pawn_color))
            print(f'{command_prompt} >>> ', end='')
            crds = coords[1]
            print(crds)
            self.remove_opponents_pawn(crds)

            return True

        except KeyError:
            print('Try again.')
            self.prompt_player_for_remove()

    def choose_best_move(self):
        pass
