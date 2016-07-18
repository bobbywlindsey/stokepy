from .headers import *
from .helpers import *

class MarkovChain:
    """
    parameters:
        P   = transition matrix
        phi = initial distribution

    returns a MarkovChain object
    """

    def __init__(self):
        self.P             = None
        self.p             = None
        self.q             = None
        self.num_of_states = None
        self.dim           = None
        self.phi           = None

    def gen_from_params(self, phi, p, num_of_states, dim):
        """
        parameters:
            p (int)             = probability of moving forward to another state
            num_of_states (int) = # of states you have
            dim (int)           = dimension of the Markov chain
            phi (numpy array)   = initial distribution

        returns P (the Markov chain)
        """

        q                  = 1 - p
        self.p             = p
        self.q             = q
        self.num_of_states = num_of_states
        self.dim           = dim
        self.phi           = phi

        if dim == 1:
            P = np.zeros([num_of_states, num_of_states])
            for row in range(num_of_states):
                if row+1 != num_of_states-1:
                    P[row+1, row]   = q
                    P[row+1, row+2] = p
                else:
                    self.P = P
                    break
        else:
            raise ValueError('Not yet support for {} dimensions'.format(self.dim))

    def gen_from_data(self, corpus, ngram, groupby = 'words'):
        """
        parameters:
            corpus (str) = text to train model
            ngram (int) = preferred number of chars or words in each state
            groupby (opt) = 'chars' or 'words'; defaulted to 'words'

        return P (the Markov chain)
        """
        # clean text
        corpus = corpus.lower()
        exclude = set(string.punctuation)
        corpus = ''.join(str(ch) for ch in corpus if ch not in exclude)

        if groupby == 'words':
            corpus = corpus.split(' ')
        elif groupby == 'chars':
            # remove carriage returns and spaces
            corpus = list(corpus)
            for index, char in enumerate(corpus):
                if char == '\n':
                    corpus[index] = ''
                if char == ' ':
                    corpus[index] = ''
            # remove all ''
            indexes = [i for i, char in enumerate(corpus) if char == '']
            offset = 0
            for index in indexes:
                del corpus[index - offset]
                offset += 1
        else:
            raise ValueError('{} is not supported'.format(groupby))

        # create ngram tuples
        ngram_tuples = zip(*[corpus[i:] for i in range(ngram)])

        # create frequency matrix
        ngram_tuples_list = [gram for index, gram in enumerate(ngram_tuples)]
        ngram_frequencies = [ngram_tuples_list.count(gram)\
                             for gram in ngram_tuples_list]
        ngram_beg_freq = {}
        for ngram in ngram_tuples_list:
            if ngram_beg_freq.get(ngram[0]):
                ngram_beg_freq[ngram[0]] += 1
            else:
                ngram_beg_freq[ngram[0]] = 1

        ngram_frequencies = dict(zip(ngram_tuples_list, ngram_frequencies))
        ngram_probabilities = ngram_frequencies.copy()
        for ngram, frequency in ngram_probabilities.items():
            ngram_probabilities[ngram] = frequency/ngram_beg_freq.get(ngram[0])
        return ngram_probabilities

    def apply_boundary_condition(self, condition):
        """
        parameters:
            condition (str): absorbing, reflecting, semi-reflecting

        applies boundary conditions to Markov chain
        """

        if self.dim == 1:
            if condition == 'absorbing':
                # create beginning boundary
                beg_boundary     = np.zeros(self.num_of_states)
                beg_boundary[0]  = 1
                # create end boundary
                end_boundary     = np.zeros(self.num_of_states)
                end_boundary[-1] = 1
                # apply boundaries to transition matrix
                self.P[0]  = beg_boundary
                self.P[-1] = end_boundary
            elif condition == 'reflecting':
                # create beginning boundary
                beg_boundary     = np.zeros(self.num_of_states)
                beg_boundary[1]  = 1
                # create end boundary
                end_boundary     = np.zeros(self.num_of_states)
                end_boundary[-2] = 1
                # apply boundaries to transition matrix
                self.P[0]  = beg_boundary
                self.P[-1] = end_boundary
            elif condition == 'semi-reflecting':
                # create beginning boundary
                beg_boundary     = np.zeros(self.num_of_states)
                beg_boundary[0]  = self.q
                beg_boundary[1]  = self.p
                # create end boundary
                end_boundary     = np.zeros(self.num_of_states)
                end_boundary[-1] = self.p
                end_boundary[-2] = self.q
                # apply boundaries to transition matrix
                self.P[0]  = beg_boundary
                self.P[-1] = end_boundary
            else:
                raise ValueError('{} is not a supported condition'.format(condition))
        else:
            raise ValueError('Not yet support for {} dimensions'.format(self.dim))

        if not architecture_check_passed(self.P, self.phi):
            raise ValueError("P and phi dimensions don't match")
