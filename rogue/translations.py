# This might be reinventing the wheel
# I don't care

from yaml import load

class TranslationFeature:
	def _(self, name):
		curr = self.curr_locales
		for i in name.split('.'):
			try:
				curr = curr[i]
			except KeyError:
				return i
		return curr
	def multiple_translations(self, *names):
		# Useful if you quickly want a list of translations
		return [self._(i) for i in names]

	def multiple_translations_in(self, where, *names):
		# Gets many translations in a single translation scope, i.e. "talk"
		return [
		self._(where + '.' + i) for i in names
		]
	def load_locales(self, lang):
		with open(f'../locale/{lang}.yml') as f:
			self.curr_locales = load(f)
