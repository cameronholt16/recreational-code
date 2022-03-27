import random as rd
import numpy as np
from copy import deepcopy

def mutate(player, mutation_rate): #object of Player class
    new_player = deepcopy(player)
    weight_peturbations = [np.random.randn(new_player.arct[i], new_player.arct[i+1]) for i in range (new_player.num_layers-1)]
    bias_peturbations = [np.random.randn(new_player.arct[i]) for i in range (new_player.num_layers)]
    adjusted_weight_peturbations = [x * mutation_rate for x in weight_peturbations]
    adjusted_bias_peturbations = [x * mutation_rate for x in bias_peturbations]
    new_player.weights = [sum(x) for x in zip(new_player.weights, adjusted_weight_peturbations)]
    new_player.biases = [sum(x) for x in zip(new_player.biases, adjusted_bias_peturbations)]
    return new_player