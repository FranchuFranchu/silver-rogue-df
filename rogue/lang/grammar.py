from typing import List, Dict

from phonetics import Phoneme

class Modifier:
	sentence = False
	word: str
	def __init__(self, word):
		self.word = word
	def get_english(self, wordict):
		return wordict[self.word].get('en') or self.word

class NounClause:
	main: str # or NounClause
	modifiers: List[Modifier]
	def __init__(self, main, modifiers):
		self.main = main
		self.modifiers = modifiers

	def get_english(self, wordict):

		if isinstance(self.main, str):
			s = self.main
		else:
			s = self.main.get_english(w)

		for i in self.modifiers:
			s = i.get_english(wordict) + ' ' + s
		return s

class Phrase:
	def __init__(self, verb: str, arguments: Dict[str, NounClause], tense: str = 'past'):
		self.verb = verb
		self.arguments = arguments
		self.tense = tense
	def get_english(self, wordict):
		conjugator = mlconjug.Conjugator(language='en')
		s = list(conjugator.conjugate(self.verb).conjug_info['indicative']['indicative ' + self.tense].values())[0]
		for k, v in self.arguments.items():
			if k == 'nominative':
				s = v.get_english(wordict) + ' ' + s
			elif k == 'accusative':
				s = s + ' ' + v.get_english(wordict)
		return s
