from .headers import *

class MarkovChain:
    """
    Creates Markov Chain object

    *TODO
    - add function to apply boundary conditions
    - add function to auto-generate P
    """

    def __init__(self):
        """
        P = transition matrix
        phi = initial distribution
        """

        self.P             = None
        self.p             = None
        self.q             = None
        self.num_of_states = None
        self.dim           = None

    def gen_from_params(self, p, num_of_states, dim):
        """
        p = probability of moving forward to another state
        dim = dimension of the Markov chain

        returns transition matrix, P
        """
        q                  = 1 - p
        self.p             = p
        self.q             = q
        self.num_of_states = num_of_states
        self.dim           = dim
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

    def apply_boundary_condition(self, condition):
        if dim == 1:
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
