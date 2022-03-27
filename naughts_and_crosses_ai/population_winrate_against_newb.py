import naughts_and_crosses_sim as ncsim
import math
import random as rd

def test_contest(player, newbs):
    player_wins = 0
    newb_wins = 0
    for newb in newbs:
        result1 = ncsim.naughts_and_crosses(player, newb)
        result2 = ncsim.naughts_and_crosses(newb, player)
        if result1 == 'Network 1 wins!':
            player_wins += 1
        elif result1 == 'Network 2 wins!':
            newb_wins += 1
        if result2 == 'Network 1 wins!':
            newb_wins += 1
        elif result2 == 'Network 2 wins!':
            player_wins += 1
    if newb_wins == 0 and player_wins > 0:
        return math.inf
    if newb_wins == 0:
        return 1
    return player_wins / newb_wins