import stokepy as sp
import numpy as np

# instantiate class
mc = sp.MarkovChain()

# create initial distribution vector
phi = np.array([0, 0, 1, 0, 0])

# generate Markov chain with no boundary conditions
mc.gen_from_params(phi, p = 0.6, num_of_states = 5, dim = 1)

# apply boundary condition: absorbing, reflecting, semi-reflecting
# only works for 1 dimension Markov chains at the moment
mc.apply_boundary_condition(condition='absorbing')

# choose solution method like Matrix Multiplication Evolution
matrx_mult_evo = sp.MatrixMultiplicationEvolution(mc, phi, steps = 2000,\
                                      rec_class_states = [])
# run the solution
matrx_mult_evo.run()

# get data from the run
average_distribution   = matrx_mult_evo.pi
tpdf                   = matrx_mult_evo.tpdf
absorption_proportions = matrx_mult_evo.absorption_proportions
apbrc                  = matrx_mult_evo.recurrent_class_absorbed_proportions
mean_absorption_time   = matrx_mult_evo.mean_absorption_time

# plot absorption tiems for recurrent classes
matrx_mult_evo.plot_absorption()
