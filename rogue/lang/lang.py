import random

import yaml

from phonetics import Phoneme

IPA_SIZE = (11, 5)
class Language:
	def __init__(self):
		self.generate_phonology()
		self.generate_phonotactics()
		self.generate_morphology()
		self.generate_grammar()
		self.generate_starting_vocabulary()

	def add_phoneme_recurse(self, consonants):
		# If the phoneme is valid, get a phoneme in the same row as the previous one, or the voicedness alternative
		if len(consonants) > 20:
			return consonants
		prev = consonants[-1]
		chance = random.random() * 100
		if phoneme.char in (None, 'Invalid'):
			continue
		while 1:
			consonants.append(phoneme)

	def generate_phonology(self):
		consonants = []
		while len(consonants) < 20:
			phoneme = Phoneme(
				random.randint(0, IPA_SIZE[1] - 1),
				random.randint(0, IPA_SIZE[0] - 1),
				random.randint(0, 1),
				0
				)
		print(consonants)
	def generate_phonotactics(self):
		pass

	def generate_morphology(self):
		pass

	def generate_grammar(self):
		pass

	def generate_starting_vocabulary(self):
		pass

Language()