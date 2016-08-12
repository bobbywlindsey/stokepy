# stokepy

Explore stochastic models through various methods of simulation and
mathematical theory.

## Install
```
$ pip install git+https://github.com/bobbywlindsey/stokepy
```

## Usage
```python
import stokepy as sp
import numpy as np
```
### Ways to Generate a Finite Markov chain

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

### Ways to Run a Finite Markov chain

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
import stokepy as sp

q                 = .9
samples           = 1000
# array of prob of producing 0 individuals, 1 individual, 2 individuals, etc...
probs             = [1-q, q/2, q/2]
colony_size_limit = 1000

bp = sp.BranchingProcess(samples, probs, colony_size_limit)
bp.run()

# print results
print('{} percent of colonies survived'.format(bp.percent_colonies_survived))
print('{} percent of colonies died'.format(bp.percent_colonies_died))
```

### Monte Carlo - Metropolis
In this example, we use the Metropolis algorithm to decode a cipher.
```python
import stokepy as sp
import numpy as np
import urllib.request
import unidecode


# instantiate class
steps         = 5000
samples       = 50
ciphered_text = '/ uc.azf-2ff"xu!tffzu.s"ffxf/d1x""tfd7 sk2f?7.f.7f/ uc!f/d1x""2"tzff/d1x""2"fx82f!2kup2"fy-up-fxcc7yf"702f1271c2f.7f!8uk2f,870ff17u5.fxff.7ff17u5.f/fk28df,x".fy-uc".f7.-28f1271c2f!x"-f,870f17u5.f/f.7f17u5.fxfk28df,x".tf1271c2ffcuku5?ffx.ff17u5.ffpiff/2u5?ffxff17u5.f!u82p.cdffu5ff/2.y225iffx82f7,.25f?uk25f.7fy75!28fy-x.s"f"7f?82x.fx/7 .f17u5.fxf.-x.f"7f0x5df1271c2f7,f17u5.f/fx82f"7fm225ff.7ff?2.f.-282iffx5!ffy-x.s"f"7f?82x.fx/7 .f17u5.f/f.-x.f"7f0x5df1271c2f7,f17u5.fxfx82f"7fm225f.7f?2.f.-282tf.-2dff7,.25ffyu"-ff.-x.ff1271c2fy7 c!ffv ".ff75p2fx5!f,78fxccfy78mf7 .fy-282f.-2f-2ccf.-2dfyx5.2!f.7f/2tff08f187""28fyx5.2!f.7f/2fx.f17u5.f!tf17u5.f!ffyx"5s.ffx5dy-282ffu5f1x8.up cx8ifu.fyx"fv ".fx5dfp75k25u25.f17u5.fxfk28dfc75?fyxdf,870f17u5."fxif/fx5!fptf-2fy7 c!f-xk2fxf5up2fcu..c2fp7..x?2ffx.ff17u5.f!iffyu.-ffxe2"f7k28f.-2f!778ifx5!f"125!fxf1c2x"x5.fx07 5.f7,f.u02fx.f17u5.f2ify-up-fy7 c!f/2f.-2f52x82".f1 /f.7f17u5.f!tff-u"ffyu,2f7,ffp7 8"2ffyx5.2!ffpcu0/u5?f87"2"if/ .f-2fyx5.2!fxe2"tf-2f!u!5s.fm57yfy-df;f-2ffv ".ffcum2!ffxe2"tff-2ff,c "-2!ff-7.cdff 5!28ff.-2f!28u"uk2f?8u5"f7,f.-2f/ cc!7:28f!8uk28"tff-2f"-u,.2!f-u"fy2u?-.f,870f,77.ff.7ff,77.iff/ .ffu.ffyx"ff2( xccdf 5p70,78.x/c2ff75ff2xp-tff7/ku7 "cdf"702/7!df-x!f/225fx11xccu5?cdfu5p7012.25.fx5!f-2f-712!f.7f?7!fu.fyx"5s.f-u0tff08f187""28f"xu!9fzd7 fy282f( u.2f25.u.c2!f.7f0xm2fx5df" ??2".u75"f78f187.2"."fx.f.-2fx118718ux.2f.u02fd7 fm57ytzffzx118718ux.2f.u02azf-77.2!fx8.- 8tfzx118718ux.2f.u02af.-2f,u8".fufm52yffx/7 .fu.fyx"fy-25fxfy78m0x5fx88uk2!fx.f0df-702fd2".28!xdtfufx"m2!f-u0fu,f-2s!fp702f.7fpc2x5f.-2fyu5!7y"fx5!f-2f"xu!ff57ff-2s!fp702ff.7ff!207cu"-ff.-2f-7 "2tf-2f!u!5s.f.2ccf02f".8xu?-.fxyxdf7,fp7 8"2tf7-f57tf,u8".f-2fyu12!fxfp7 1c2f7,fyu5!7y"fx5!fp-x8?2!ff02fxf,uk28tf.-25f-2f.7c!f02tzffz/ .f08f!25.if.-2f1cx5"f-xk2f/225fxkxucx/c2fu5f.-2fc7pxcf1cx55u5?f7,,up2f,78f.-2fcx".f5u52f075.-tzffz7-fd2"ify2ccfx"f"775fx"fuf-2x8!fufy25.ff".8xu?-.ff87 5!ff.7ff"22f.-20iffd2".28!xdffx,.285775tffd7 f-x!5s.f2exp.cdf?752f7 .f7,fd7 8fyxdf.7fp'
metro = sp.Metropolis(steps, samples, ciphered_text)

# get corpus about a bad-ass detective
url                    = 'https://www.gutenberg.org/cache/epub/1661/pg1661.txt'
adv_of_sherlock_holmes = urllib.request.urlopen(url)
corpus                 = adv_of_sherlock_holmes.read()
corpus                 = corpus.decode("utf-8") + '/'
# remove unicode accents
corpus                 = unidecode.unidecode(corpus)

# decide which characters you don't want in corpus
chars_to_remove = ['[', ']', '\n', '\r', '$', '#', '%', '*', '@', \
                   '&', '+', '<', '>', '=', '_', '{', '}', '|']
# clean the corpus
ts = sp.TextStats(corpus)
ts.clean_corpus(chars_to_remove)
ts.set_corpus_frequencies(ngram = 2, groupby='chars', log=True)

# set target plausibility then run the Markov chain
metro.set_target_plausibility(ts.corpus, ts.corpus_len, ts.unique_symbols, \
                              ts.ngram, ts.M)
metro.run()

# print results
print(metro.deciphered_text)
```
