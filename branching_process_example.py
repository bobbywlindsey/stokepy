import stokepy as sp

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
