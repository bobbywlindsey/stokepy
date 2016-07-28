from .helpers import *

class MatrixMultiplicationEvolution:
    """
    parameters:
        markov_chain (numpy matrix)
        phi (numpy vector)                 = initial distribution
        steps (int)                        = number of steps to take
        rec_class_states (array of arrays) = recurrent classes
        memory (int)                       = how many steps to keep of the run
        tolerance (float)
    """

    def __init__(self, markov_chain, phi, steps, rec_class_states, memory = 10,\
                 tolerance = 0.001):
        """
        parameters:
            markov_chain = MarkovChain object
            phi (numpy array) = initial distribution vector
            steps (int) = number of steps
            rec_class_states (array) = recurrent classes in chain
            memory (int) = # of steps you want to remember in simulation
            tolerance (float)

        memory and tolerance are optional parameters

        returns MatrixMultiplicationEvolution object with metadata
        """

        self.P                           = markov_chain.P
        self.phi                         = phi
        self.num_steps                   = steps
        self.memory                      = memory
        self.num_states                  = phi.shape[0]
        self.states_in_recurrent_classes = rec_class_states
        self.tolerance                   = tolerance

        # place to store values returned from simulation
        self.tpdf = None
        # average distribution
        self.pi = None
        # absorption proportions for plotting
        self.absorption_proportions = None

        self.recurrent_class_absorbed_proportions = None
        self.mean_absorption_time = None

    def plot_absorption(self):
        plot_absorption_helper(self.absorption_proportions, self.tolerance)

        return None

    def run(self):
        """ Evolves the system via matrix multiplication """

        ### -------------- set stage for simulation -------------- ###
        # create theoretical probability distribution function
        tpdf    = np.zeros([self.memory, self.num_states], dtype = float)
        # initialize the tpdf by writing the initial distribution matrix to tpdf
        tpdf[0] = self.phi[:]
        ap = compute_absorbed_proportions(self.phi, \
                                          self.states_in_recurrent_classes)
        absorption_proportions = [ap]

        ### -------------- run the simulation -------------- ###
        step = 0
        while (step < self.num_steps) or (np.sum(ap) < 1 - self.tolerance):
            current_step       = step % self.memory
            next_step          = (step + 1) % self.memory
            tpdf[next_step, :] = tpdf[current_step, :].dot(self.P)

            ap = compute_absorbed_proportions(tpdf[next_step,:], \
                                              self.states_in_recurrent_classes)
            absorption_proportions.append(ap)
            step += 1

        # right now, the last distribution is not necessarily on the bottom
        # of the epdf matrix; so, the following code rearranges the rows of
        # the matrix to make sure the final distribution is on bottom
        tpdf = np.roll(tpdf, self.memory - next_step - 1, axis = 0)

        ### -------- set results -------- ###
        self.tpdf = tpdf
        self.pi   = np.mean(tpdf, 0)
        self.absorption_proportions = absorption_proportions
        self.recurrent_class_absorbed_proportions = absorption_proportions[-1]

        # get mean absorption time
        absorbed_marginal = get_newly_absorbed_proportions(\
                            self.absorption_proportions, self.tolerance)
        times = np.arange(absorbed_marginal.shape[0])
        self.mean_absorption_time = absorbed_marginal.dot(times)
        return None
