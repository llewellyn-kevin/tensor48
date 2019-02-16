import numpy as np


class GA:
    def __init__(self):
        pass


class Pool:
    def __init__(self):
        self.pool = np.array()
        pass


class Chromosome:
    def __init__(self):
        self.DNA = np.array()
        pass


class Phenotype:
    def __init__(self):
        pass


class Fitness:
    def __init__(self):
        pass


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
# dirived from
# https://databoys.github.io/Feedforward/
class NeuralNet:
    def init_set(self, in_weights, out_weights):
        self.wi = in_weights
        self.wo = out_weights


    def init_rand(self, in_nodes, hidden_nodes, out_nodes):

        self.input = in_nodes + 1 # add 1 for bias node
        self.hidden = hidden_nodes
        self.output = out_nodes

        # set up array of 1s for activations
        self.ai = [1.0] * self.input
        self.ah = [1.0] * self.hidden
        self.ao = [1.0] * self.output

        # create randomized weights
        self.wi = np.random.randn(self.input, self.hidden) 
        self.wo = np.random.randn(self.hidden, self.output) 

        # create arrays of 0 for changes
        self.ci = np.zeros((self.input, self.hidden))
        self.co = np.zeros((self.hidden, self.output))


    def feedForward(self, inputs):
        if len(inputs) != self.input-1:
            raise ValueError('Wrong number of inputs you silly goose!')
        # input activations
        for i in range(self.input -1): # -1 is to avoid the bias
            self.ai[i] = inputs[i]
        # hidden activations
        for j in range(self.hidden):
            sum = 0.0
            for i in range(self.input):
                sum += self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)
        # output activations
        for k in range(self.output):
            sum = 0.0
            for j in range(self.hidden):
                sum += self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)
        return self.ao[:]

