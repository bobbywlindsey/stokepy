from .headers import *
from .helpers import *

class Metropolis:

    def __init__(self):
        self.current_state = None

    def run(self, co_domain):
        self.co_domain = co_domain
        # number of neighbors
        self.d = sym.binomial(len(self.co_domain), 2)
        self.J_unif_prob = 1/self.d

        # generate neighbors
        neighbors = self.generate_neighbors()
        # pick neighbor
        chosen_neighbor = neighbors[self.pick_neighbor()]
        print(chosen_neighbor)

    def plausibility(self):
        pass

    def clean_corpus(self, corpus, remove_chars, groupby = 'words'):
        # clean corpus
        corpus = corpus.lower()
        corpus = ''.join(str(ch) for ch in corpus if ch not in remove_chars)

        if groupby == 'words':
            corpus = corpus.split(' ')
        elif groupby == 'chars':
            corpus = list(corpus)
        else:
            raise ValueError('{} is not supported'.format(groupby))
        return corpus

    def get_corpus_frequencies(self, corpus, ngram):
        symbols = sorted(list(set(corpus)))
        print(symbols)
        corpus_numeric = text_to_numeric(symbols, corpus)
        print(corpus_numeric[0:500])

        # # create ngram tuples
        # ngram_tuples = zip(*[corpus[i:] for i in range(ngram)])
        #
        # # create frequency matrix
        # ngram_tuples_list = [gram for index, gram in enumerate(ngram_tuples)]
        # ngram_frequencies = [ngram_tuples_list.count(gram)\
        #                      for gram in ngram_tuples_list]
        # ngram_beg_freq = {}
        # for ngram in ngram_tuples_list:
        #     if ngram_beg_freq.get(ngram[0]):
        #         ngram_beg_freq[ngram[0]] += 1
        #     else:
        #         ngram_beg_freq[ngram[0]] = 1
        #
        # ngram_frequencies = dict(zip(ngram_tuples_list, ngram_frequencies))
        # ngram_probabilities = ngram_frequencies.copy()
        # for ngram, frequency in ngram_probabilities.items():
        #     ngram_probabilities[ngram] = frequency/ngram_beg_freq.get(ngram[0])
        # return ngram_probabilities

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
