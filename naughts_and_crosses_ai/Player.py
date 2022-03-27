import numpy as np

class Player:
    def __init__(self, arct):
        self.arct = arct
        self.num_layers = len(self.arct)
        self.weights = [np.random.randn(self.arct[i], self.arct[i+1]) for i in range (self.num_layers-1)]
        self.biases = [np.random.randn(self.arct[i]) for i in range (self.num_layers)] #biases made for inputs, which I don't use

    def make_move(self, board, role): #board in computer friendly form, role is +-1
        #multiply all illegal outputs by 0, -inf or summat at the very end
        # initialise arrays of activations and inputs
        activations = board.copy()
        activations.append(role) #10 nodes, last one tells the network what player it is
        for i in range(self.num_layers-1): #for every layer except the last, calculate the activations of the next layer
            activations = self.squish(np.dot(activations, self.weights[i])-self.biases[i+1]) #weights is a matrix, 'dot' means vector-matrix product. From my perspective, vectors are horizontal in numpy
            #weights i is weights leaving layer i. biases i+1 is biases into layer i+1.
        for i in range(len(board)):
            if board[i] != 0: #if the output isn't legal:
                activations[i] = 0 # sigmoid puts you in (0,1)
        #I am worried that the thing below will not break ties
        return np.argmax(activations) + 1 #chosen number = index of the chosen number + 1
        
    def squish(self, weighted_inputs, squish_choice = 'sigmoid'):
        if squish_choice == 'sigmoid':
            return (1/(1+np.exp(-1*weighted_inputs)))
        else:
            print('You have asked for a squish function I do not yet have')

    