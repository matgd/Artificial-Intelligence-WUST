from futoshiki import Futoshiki
from skyscrapper import Skyscrapper
import time

# F_file = '/home/mateusz/PWr/SI/SI_2/test_data/futoshiki_4_0.txt'
f_s = 1
if f_s == 2:
    for i in range(4, 10):
        for j in range(3):
            if i == 8 and j == 0:
                continue

            F_file = f'/home/mateusz/PWr/SI/SI_2/research_data/test_futo_{i}_{j}.txt'
            #

            # #
            F = Futoshiki(F_file)
            start_sec = time.time()
            # for x in range(F.N):
            #     for y in range(F.N):
            #         print(f'{F.assign_domain_to_cell(x, y)}', end=' ')
            #     print()
            F.solve_what_is_known()

            # F.solve_with_backtracking()
            F.solve_with_look_forward()

            stop_sec = time.time()

            print(f'File:    {F_file}')
            print(f'Time:    {stop_sec - start_sec} s.')
            print(f'Steps:   {F.steps}')
            print(f'Correct: {F.board_valid_sumcheck()}')
            print('==================================')
            F.steps = 0

        # F.save_to_html()
else:
    for i in range(4, 7):
        for j in range(5):
            # S_file = '/home/mateusz/PWr/SI/SI_2/test_data/skyscrapper_5_0.txt'
            S_file = f'research_data/test_sky_{i}_{j}.txt'

            #
            #
            S = Skyscrapper(S_file)
            start_sec = time.time()
            # for i in range(len(S.board)):
            #     for j in range(len(S.board[i])):
            #         print(S.assign_domain_to_cell(i, j, False), end=' ')
            #     print()
            S.solve_what_is_known()

            # print(S.assign_domain_to_cell(5, 4))
            # S.assign_value_to_cell(1, 1, 2)
            # S.assign_value_to_cell(0, 1, 3)

            # S.assign_value_to_cell(1, 2, 2)
            # S.solve_with_backtracking()
            S.solve_with_look_forward()
            stop_sec = time.time()
            print(f'File:    {S_file}')
            print(f'Time:    {stop_sec - start_sec} s.')
            print(f'Steps:   {S.steps}')
            print(f'Correct: {S.board_valid_sumcheck()}')
            print('=SKY===============================')
            S.steps = 0
        # for i in range(len(S.board)):
    #     for j in range(len(S.board[i])):
    #         print(S.assign_domain_to_cell(i, j, False), end=' ')
    #     print()
    print(S.board_valid_sumcheck())
    print(S.steps)
    S.save_to_html()
#
