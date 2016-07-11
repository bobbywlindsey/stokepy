import stokepy as sp
import numpy as np


# instantiate class
mc = sp.MarkovChain()

# generate Markov chain with no boundary conditions
mc.gen_from_params(p = 0.6, num_of_states = 5, dim = 2)

# apply boundary condition: absorbing, reflecting, semi-reflecting
# only works for 1 dimension Markov chains at the moment
mc.apply_boundary_condition(condition='semi-reflecting')

#create nxn transition matrix
P = np.array([[0, .5, 0, .5, 0, 0, 0, 0, 0], \
              [1/3, 0, 1/3, 0, 1/3, 0, 0, 0, 0], \
              [0, .5, 0, 0, 0, .5, 0, 0, 0], \
              [1/3, 0, 0, 0, 1/3, 0, 1/3, 0, 0], \
              [0, 1/4, 0, 1/4, 0, 1/4, 0, 1/4, 0], \
              [0, 0, 1/3, 0, 1/3, 0, 0, 0, 1/3], \
              [0, 0, 0, 0, 0, 0, 1, 0, 0], \
              [0, 0, 0, 0, 1/3, 0, 1/3, 0, 1/3], \
              [0, 0, 0, 0, 0, 0, 0, 0, 1]])

# create initial distribution vector
phi = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0])

# create Markov chain object
markov_chain = sp.MarkovChain(P, phi)

# choose solution method like Sample Evolution
sample_evolution = sp.SampleEvolution(markov_chain, samples, steps, states_in_recurrent_classes)

# run the solution
sample_evolution.run()

# get data from the run
average_distribution   = sample_evolution.pi
epdf                   = sample_evolution.epdf
absorption_proportions = sample_evolution.absorption_proportions
apbrc                  = sample_evolution.recurrent_class_absorbed_proportions
mean_absorption_time   = sample_evolution.mean_absorption_time
