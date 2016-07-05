# stokepy

Explore your stochastic models through various methods of simulation and
mathematical theory.

## Install
```
$ pip install [something here]
```

## Usage
```python
import stokepy as sp
import numpy as np

# create nxn transition matrix
P = np.array([[0, .5, 0, .5, 0, 0, 0, 0, 0], [1/3, 0, 1/3, 0, 1/3, 0, 0, 0, 0], [0, .5, 0, 0, 0, .5, 0, 0, 0], \
              [1/3, 0, 0, 0, 1/3, 0, 1/3, 0, 0], [0, 1/4, 0, 1/4, 0, 1/4, 0, 1/4, 0], [0, 0, 1/3, 0, 1/3, 0, 0, 0, 1/3], \
              [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1/3, 0, 1/3, 0, 1/3], [0, 0, 0, 0, 0, 0, 0, 0, 1]])

# create initial distribution vector
phi = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0])

# create Markov chain object
markov_chain = sp.MarkovChain(P, phi)

# choose solution method like Sample Evolution
sample_evolution = sp.SampleEvolution(markov_chain, samples, steps, states_in_recurrent_classes)

# run the solution
sample_evolution.run()

# get data from the run
average_distribution = sample_evolution.pi
# empirical probability distribution function
epdf = sample_evolution.epdf

absorption_proportions = sample_evolution.absorption_proportions
# absorbed proportions by recurrent class
apbrc = sample_evolution.absorbed_proportions_by_recurrent_class
mean_absorption_time = sample_evolution.mean_absorption_time

# plot absorption times for recurrent classes
sample_evolution.plot_absorption()
```
