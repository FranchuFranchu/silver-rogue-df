from collections import namedtuple

from bidict import bidict

class Position(namedtuple('Position', 'xyz')):
	pass

class Entity:
	pass

class Map:

	def __init__(self):
		# Position -> Entity
		self._internal = bidict()

	def add(self, position: Position, entity: Entity, check_empty=False):
		if check_empty and position in self._internal:
			raise ValueError()

		current = self._internal.get(position)
		self._internal[position] = entity
		return current

	def clear(self, position: Position):
		del self._internal[position]

	def at(self, position: Position) -> Entity
		return self._internal[position]

	def find(self, entity: Entity) -> Position
		return self._internal.inverse.get(entity, None)

