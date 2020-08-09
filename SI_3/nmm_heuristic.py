from nmm_player import NMM_Player


def removed_difference_ratio(guided_player: NMM_Player, enemy_player: NMM_Player):
    return guided_player.pawns_taken - enemy_player.pawns_taken


def empty_adjacent_fields(guided_player: NMM_Player, enemy_player: NMM_Player):
    no_empty_adjacent_fields = 0
    no_empty_adjacent_fields_opponent = 0

    for pawn in guided_player.pawns_coordinates:
        no_empty_adjacent_fields += len(guided_player.board.board[pawn].get_empty_adjacent_fields())

    for pawn in enemy_player.pawns_coordinates:
        no_empty_adjacent_fields_opponent += len(enemy_player.board.board[pawn].get_empty_adjacent_fields())

    return (no_empty_adjacent_fields + (guided_player.pawns_taken * 5)) - \
           ((enemy_player.pawns_taken * 5))  # samuraj, jak w następnym ruchu przegra przez młynek to potrafi
    # zrobić hara-kiri i się zablokować by przegrać
    # tree depth = 3
    # alpha beta x2
    # + usunięcie z warunku game_is_over pawns > 3

    # return (no_empty_adjacent_fields * guided_player.pawns_taken) \
    #       - (no_empty_adjacent_fields_opponent - enemy_player.pawns_taken)


def empty_adjacent_fields_dont_mind_enemy(guided_player: NMM_Player, enemy_player: NMM_Player):
    no_empty_adjacent_fields = 0

    for pawn in guided_player.pawns_coordinates:
        no_empty_adjacent_fields += len(guided_player.board.board[pawn].get_empty_adjacent_fields())

    return no_empty_adjacent_fields * guided_player.pawns_taken


def good_start(guided_player: NMM_Player, enemy_player: NMM_Player):
    no_empty_adjacent_fields = 0

    if guided_player.pawns_to_deploy > 0:
        for pawn in guided_player.pawns_coordinates:
            no_empty_adjacent_fields += len(guided_player.board.board[pawn].get_empty_adjacent_fields())
        return no_empty_adjacent_fields
    else:
        return guided_player.pawns_taken - enemy_player.pawns_taken
