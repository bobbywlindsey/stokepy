import numpy as np
import sympy

class Metropolis:

    def __init__(self, co_domain, current_state):
        self.co_domain = co_domain
        self.current_state = current_state
        # number of neighbors
        self.d = sympy.binomial(len(self.co_domain), 2)
        self.J_unif_prob = 1/self.d
        pass

    def run(self):
        # generate neighbors
        neighbors = self.generate_neighbors()
        # pick neighbor
        chosen_neighbor = neighbors[self.pick_neighbor()]
        print(chosen_neighbor)

    def plausibility(self):
        # TODO: generate Markov chain from data
        pass

    def generate_neighbors(self):
        neighbors = []
        for index in range(0, len(self.current_state) - 1):
            for i in range(index+1, len(self.current_state)):
                transposition = list(self.current_state)

                first_number = self.current_state[index]
                second_number = self.current_state[i]

                transposition[index] = second_number
                transposition[i] = first_number

                neighbors.append(transposition)
        return neighbors

    def pick_neighbor(self):
        # get number of possible neighbors
        random_probability = np.random.rand()
        for neighbor in range(self.d):
            random_probability = random_probability - self.J_unif_prob
            if random_probability < 0:
                chosen_neighbor = neighbor
                return chosen_neighbor

m = Metropolis([3, 6, 7, 3, 4], [1, 2, 3, 4, 5])
neighbors = m.run()
