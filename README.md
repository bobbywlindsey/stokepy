# stokepy

Explore stochastic models through various methods of simulation and
mathematical theory.

## Install
```
$ pip install [something here]
```

## Usage
```python
import stokepy as sp
import numpy as np
```
### Ways to Generate a Markov chain

Manually:
```python
# create nxn Markov chain
fmc = np.array([[0, .5, 0, .5, 0, 0, 0, 0, 0], \
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
```
By Parameters:
```python
# instantiate class
fmc = sp.FiniteMarkovChain()

# create initial distribution vector
phi = np.array([0, 0, 1, 0, 0])

# generate Markov chain with no boundary conditions
fmc.gen_from_params(phi, p = 0.6, num_of_states = 5, dim = 2)

# apply boundary condition: absorbing, reflecting, semi-reflecting
# only works for 1 dimension Markov chains at the moment
fmc.apply_boundary_condition(condition='semi-reflecting')
```

### Ways to Run the Markov chain

Evolution via Samples
```python

# choose solution method like Sample Evolution
sample_evolution = sp.SampleEvolution(fmc, phi, samples = 2000, steps = 2000,\
                                      rec_class_states)

# run the solution
sample_evolution.run()

# get data from the run
average_distribution   = sample_evolution.pi
epdf                   = sample_evolution.epdf
absorption_proportions = sample_evolution.absorption_proportions
apbrc                  = sample_evolution.recurrent_class_absorbed_proportions
mean_absorption_time   = sample_evolution.mean_absorption_time

# plot absorption times for recurrent classes
sample_evolution.plot_absorption()
```
Evolution via Matrix Multiplication
```python

# choose solution method like Matrix Multiplication Evolution
matrx_mult_evo = sp.MatrixMultiplicationEvolution(fmc, phi, steps = 2000,\
                                      rec_class_states = [])
# run the solution
matrx_mult_evo.run()

# get data from the run
average_distribution   = matrx_mult_evo.pi
tpdf                   = matrx_mult_evo.tpdf
absorption_proportions = matrx_mult_evo.absorption_proportions
apbrc                  = matrx_mult_evo.recurrent_class_absorbed_proportions
mean_absorption_time   = matrx_mult_evo.mean_absorption_time

# plot absorption times for recurrent classes
matrx_mult_evo.plot_absorption()
```

### Galton's Branching Process Markov chain
```python
q                 = .9
samples           = 1000
# array of prob of producing 0 individuals, 1 individual, 2 individuals, etc...
probs        = [1-q, q/2, q/2]
colony_size_limit = 1000

bp = sp.BranchingProcess(samples, probs, colony_size_limit)
bp.run()

# print results
print('{} percent of colonies survived'.format(bp.percent_colonies_survived))
print('{} percent of colonies died'.format(bp.percent_colonies_died))
```
