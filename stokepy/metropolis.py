from .helpers import *

class Metropolis:
	"""
	parameters:
		num_steps (int) = number of steps to take
		num_samples (int) = number of samples
		ciphered_text (str) = ciphered text you want to decipher
	"""

	def __init__(self, num_steps, num_samples, ciphered_text):
		self.num_steps           = num_steps
		self.num_samples         = num_samples
		self.ciphered_text       = ciphered_text
		self.ciphered_text_len   = len(self.ciphered_text)

		self.unique_symbols      = None
		self.ciphered_numeric    = None
		self.num_unique_symbols  = None
		self.target_plausibility = None

		self.ngram               = None
		self.M                   = None

		self.deciphered_text     = None

	def set_target_plausibility(self, corpus, corpus_len, unique_symbols, \
								ngram, M):
		"""
		parameters:
			all are taken from the TextStats class
		"""

		self.unique_symbols     = unique_symbols
		self.num_unique_symbols = len(self.unique_symbols)
		self.ngram              = ngram
		self.M                  = M
		# set target plausibility
		start = np.random.randint(corpus_len - self.ciphered_text_len)
		target_text = corpus[start : start + self.ciphered_text_len]
		target_numeric = text_to_numeric(self.unique_symbols, target_text)
		self.target_plausibility = self.log_plausibility(target_numeric)

		return None

	def run(self):
		self.ciphered_numeric = text_to_numeric(self.unique_symbols,\
												self.ciphered_text)
		# randomly choose initial states for each sample
		deciphers = [np.random.permutation(self.num_unique_symbols) \
					 for sample in range(self.num_samples)]
		# calculate plausibility for initial states
		current_plausibilities = [self.log_plausibility(apply_cipher(decipher,\
								  self.ciphered_numeric)) \
								  for decipher in deciphers]
		plausibility_hist = np.zeros([self.num_steps, self.num_samples])

		for step in range(self.num_steps):
			for sample in range(self.num_samples):
				evolution_results             = self.evolve(deciphers[sample],\
												current_plausibilities[sample])
				deciphers[sample]               = evolution_results[0]
				current_plausibilities[sample]  = evolution_results[1]
				plausibility_hist[step, sample] = current_plausibilities[sample]

			# get greatest plausibility
			index = np.argmax(current_plausibilities)
			max_plausibility = current_plausibilities[index]

			if np.exp(max_plausibility - self.target_plausibility) > 0.999:
				break

		print("Best sample is number {}.\n".format(index))
		plausibility_hist = plausibility_hist[:step, :]

		self.decipher_text(deciphers[index], self.ciphered_numeric)

		return None

	def log_plausibility(self, message_numeric):
		plausibility = 0
		for i in range(self.ciphered_text_len - self.ngram + 1):
			# sum because we took log of M to avoid roundoff errors
			plausibility += self.M[message_numeric[i: i + self.ngram]]
		return plausibility

	def evolve(self, decipher, current_plausibility):
		# randomly choose neighbor from (num_unique_symbols choose 2) neighbors
		i, j = np.random.randint(self.num_unique_symbols, size = 2)
		# make a transposition
		decipher[i], decipher[j] = decipher[j], decipher[i]

		proposed_deciphered_numeric = apply_cipher(decipher, \
												   self.ciphered_numeric)
		proposed_plaus = self.log_plausibility(proposed_deciphered_numeric)
		plausibility_diff = proposed_plaus - current_plausibility
		if plausibility_diff > 0:
			# move to neighbor
			current_plausibility = proposed_plaus
		else:
			acceptance_ratio = np.e**plausibility_diff
			r = np.random.rand()
			if r <= acceptance_ratio:
				# move to neighbor
				current_plausibility = proposed_plaus
			else:
				# stay; so we need to unflip transposition
				decipher[i], decipher[j] = decipher[j], decipher[i]

		return decipher, current_plausibility

	def decipher_text(self, best_cipher, ciphered_numeric):
		deciphered_numeric   = apply_cipher(best_cipher, ciphered_numeric)
		deciphered_text      = numeric_to_text(self.unique_symbols, \
											   deciphered_numeric)
		self.deciphered_text = deciphered_text

		return None
