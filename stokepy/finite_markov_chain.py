from .headers import *
from .helpers import *

class FiniteMarkovChain:

    def __init__(self):
        self.P          = None
        self.p          = None
        self.q          = None
        self.num_states = None
        self.dim        = None
        self.phi        = None

    def gen_from_params(self, phi, p, num_states, dim):
        """
        parameters:
            phi (numpy array)   = initial distribution
            p (int)             = probability of moving forward to another state
            num_states (int) = # of states you have
            dim (int)           = dimension of the Markov chain

        returns P (the Markov chain)
        """

        q               = 1 - p
        self.p          = p
        self.q          = q
        self.num_states = num_states
        self.dim        = dim
        self.phi        = phi

        if dim == 1:
            P = np.zeros([num_states, num_states])
            for row in range(num_states):
                if row+1 != num_states-1:
                    P[row+1, row]   = q
                    P[row+1, row+2] = p
                else:
                    self.P = P
                    break
        else:
            raise ValueError('No support for {} dimensions'.format(self.dim))

    def apply_boundary_condition(self, condition):
        """
        parameters:
            condition (str): absorbing, reflecting, semi-reflecting

        applies boundary conditions to Markov chain
        """

        if self.dim == 1:
            if condition == 'absorbing':
                # create beginning boundary
                beg_boundary     = np.zeros(self.num_states)
                beg_boundary[0]  = 1
                # create end boundary
                end_boundary     = np.zeros(self.num_states)
                end_boundary[-1] = 1
                # apply boundaries to transition matrix
                self.P[0]  = beg_boundary
                self.P[-1] = end_boundary
            elif condition == 'reflecting':
                # create beginning boundary
                beg_boundary     = np.zeros(self.num_states)
                beg_boundary[1]  = 1
                # create end boundary
                end_boundary     = np.zeros(self.num_states)
                end_boundary[-2] = 1
                # apply boundaries to transition matrix
                self.P[0]  = beg_boundary
                self.P[-1] = end_boundary
            elif condition == 'semi-reflecting':
                # create beginning boundary
                beg_boundary     = np.zeros(self.num_states)
                beg_boundary[0]  = self.q
                beg_boundary[1]  = self.p
                # create end boundary
                end_boundary     = np.zeros(self.num_states)
                end_boundary[-1] = self.p
                end_boundary[-2] = self.q
                # apply boundaries to transition matrix
                self.P[0]  = beg_boundary
                self.P[-1] = end_boundary
            else:
                raise ValueError('{} is not a supported condition'.\
                                 format(condition))
        else:
            raise ValueError('Not yet support for {} dimensions'.\
                             format(self.dim))

        if not architecture_check_passed(self.P, self.phi):
            raise ValueError("P and phi dimensions don't match")
