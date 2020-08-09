from enum import IntEnum
from random import randint, shuffle
from time import time

from nmm_ai import NMM_AI
from nmm_board import NMM_Board
from nmm_player import NMM_Player
from nmm_pawn_types import NMM_Pawn
from nmm_decision_tree import MiniMax, AlphaBeta
from nmm_heuristic import *


class GamePhase(IntEnum):
    DEPLOYMENT_PHASE = 1
    SHIFT_PHASE = 2
    THREE_STANDING_PHASE = 3

class NMM_Game:
    def __init__(self):
        self.board = NMM_Board()
        self.player1 = NMM_Player(self.board, NMM_Pawn.WHITE, 'Human')
        self.player2 = NMM_Player(self.board, NMM_Pawn.BLACK, 'Human 2')
        self.player1.assign_opponent(self.player2)
        self.player2.assign_opponent(self.player1)
        self.players = [self.player1, self.player2]
        self.phase = GamePhase.DEPLOYMENT_PHASE
        self.__choose_player_order()

    def __choose_player_order(self):
        shuffle(self.players)

    def main_menu(self):
        answer = None
        print()
        print(80 * '=')
        print('Welcome!')
        print(80 * '=')
        while answer not in [1, 2, 3]:
            print('Please choose game type:')
            print('1. Human vs Human')
            print('2. Human vs AI')
            print('3. AI vs AI')
            answer = int(input('>>> '))
            print()
            if answer == 1:
                pass
                return 1

        if answer == 2:
            strategy = 'mini-max'
            answer = None
            answer_heuristic = None
            while answer not in [1, 2]:
                print('Please choose AI strategy:')
                print('1. Min-max')
                print('2. Alpha-beta')
                answer = int(input('>>> '))
                print()
            if answer == 1:
                strategy = 'mini-max' 
            elif answer == 2:
                strategy = 'alpha-beta'

            while answer_heuristic not in [1, 2, 3, 4]:
                print('Please choose heuristic:')
                print(f'1. {removed_difference_ratio.__name__}')
                print(f'2. {empty_adjacent_fields.__name__}')
                print(f'3. {empty_adjacent_fields_dont_mind_enemy.__name__}')
                print(f'4. {good_start.__name__}')
                answer_heuristic = int(input('>>> '))
                print()
            if answer_heuristic == 1:
                heuristic = removed_difference_ratio
            elif answer_heuristic == 2:
                heuristic = empty_adjacent_fields
            elif answer_heuristic == 3:
                heuristic = empty_adjacent_fields_dont_mind_enemy
            elif answer_heuristic == 4:
                heuristic = good_start

            self.player2 = NMM_AI(self.board, NMM_Pawn.BLACK, strategy, heuristic, f'CPU_{strategy}')
            self.player1.assign_opponent(self.player2)
            self.player2.assign_opponent(self.player1)
            self.players = [self.player1, self.player2]
            self.__choose_player_order()
            return 2

        if answer == 3:
            strategies = []
            heuristics = []
            for i in range(2):
                answer = None
                answer_heuristic = None
                while answer not in [1, 2]:
                    print(f'Please choose AI {i+1} strategy:')
                    print('1. Min-max')
                    print('2. Alpha-beta')
                    answer = int(input('>>> '))
                    print()
                if answer == 1:
                    strategies.append('mini-max')
                elif answer == 2:
                    strategies.append('alpha-beta')

                while answer_heuristic not in [1, 2, 3, 4]:
                    print('Please choose heuristic:')
                    print(f'1. {removed_difference_ratio.__name__}')
                    print(f'2. {empty_adjacent_fields.__name__}')
                    print(f'3. {empty_adjacent_fields_dont_mind_enemy.__name__}')
                    print(f'4. {good_start.__name__}')
                    answer_heuristic = int(input('>>> '))
                    print()
                if answer_heuristic == 1:
                    heuristics.append(removed_difference_ratio)
                elif answer_heuristic == 2:
                    heuristics.append(empty_adjacent_fields)
                elif answer_heuristic == 3:
                    heuristics.append(empty_adjacent_fields_dont_mind_enemy)
                elif answer_heuristic == 4:
                    heuristics.append(good_start)
            self.player1 = NMM_AI(self.board, NMM_Pawn.WHITE, strategies[0], heuristics[0], f'CPU_1_{strategies[0]}')
            self.player2 = NMM_AI(self.board, NMM_Pawn.BLACK, strategies[1], heuristics[1], f'CPU_2_{strategies[1]}')
            self.player1.assign_opponent(self.player2)
            self.player2.assign_opponent(self.player1)
            self.players = [self.player1, self.player2]
            self.__choose_player_order()
            return 3

        return 0

    def start(self, window):
        start_time = time()
        print(f'Start for {self.players[0].pawn_color.name}')
        while True:
            for player in self.players:
                move = None
                if isinstance(player, NMM_AI):
                    if player.algorithm_name == 'mini-max':
                        algorithm = MiniMax(player.heuristic, player.pawn_color, self)
                    elif player.algorithm_name == 'alpha-beta':
                        algorithm = AlphaBeta(player.heuristic, player.pawn_color, self)
                    move = algorithm.return_best_move()
                    if player.pawns_owned < 3 or not move:
                        print('=' * 80)
                        print('GAME OVER')
                        print('=' * 80)
                        print(f'Player {player.name} has lost!')
                        winner = self.players.copy()
                        winner.remove(player)
                        winner = winner[0]
                        print(f'Player {winner.name} has won!')
                        print(f'Time: {time() - start_time}s.')
                        print(f'Total moves: {len(self.board.move_history)}')
                        print(f'{player.name} moves: {len(player.move_history)}')
                        print(f'{winner.name} moves: {len(winner.move_history)}')
                        print('=' * 80)
                        return winner
                    player.prompt_ai_for_move(move[0])
                elif player.pawns_owned < 3 or not player.prompt_player_for_move():
                    print('GAME OVER')
                    print(f'Player {player.name} has lost!')
                    winner = self.players.copy()
                    winner.remove(player)
                    winner = winner[0]
                    print(f'Player {winner.name} has won!')
                    return winner

                window.repaint()
                for _ in range(self.board.check_for_mill()):
                    # minimax.game_state = self  # game state changes after pawn placement
                    if isinstance(player, NMM_AI):
                        # remove = minimax.return_best_move()
                        player.prompt_ai_for_remove(move[1])
                    else:
                        player.prompt_player_for_remove()
                    window.repaint()

    def game_is_over(self):
        for player in self.players:
            if player.pawns_owned < 3:
                return True
            if player.pawns_to_deploy == 0:
                if not player.get_available_pawns_to_move() and player.pawns_owned > 3:
                    return True

        return False

    def __lt__(self, other):
        return True

    def __ge__(self, other):
        return True