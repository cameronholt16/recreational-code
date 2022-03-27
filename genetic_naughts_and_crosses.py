import Player as pl
import naughts_and_crosses_sim as ncsim
import mutate as mt
import population_winrate_against_newb as pwan
import animate_naughts_and_crosses as anm

import random as rd
import numpy as np

def genetic_naughts_and_crosses(num_players, num_generations, num_test_newbs, arct, mutation_rate): #arct is the neural network architecture
    #hyperparams drawn from standard normal
    newbs = [pl.Player(arct) for i in range (num_test_newbs)] #for testing
    players = [pl.Player(arct) for i in range (num_players)]
    best_performance = 0
    for i in range (num_generations):
        #print('start of generation', i)
        rd.shuffle(players)
        survivors = []
        next_generation = []
        for j in range (num_players//2): #for every pair of players
            #print('start of match', j)
            player1 = players[2*j]
            player2 = players[(2*j)+1]
            player1_wins = 0
            player2_wins = 0
            draws = 0 #for debugging and analysis
            #play once in each role:
            #print('start of round 1:', k)
            result = ncsim.naughts_and_crosses(player1, player2)
            if result == 'Network 1 wins!':
                player1_wins += 1
            elif result == 'Network 2 wins!':
                player2_wins += 1
            elif result == 'Draw!':
                draws += 1
            else:
                print('Did not get a proper result :(')
            #print('start of round 2:', k)
            result = ncsim.naughts_and_crosses(player2, player1) #swap sides
            if result == 'Network 1 wins!':
                player2_wins += 1 #other guy has now won
            elif result == 'Network 2 wins!':
                player1_wins += 1
            elif result == 'Draw!':
                draws += 1
            else:
                print('Did not get a proper result :(')
            if player2_wins > player1_wins:
                survivors.append(player2)
            else:
                survivors.append(player1) #player 1 chosen at random because rd.shuffle
        #print('start of mutations')
        for player in survivors: #add a mutated version
            #print('started considering a player')
            next_generation.append(player)
            next_generation.append(mt.mutate(player, mutation_rate))
        test_score = pwan.test_contest(next_generation, newbs)
        print(test_score)
        if test_score > best_performance:
            players = next_generation
            best_performance = test_score
        #if i % 5000 == 0: #show me a game every 500 gens
         #   ncsim.naughts_and_crosses(players[0], rd.choice(newbs), animate = True)
          #  anm.new_game()
           # ncsim.naughts_and_crosses(rd.choice(newbs), players[0], animate = True)
            #anm.new_game()

genetic_naughts_and_crosses(40, 100000, 200, np.array([10, 5, 9]), 0.001) ###