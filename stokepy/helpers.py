from .headers import *

def architecture_check_passed(P, phi):
    """
    Make sure columns of the transition matrix, P, (which represent the
    number of states) match the number of elements in the initial distribution,
    phi, which represents the starting point in each state
    """
    num_of_states = P.shape[0]
    if phi.shape[0] != num_of_states:
        #print("Transition matrix and initial distribution dimensions don't match")
        return False

    row_sums  = np.sum(P, 1)
    should_be = np.ones_like(row_sums)
    if np.allclose(row_sums, should_be) == False:
        #print('Rows of transition matrix do not all sum to 1')
        return False
    return True

def compute_absorbed_proportions(vector, states_in_recurrent_classes = []):
    """ return numpy array of absorbed proportions for each recurrent state """
    if states_in_recurrent_classes == []:
        ap = [1.0]
    else:
        ap = [np.sum(vector[states]) for states in states_in_recurrent_classes]
    return np.array(ap)

def support(vector):
    """ return nonzero entries of a vector """
    return np.nonzero(vector)[0]

def normalize_vector(vector):
    """ normalize vector given hard-coded tolerance level """
    tolerance = 0.001
    sigma = np.sum(vector)
    if np.abs(sigma) < tolerance:
        # if row sums to 0, divide by leftmost nonzero entry
        sigma = vector[support(vector)][0]
    return vector/sigma

def normalize_rows(transition_matrix):
    return np.apply_along_axis(normalize_vector, 1, transition_matrix)

def get_newly_absorbed_proportions(absorption_proportions, tolerance):
    absorption_proportions = np.array(absorption_proportions)
    # total absorbed by all recurrent classes
    absorbed_cumulative = np.sum(absorption_proportions, axis = 1)
    # remove tail, if simulation continued to run after complete absorption
    absorbed_cumulative = absorbed_cumulative[absorbed_cumulative < 1-tolerance]
    # append 1.0 to end
    absorbed_cumulative = np.append(absorbed_cumulative, 1.0)
    # find "newly" absorbed proportion at each step
    absorbed_marginal = np.diff(absorbed_cumulative)
    # np.diff shrinks array by 1 entry so prepend 0.0
    absorbed_marginal = np.insert(absorbed_marginal, 0, absorbed_cumulative[0])
    return absorbed_marginal

def plot_absorption_helper(absorption_proportions, tolerance):
    absorbed_marginal = get_newly_absorbed_proportions(absorption_proportions, \
                        tolerance)
    times = np.arange(absorbed_marginal.shape[0])
    plt.bar(times, absorbed_marginal)
    plt.xlabel('jumps')
    plt.ylabel('proportion')
    plt.title('Distribution of Absorption Times')
    plt.show()
    return None
