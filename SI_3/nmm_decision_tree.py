from copy import deepcopy

from nmm_pawn_types import NMM_Pawn

tree_depth = 4


class MiniMax:
    def __init__(self, heuristic, ai_color: NMM_Pawn, game_state):
        self.heuristic = heuristic
        self.game_state = deepcopy(game_state)
        self.ai_color = ai_color
        if ai_color is NMM_Pawn.BLACK:
            self.opponent_color = NMM_Pawn.WHITE
        else:
            self.opponent_color = NMM_Pawn.BLACK

        self.ai = get_player(self.ai_color, self.game_state)

    def return_best_move(self):
        def minimax(game_state, depth, maximizing_player: bool, mill=False):
            game_state_considered = deepcopy(game_state)
            game_is_over = game_state_considered.game_is_over()

            ai = get_player(self.ai_color, game_state_considered)

            if depth == 0 or game_is_over:
                # return [self.heuristic(ai, ai.opponent), ai.move_history[-1]]
                return [self.heuristic(ai, ai.opponent), game_state_considered]
            if maximizing_player:
                value = [float('-inf'), game_state_considered]

                # for _  in range(game_state_considered.board.check_for_mill()):  TODO handle still maximizing when 2
                if mill:
                    available_to_remove = game_state_considered.board.color_fields_coordinates(ai.opponent.pawn_color)
                    for field_crd in available_to_remove:
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        ai_child.remove_opponents_pawn(field_crd)
                        if ai_child.opponent.pawns_owned == 2:
                            value = [float('inf'), game_state_child]
                        else:
                            value = max(value, minimax(game_state_child, depth - 1, False))
                    return value

                elif ai.pawns_to_deploy > 0:
                    for field_crd in ai.get_free_fields_to_deploy():
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        ai_child.place_pawn(field_crd)

                        mill_created_so_maximize = bool(game_state_child.board.check_for_mill())
                        # TODO maybe use number instead of bool to determine 2 mills

                        depth_for_recursion = depth - 1
                        if mill_created_so_maximize:
                            depth_for_recursion += 1
                        value = max(value, minimax(game_state_child, depth_for_recursion, mill_created_so_maximize,
                                                   mill_created_so_maximize))
                    return value

                elif ai.pawns_owned > 3:
                    movable_pawns = ai.get_available_pawns_to_move()
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        available_moves = [field.coordinates for field in
                                           game_state_child.board.board[pawn].get_empty_adjacent_fields()]
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            ai_child_deep = get_player(self.ai_color, game_state_child_deep)
                            ai_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created_so_maximize = bool(game_state_child_deep.board.check_for_mill())
                            # TODO maybe use number instead of bool to determine 2 mills

                            depth_for_recursion = depth - 1
                            if mill_created_so_maximize:
                                depth_for_recursion += 1
                            value = max(value,
                                        minimax(game_state_child_deep, depth_for_recursion, mill_created_so_maximize,
                                                mill_created_so_maximize))
                        return value

                elif ai.pawns_owned == 3:
                    movable_pawns = ai.pawns_coordinates
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        available_moves = game_state_child.board.free_fields_coordinates()
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            ai_child_deep = get_player(self.ai_color, game_state_child_deep)
                            ai_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created_so_maximize = bool(game_state_child_deep.board.check_for_mill())
                            # TODO maybe use number instead of bool to determine 2 mills

                            depth_for_recursion = depth - 1
                            if mill_created_so_maximize:
                                depth_for_recursion += 1
                            value = max(value,
                                        minimax(game_state_child_deep, depth_for_recursion, mill_created_so_maximize,
                                                mill_created_so_maximize))
                        return value

            else:  # minimizing_player
                value = [float('inf'), game_state_considered]

                # for _  in range(game_state_considered.board.check_for_mill()):  TODO handle still maximizing when 2
                if mill:
                    available_to_remove = game_state_considered.board.color_fields_coordinates(ai.pawn_color)
                    for field_crd in available_to_remove:
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.ai.opponent.pawn_color, game_state_child)
                        opponent_child.remove_opponents_pawn(field_crd)

                        if opponent_child.opponent.pawns_owned == 2:
                            value = [float('-inf'), game_state_child]
                        else:
                            value = min(value, minimax(game_state_child, depth - 1, True))
                    return value

                elif ai.opponent.pawns_to_deploy > 0:
                    for field_crd in ai.opponent.get_free_fields_to_deploy():
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.opponent_color, game_state_child)
                        opponent_child.place_pawn(field_crd)

                        mill_created = bool(game_state_child.board.check_for_mill())  # returns True if mill
                        # TODO maybe use number instead of bool to determine 2 mills
                        depth_for_recursion = depth - 1
                        if mill_created:
                            depth_for_recursion += 1
                        value = min(value,
                                    minimax(game_state_child, depth_for_recursion, not mill_created, mill_created))
                    return value

                elif ai.pawns_owned > 3:
                    movable_pawns = ai.opponent.get_available_pawns_to_move()
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.opponent_color, game_state_child)
                        available_moves = [field.coordinates for field in
                                           game_state_child.board.board[pawn].get_empty_adjacent_fields()]
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            opponent_child_deep = get_player(self.opponent_color, game_state_child_deep)
                            opponent_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created = bool(game_state_child_deep.board.check_for_mill())  # returns True if mill
                            # TODO maybe use number instead of bool to determine 2 mills
                            depth_for_recursion = depth - 1
                            if mill_created:
                                depth_for_recursion += 1
                            value = min(value, minimax(game_state_child_deep, depth_for_recursion, not mill_created,
                                                       mill_created))
                        return value

                elif ai.pawns_owned == 3:
                    movable_pawns = ai.opponent.pawns_coordinates
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.opponent_color, game_state_child)
                        available_moves = game_state_child.board.free_fields_coordinates()
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            opponent_child_deep = get_player(self.opponent_color, game_state_child_deep)
                            opponent_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created = bool(game_state_child_deep.board.check_for_mill())  # returns True if mill
                            # TODO maybe use number instead of bool to determine 2 mills
                            depth_for_recursion = depth - 1
                            if mill_created:
                                depth_for_recursion += 1
                            value = min(value, minimax(game_state_child_deep, depth_for_recursion, not mill_created,
                                                       mill_created))
                        return value

        minimax_result = minimax(self.game_state, tree_depth, True)
        no_moves = len(self.game_state.board.move_history)
        if len(minimax_result[1].board.move_history) == no_moves:
            return False
        return (minimax_result[1].board.move_history[no_moves],  # - tree depth cause we get the leaf node
                minimax_result[1].board.move_history[no_moves + 1])  # get next in case of removal


class AlphaBeta:
    def __init__(self, heuristic, ai_color: NMM_Pawn, game_state):
        self.heuristic = heuristic
        self.game_state = deepcopy(game_state)
        self.ai_color = ai_color
        if ai_color is NMM_Pawn.BLACK:
            self.opponent_color = NMM_Pawn.WHITE
        else:
            self.opponent_color = NMM_Pawn.BLACK

        self.ai = get_player(self.ai_color, self.game_state)

    def return_best_move(self):
        def alphabeta(game_state, depth, alpha, beta, maximizing_player: bool, mill=False):
            game_state_considered = deepcopy(game_state)
            game_is_over = game_state_considered.game_is_over()

            ai = get_player(self.ai_color, game_state_considered)

            if depth == 0 or game_is_over:
                # return [self.heuristic(ai, ai.opponent), ai.move_history[-1]]
                return [self.heuristic(ai, ai.opponent), game_state_considered]
            if maximizing_player:
                value = [float('-inf'), game_state_considered]

                # for _  in range(game_state_considered.board.check_for_mill()):  TODO handle still maximizing when 2
                if mill:
                    available_to_remove = game_state_considered.board.color_fields_coordinates(ai.opponent.pawn_color)
                    for field_crd in available_to_remove:
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        ai_child.remove_opponents_pawn(field_crd)
                        if ai_child.opponent.pawns_owned == 2:
                            value = [float('inf'), game_state_child]
                        else:
                            value = max(value, alphabeta(game_state_child, depth - 1, alpha, beta, False))
                        alpha = max(alpha, value)
                        if alpha >= beta and depth >= 2:  # depth >= 2 - cant cut too soon if removal is after
                            break
                    return value

                elif ai.pawns_to_deploy > 0:
                    for field_crd in ai.get_free_fields_to_deploy():
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        ai_child.place_pawn(field_crd)

                        mill_created_so_maximize = bool(game_state_child.board.check_for_mill())
                        # TODO maybe use number instead of bool to determine 2 mills

                        depth_for_recursion = depth - 1
                        if mill_created_so_maximize:
                            depth_for_recursion += 1
                        value = max(value, alphabeta(game_state_child, depth_for_recursion, alpha, beta,
                                                     mill_created_so_maximize, mill_created_so_maximize))
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            break
                    return value

                elif ai.pawns_owned > 3:
                    movable_pawns = ai.get_available_pawns_to_move()
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        available_moves = [field.coordinates for field in
                                           game_state_child.board.board[pawn].get_empty_adjacent_fields()]
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            ai_child_deep = get_player(self.ai_color, game_state_child_deep)
                            ai_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created_so_maximize = bool(game_state_child_deep.board.check_for_mill())
                            # TODO maybe use number instead of bool to determine 2 mills

                            depth_for_recursion = depth - 1
                            if mill_created_so_maximize:
                                depth_for_recursion += 1
                            value = max(value, alphabeta(game_state_child_deep, depth_for_recursion, alpha, beta,
                                                         mill_created_so_maximize, mill_created_so_maximize))
                            alpha = max(alpha, value)
                            if alpha >= beta and depth >= 2:
                                break
                        return value

                elif ai.pawns_owned == 3:
                    movable_pawns = ai.pawns_coordinates
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        ai_child = get_player(self.ai_color, game_state_child)
                        available_moves = game_state_child.board.free_fields_coordinates()
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            ai_child_deep = get_player(self.ai_color, game_state_child_deep)
                            ai_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created_so_maximize = bool(game_state_child_deep.board.check_for_mill())
                            # TODO maybe use number instead of bool to determine 2 mills

                            depth_for_recursion = depth - 1
                            if mill_created_so_maximize:
                                depth_for_recursion += 1
                            value = max(value, alphabeta(game_state_child_deep, depth_for_recursion, alpha, beta,
                                                         mill_created_so_maximize, mill_created_so_maximize))
                            alpha = max(alpha, value)
                            if alpha >= beta and depth >= 2:
                                break
                        return value

            else:  # minimizing_player
                value = [float('inf'), game_state_considered]

                # for _  in range(game_state_considered.board.check_for_mill()):  TODO handle still maximizing when 2
                if mill:
                    available_to_remove = game_state_considered.board.color_fields_coordinates(ai.pawn_color)
                    for field_crd in available_to_remove:
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.ai.opponent.pawn_color, game_state_child)
                        opponent_child.remove_opponents_pawn(field_crd)

                        if opponent_child.opponent.pawns_owned == 2:
                            value = [float('-inf'), game_state_child]
                        else:
                            value = min(value, alphabeta(game_state_child, depth - 1, alpha, beta, True))
                        beta = min(beta, value)
                        if alpha >= beta and depth >= 2:
                            break
                    return value

                elif ai.opponent.pawns_to_deploy > 0:
                    for field_crd in ai.opponent.get_free_fields_to_deploy():
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.opponent_color, game_state_child)
                        opponent_child.place_pawn(field_crd)

                        mill_created = bool(game_state_child.board.check_for_mill())  # returns True if mill
                        # TODO maybe use number instead of bool to determine 2 mills
                        depth_for_recursion = depth - 1
                        if mill_created:
                            depth_for_recursion += 1
                        value = min(value,
                                    alphabeta(game_state_child, depth_for_recursion, alpha, beta, not mill_created,
                                              mill_created))
                        beta = min(beta, value)
                        if alpha >= beta and depth >= 2:
                            break
                    return value

                elif ai.pawns_owned > 3:
                    movable_pawns = ai.opponent.get_available_pawns_to_move()
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.opponent_color, game_state_child)
                        available_moves = [field.coordinates for field in
                                           game_state_child.board.board[pawn].get_empty_adjacent_fields()]
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            opponent_child_deep = get_player(self.opponent_color, game_state_child_deep)
                            opponent_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created = bool(game_state_child_deep.board.check_for_mill())  # returns True if mill
                            # TODO maybe use number instead of bool to determine 2 mills
                            depth_for_recursion = depth - 1
                            if mill_created:
                                depth_for_recursion += 1
                            value = min(value, alphabeta(game_state_child_deep, depth_for_recursion, alpha, beta,
                                                         not mill_created, mill_created))
                            beta = min(beta, value)
                            if alpha >= beta and depth >= 2:
                                break
                        return value

                elif ai.pawns_owned == 3:
                    movable_pawns = ai.opponent.pawns_coordinates
                    for pawn in movable_pawns:
                        game_state_child = deepcopy(game_state_considered)
                        opponent_child = get_player(self.opponent_color, game_state_child)
                        available_moves = game_state_child.board.free_fields_coordinates()
                        for move_coordinates in available_moves:
                            game_state_child_deep = deepcopy(game_state_child)
                            opponent_child_deep = get_player(self.opponent_color, game_state_child_deep)
                            opponent_child_deep.move_pawn(pawn, move_coordinates)

                            mill_created = bool(game_state_child_deep.board.check_for_mill())  # returns True if mill
                            # TODO maybe use number instead of bool to determine 2 mills
                            depth_for_recursion = depth - 1
                            if mill_created:
                                depth_for_recursion += 1
                            value = min(value, alphabeta(game_state_child_deep, depth_for_recursion, alpha, beta,
                                                         not mill_created, mill_created))
                            beta = min(beta, value)
                            if alpha >= beta and depth >= 2:
                                break
                        return value

        alphabeta_result = alphabeta(self.game_state, tree_depth, [float('-inf'), deepcopy(self.game_state)],
                                     [float('inf'), deepcopy(self.game_state)], True)
        no_moves = len(self.game_state.board.move_history)
        if len(alphabeta_result[1].board.move_history) == no_moves:
            return False
        print(alphabeta_result[1].board.move_history)

        result_1 = alphabeta_result[1].board.move_history[no_moves]
        try:
            result_2 = alphabeta_result[1].board.move_history[no_moves + 1]
        except:
            result_2 = None

        return result_1, result_2  # get next in case of removal


def get_player(color, game_state):
    if game_state.player1.pawn_color is color:
        ai = game_state.player1
    else:
        ai = game_state.player2

    return ai
