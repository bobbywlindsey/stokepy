class MarkovChain:
    """
    Creates Markov Chain object

    *TODO
    - add function to apply boundary conditions
    - add function to auto-generate P
    """

    def __init__(self, P, phi):
        """
        P = transition matrix
        phi = initial distribution
        """

        self.P   = P
        self.phi = phi
