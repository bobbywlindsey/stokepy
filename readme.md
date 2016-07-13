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
mc = np.array([[0, .5, 0, .5, 0, 0, 0, 0, 0], \
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
mc = sp.MarkovChain()

# create initial distribution vector
phi = np.array([0, 0, 1, 0, 0])

# generate Markov chain with no boundary conditions
mc.gen_from_params(phi, p = 0.6, num_of_states = 5, dim = 2)

# apply boundary condition: absorbing, reflecting, semi-reflecting
# only works for 1 dimension Markov chains at the moment
mc.apply_boundary_condition(condition='semi-reflecting')
```

### Ways to Run the Markov chain

Evolution via Samples
```python

# choose solution method like Sample Evolution
sample_evolution = sp.SampleEvolution(mc, phi, samples = 2000, steps = 2000,\
                                      rec_class_states = [])

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
