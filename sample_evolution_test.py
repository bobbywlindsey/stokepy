import stokepy as sp
import numpy as np

# define transition matrix
P = np.array([[0, .5, 0, .5, 0, 0, 0, 0, 0], \
              [1/3, 0, 1/3, 0, 1/3, 0, 0, 0, 0], \
              [0, .5, 0, 0, 0, .5, 0, 0, 0], \
              [1/3, 0, 0, 0, 1/3, 0, 1/3, 0, 0], \
              [0, 1/4, 0, 1/4, 0, 1/4, 0, 1/4, 0], \
              [0, 0, 1/3, 0, 1/3, 0, 0, 0, 1/3], \
              [0, 0, 0, 0, 0, 0, 1, 0, 0], \
              [0, 0, 0, 0, 1/3, 0, 1/3, 0, 1/3], \
              [0, 0, 0, 0, 0, 0, 0, 0, 1]])
              
# define initial distribution
phi = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0])

# create Markov chain
markov_chain = sp.MarkovChain(P, phi)

# specify SampleEvolution parameters
samples                     = 2000
steps                       = 1000
states_in_recurrent_classes = [[6], [8]]

# instantiate solution; memory and tolerance are optional parameters
sample_evolution = sp.SampleEvolution(markov_chain, samples, steps, \
                                      states_in_recurrent_classes)
# run simulation
sample_evolution.run()

# sample_evolution now has data from the results of its simulation
average_distribution = sample_evolution.pi

# you can even plot absorption times
sample_evolution.plot_absorption()
