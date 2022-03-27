import Player as pl
import naughts_and_crosses_sim as ncsim
import mutate as mt
import population_winrate_against_newb as pwan
import animate_naughts_and_crosses as anm

import random as rd
import numpy as np

def round_robin_naughts_and_crosses(num_players, num_generations, num_test_newbs, arct, mutation_rate, report_every_n, animate_every_n): #arct is the neural network architecture
    #hyperparams drawn from standard normal
    newbs = [pl.Player(arct) for i in range (num_test_newbs)] #for testing
    players = [pl.Player(arct) for i in range (num_players)]
    for i in range (num_generations):
        player_wins = [0]*num_players
        draws = 0 # for analysis
        for player1 in players:
            for player2 in players: #for every pair of players, including reverse fixtures
                if player1 != player2:
                    result = ncsim.naughts_and_crosses(player1, player2)
                    if result == 'Network 1 wins!':
                        player_wins[players.index(player1)] += 1
                    elif result == 'Network 2 wins!':
                        player_wins[players.index(player2)] += 1
                    elif result == 'Draw!':
                        draws += 1
                    else:
                        print('Did not get a proper result :(')
        for_sorting = players.copy()
        players.sort(key = lambda player: player_wins[for_sorting.index(player)], reverse = True)
        if i % report_every_n == 0: # print performance against test newbs
            champion_test_score = pwan.test_contest(players[0], newbs)
            print('Champions score against newbs = ', champion_test_score)
            median_test_score = pwan.test_contest(players[num_players//2], newbs)
            print('Medians score against newbs = ', median_test_score)
            loser_test_score = pwan.test_contest(players[-1], newbs)
            print('Losers score against newbs = ', loser_test_score)
        for j in range(num_players-10): #For players who finished outside the top 10
            players[j+10] = mt.mutate(rd.choice(players[:10]), mutation_rate) # replace with a mutant of a top 10
        if i % animate_every_n == 0: # print performance against test newbs then show me a pair of games every 500 gens
            ncsim.naughts_and_crosses(players[0], rd.choice(newbs), animate = True) #champ vs newb
            anm.new_game()
            ncsim.naughts_and_crosses(rd.choice(newbs), players[0], animate = True) #newb vs champ
            anm.new_game()

round_robin_naughts_and_crosses(50, 500, 100, np.array([10, 5, 9]), 0.1, 20, 100)