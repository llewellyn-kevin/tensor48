import numpy as np


class GA:
    def __init__(self, in_nodes, hidden_nodes, out_nodes):
        self.length = 100        
        self.pool_in = np.random.randn(self.length, in_nodes+1, hidden_nodes) 
        self.pool_out = np.random.randn(self.length, hidden_nodes, out_nodes)
        self.pool_fitness = np.zeros(self.length)
        self.nn = NeuralNet(in_nodes, hidden_nodes, out_nodes)


    def next_gen(self):
        print(self.pool_fitness.max())

        num_children = self.length // 3        
        percent_mutation = 0.01
        tournament_cull = 0.8 
        tournament_parent = 0.2 

        in_x, in_y, in_z = self.pool_in.shape
        out_x, out_y, out_z = self.pool_out.shape
 
        child_in = np.zeros((num_children, in_y, in_z) )
        child_out = np.zeros((num_children, out_y, out_z))
        child_fitness = np.zeros(num_children)
        pos_replace = np.zeros(num_children)

        # mate/mutate
        for i in range(num_children):
            # pick pos to replace
            pos_replace[i] = self.tournament(tournament_cull)

            # pick two to mate
            parent1 = self.tournament(tournament_parent)
            parent2 = self.tournament(tournament_parent)
            
            pos_in = np.random.randint(in_y)
            pos_out = np.random.randint(out_y)
            # crossover
            child_in[i][:pos_in] = self.pool_in[parent1][:pos_in]
            child_in[i][pos_in:] = self.pool_in[parent2][pos_in:]
            child_out[i][:pos_in] = self.pool_out[parent1][:pos_in]
            child_out[i][pos_in:] = self.pool_out[parent2][pos_in:]

            
            # mutate 
            
            # add to children

        # replace pool gene with children gene
        for i in range(num_children):
            pos = int(pos_replace[i])
            self.pool_in[pos] = child_in[i]
            self.pool_out[pos] = child_out[i]
            self.pool_fitness[pos] = child_fitness[i]
    
    def tournament(self, percent):
        pos1 = np.random.randint(self.length)
        pos2 = np.random.randint(self.length)
        fit1 = self.pool_fitness[pos1] 
        fit2 = self.pool_fitness[pos2] 
        # higher percent gets lower fitness
        if percent > np.random.random():
            return pos1 if fit1 > fit2 else pos2
        else:
            return pos1 if fit1 <= fit2 else pos2

    
    def get_nn(self, pos):
        self.nn.init_set(self.pool_in[pos], self.pool_out[pos])
        return self.nn


    def set_score(self, pos, score):
        self.pool_fitness[pos] = score


def sigmoid(x):
    return 1 / (1 + np.exp(-x))
# dirived from
# https://databoys.github.io/Feedforward/
class NeuralNet:
    def __init__(self,  in_nodes, hidden_nodes, out_nodes):
        self.input = in_nodes + 1 # add 1 for bias node
        self.hidden = hidden_nodes
        self.output = out_nodes
    
        # set up array of 1s for activations
        self.ai = [1.0] * self.input
        self.ah = [1.0] * self.hidden
        self.ao = [1.0] * self.output
 

    def init_set(self, in_weights, out_weights):
        self.wi = in_weights
        self.wo = out_weights

       
    def init_rand(self):
        # create randomized weights
        self.wi = np.random.randn(self.input, self.hidden) 
        self.wo = np.random.randn(self.hidden, self.output) 


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

