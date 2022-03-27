import game_finished_checker as gfc
import animate_naughts_and_crosses as anm

def naughts_and_crosses(network1, network2, animate = False):
    if animate:
        anm.draw_grid()
    net1_bag = []
    net2_bag = []
    computer_friendly_board = [0, 0, 0, 0, 0, 0, 0, 0, 0] #1 if player 1 has it, -1 if 2 and 0 if available
    for turn in range(9): #9 turns, game unable to be won is not calculated
        if turn % 2 == 0: # if it's player 1's turn
            move = network1.make_move(computer_friendly_board, 1) #returns a legal number to choose
            net1_bag.append(move)
            if animate:
                anm.play_move(move, 'Naught')
            if gfc.contains_3_digits_that_sum_to_15(net1_bag):
                return 'Network 1 wins!'
            computer_friendly_board[move - 1] = 1 #1 has that digit, now
        else: # If it's player 2's turn, shold be symmertric to above
            move = network2.make_move(computer_friendly_board, - 1)
            net2_bag.append(move)
            if animate:
                anm.play_move(move, 'Cross')
            if gfc.contains_3_digits_that_sum_to_15(net2_bag):
                return 'Network 2 wins!'
            computer_friendly_board[move - 1] = -1
    return 'Draw!' #9 moves and no winner