from .helpers import *

class TextStats:
	"""
	Assorted statistical functions on a corpus

	parameters:
		corpus (str) = a reference text
	"""

	def __init__(self, corpus):
		self.corpus             = corpus
		self.unique_symbols     = None
		self.unique_words       = None
		self.ciphered_numeric   = None
		self.num_unique_symbols = None
		self.num_unique_words   = None
		self.corpus_len         = None
		self.ngram              = None

	def clean_corpus(self, remove_chars):
		"""
		parameters:
			remove_chars (array) = characters you want to be removed from corpus
		"""

		# clean corpus
		self.corpus = self.corpus.lower()
		self.corpus = ''.join(str(ch) if ch not in remove_chars else ' ' \
							  for ch in self.corpus)
		corpus_len  = len(self.corpus)

		self.corpus_len         = corpus_len
		# get unique symbols in corpus
		unique_symbols          = sorted(list(set(self.corpus)))
		unique_words            = sorted(list(set(self.corpus.split())))
		self.unique_words       = unique_words
		self.num_unique_words   = len(unique_words)
		self.unique_symbols     = unique_symbols
		num_unique_symbols      = len(unique_symbols)
		self.num_unique_symbols = num_unique_symbols


		self.corpus_numeric = None
		self.ngram = None

		return None

	def set_corpus_frequencies(self, ngram, groupby = 'words', log = False):
		"""
		parameters:
			ngram (int)
			groupby (str) = options: 'chars', 'words'; default is 'words'
			log (bool) = values of frequency 'matrix'
		"""

		if groupby == 'words':
			self.corpus = self.corpus.split(' ')
			# remove all ''
			indexes = [i for i, word in enumerate(self.corpus) if word == '']
			offset = 0
			for index in indexes:
				del self.corpus[index-offset]
				offset+=1
		elif groupby == 'chars':
			self.corpus = list(self.corpus)
		else:
			raise ValueError('{} is not supported'.format(groupby))

		if groupby == 'chars':
			corpus_numeric = text_to_numeric(self.unique_symbols, self.corpus)
			dimensions = np.repeat(self.num_unique_symbols, ngram)
		else:
			corpus_numeric = text_to_numeric(self.unique_words, self.corpus)
			dimensions = np.repeat(self.num_unique_words, ngram)

		if log:
			# initialize M with 1s because log function doesn't like 0s
			M = np.ones(dimensions, int)
		else:
			M = np.zeros(dimensions, int)
		# count frequencies
		for i in range(self.corpus_len - ngram + 1):
			M[corpus_numeric[i:i + ngram]] += 1
		# normalize last dimension
		M = np.apply_along_axis(normalize_vector, -1, M)
		if log:
			# log all frequencies to avoid floating point error
			M = np.log(M)
		self.M = M

		return None
