import numpy as np
import matplotlib.pyplot as plt

class BranchingProcess:
	"""
	parameters:
		samples (int) = number of samples
		probs (array) = P(1 individual), P(2 individuals), etc... all sum to 1
		colony_size_limit (int) = stopping point for colony growth

	attributes:
		percent_colonies_survived
		percent_colonies_died
	"""

	def __init__(self, samples, probs, colony_size_limit):
		self.samples                   = samples
		self.probs                     = probs
		self.colony_size_limit         = colony_size_limit

		self.percent_colonies_survived = None
		self.percent_colonies_died     = None

	def run(self):

		samples_survived = 0
		samples_died = 0

		for sample in range(self.samples):
			# start colony with 1 individual
			X = 1
			# set limit on how big a colony can grow
			while X < self.colony_size_limit:
				for i in range(X):
					r = np.random.rand()
					for idx, value in enumerate(self.probs):
						# special range for producing 0 individuals
						if idx == 0 and r >= 0 and r < self.probs[idx]:
							X -= 1
							break
						# special range for producing 1 individuals
						elif idx == 1 and r > self.probs[0] and \
									  r < 1 - self.probs[idx]:
							X += 0
							break
						# special range for last element in array
						elif idx == len(self.probs) - 1 and \
									r > 1 - self.probs[idx] and \
									r < 1:
							X += idx - 1
							break
						# general case
						elif idx in list(range(1, len(self.probs))) and \
									r > 1 - self.probs[idx - 1] and \
									r < 1 - self.probs[idx]:
							X += idx - 1
							break

				# if at any time X = 0, the population will never recover
				if X <= 0:
					samples_died += 1
					break

			if X > 0:
				samples_survived += 1

		self.percent_colonies_survived = (samples_survived/self.samples)*100
		self.percent_colonies_died = (samples_died/self.samples)*100

		return None
