#remove the swearing
#unfinished
#apply to 0s and Xs

import random #for weights and biases
import numpy as np # for matrices

#np.dot doesn't make this easy, so I do it myself
def matrix_of_vectors(a,b):
    result = np.zeros([a.size, b.size])
    for i in range(a.size):
        result[i] = a[i]*b
    return result
        

class Network:
    def __init__(self, arct):
    # arct (architecture) will be a list of number of nodes, layers read left to right. e.g. np.array([2,2,3]) is 2 input nodes, 3 output nodes and one hidden layer of 2 nodes
        self.arct = arct
        self.num_layers = len(self.arct)
        self.weights = [np.random.randn(self.arct[i], self.arct[i+1]) for i in range (self.num_layers-1)] #list of matrices
        self.biases = [np.random.randn(self.arct[i]) for i in range (self.num_layers)] #list of vectors. I create biases for input neurons, but don't use them, so the indexing is comfortable for me.
        
    def passthrough(self, image):
        #PROBLEM: WORK OUT HOW TO INSERT. AXIS??
        # initialise arrays of activations and inputs
        activations = [image]
        unsquished = [image] #first layer doesn't (?) get squished
        for i in range(self.num_layers-1): #for every layer except the last, calculate the activations of the next layer
            unsquished.append(np.dot(activations[i], self.weights[i])-self.biases[i+1]) #weights is a matrix, 'dot' means vector-matrix product. From my perspective, vectors are horizontal in numpy
            #weights i is weights leaving layer i. biases i+1 is biases into layer i+1.
            activations.append(self.squish(unsquished[i+1])) # Squish the activations into a small range
        return [activations, unsquished] # all activations and all unsquished inputs, unsqished needed for backprop
    
    def squish(self, weighted_inputs, squish_choice = 'sigmoid'):
        if squish_choice == 'sigmoid':
            return (1/(1+np.exp(-1*weighted_inputs)))
        else:
            print('You have asked for a squish function I do not yet have')
    
    def squish_prime(self, weighted_inputs, squish_choice = 'sigmoid'): #Derivative of the squish function, used in backprop algorithm. Thankfully simple for sigmoid.
        if squish_choice == 'sigmoid':
            s=self.squish(weighted_inputs, squish_choice = 'sigmoid')
            return s*(s-1)
        else:
            print('You have asked for the derivative of a squish function I do not yet have')
        
    def cost(self, image, expected_output, cost_choice='quadratic'):
        if cost_choice == 'quadratic':
            actual_output = self.passthrough(image)[0][-1]
            difference = []
            for (actual, expected) in zip (actual_output, expected_output):
                difference.append(actual-expected)
            return np.dot(difference, difference)/(2*self.arct[-1]) #Mean square error of output. Factor of 2 is so BP1 calculation is nice
        else:
            print('You have asked for me to use a cost function I do not yet have')
    
    def backprop(self, image, expected_output, neta, cost_choice = 'quadratic'):
        if cost_choice == 'quadratic': #clumsy to need to specify cost function twice. Backprop depends on cost choice
            output_a, output_z = self.passthrough(image) # post and pre squish. Naming following michael nielsen's book
            #errors is a measure of how the algorithm wants the weights and biases to change
            errors =  [np.multiply((output_a[-1] - expected_output), self.squish_prime(output_z[-1]))] #1 element list of the vector of outputs
            #np.multiply is element wise multiplication
        else:
            print('You have asked for me to use a cost function I do not yet have')
        for i in range (self.num_layers - 1): #for all but the last layer, calculate errors
            #calculate everything in the wrong order then reverse it
            #errors below needs to be a sum over "to" neurons k
            errors.append(np.multiply(self.squish_prime(output_z[-(i+2)]), np.dot(errors[i], np.transpose(self.weights[-(i+1)])))) #
        errors.reverse()
        for i in range(self.num_layers-1):
            self.biases[i+1] = self.biases[i+1] - neta * errors[i+1] #this needs to be a minus, but the weight_grad is plus??
        #errors give bias' gradients directly
        #calculate an array of 2d arrays, same shape as weights, of gradients
        weight_grad = []
        for i in range (self.num_layers-1):
            weight_grad.append(matrix_of_vectors(output_a[i], errors[i+1])) #errors i+1 cuz I calculated all the errors, instead of all but input layer's
        #uncomment the biases when u actually do 'em
        #self.biases = self.biases - neta*errors # are these the same shape?
        for i in range(self.num_layers-1):
            self.weights[i] = self.weights[i] + neta * weight_grad[i] #I would exepct this to be a -. Hopefully just a harmless sign error
           
    
    
uninteresting_network=Network(np.array([2,2,3,4]))
print(uninteresting_network.cost(np.array([0.1, 0.45]), np.array([1, 1, 1, 1])))
for _ in range(1000):
    uninteresting_network.backprop(np.array([0.1, 0.45]), np.array([1, 1, 1, 1]), 0.1)
print(uninteresting_network.cost(np.array([0.1, 0.45]), np.array([1, 1, 1, 1])))