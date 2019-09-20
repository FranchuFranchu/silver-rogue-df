from random import choice, randint
import random

from noise import snoise2
from game_classes import BaseMapTile, Map, Site, BaseEntity

def get_all_ndirections(direction):
	# Gets all possible (not diagonal) directions not equal to (direction)
	k = [2, 4, 6, 8]
	k.remove(direction)
	return k

class Town(Site):
	roads: list
	def __init__(self, entities = Map()):
		self.roads = [Road(entities)]
	def gen(self, entities = Map()):
		self.grow(entities)
		new_entities = Map()
		for road in self.roads:
			new_entities += road.gen(entities)
		return new_entities

	def grow(self, entities):
		pos = []
		for i in self.roads:
			if (i.x, i.y, i.bdirection) in pos:
				pos.remove((i.x, i.y, i.bdirection))
			elif (i.ex, i.ey, i.edirection) in pos:
				pos.remove((i.ex, i.ey, i.edirection))
			else:
				for d in get_all_ndirections(i.edirection):
					pos.append((i.ex, i.ey, d))
				for d in get_all_ndirections(i.bdirection):
					pos.append((i.x, i.y, d))
		where_to_grow = random.choice(pos)
		self.roads.append(Road.from_direction(entities, *where_to_grow))
class Road:
	x: int
	y: int
	# Length and width
	l: int
	w: int

	# Horizontal?
	h: bool 
	houses: list
	def __init__(self, entities, x = 10, y = 10, w = 3, l = 20, h = True):
		self.houses = []

		HOUSE_SIZE_AVG = 40 
		HOUSE_SIZE_STD = 4

		HOUSE_W_AVG = 6
		HOUSE_W_STD = 0.5


		HOUSE_SPACING = 3 # Spacing between house and house
		HOUSE_STREET_SPACING = 2 # Spacing between house and street (like a "frontyard")

		self.x = x
		self.y = y
		self.w = w
		self.l = l
		self.h = h

		new_entities = Map()
		posx = self.x
		posz = self.y
		sizeparallel = self.l      # Length of the street
		sizeperpendicular = self.w  # Width of the street
		horizontal = self.h

		# Negative side (8 if horizontal, 4 if vertical)
		occupied_tiles = 0
		print(posx, posz)
		while occupied_tiles < sizeparallel:
			house_size_parallel = int(random.gauss(HOUSE_W_AVG, HOUSE_W_STD))
			house_size_tiles = random.gauss(HOUSE_SIZE_AVG, HOUSE_SIZE_STD)
			house_size_perpendicular = int(house_size_tiles / house_size_parallel)
			occupied_tiles += house_size_parallel + HOUSE_SPACING # Add 2 so that there is space between the houses
			if horizontal:
				self.houses.append(House(
				 posx + occupied_tiles - 5,
				 posz - house_size_perpendicular - HOUSE_STREET_SPACING,
				 house_size_parallel,
				 house_size_perpendicular, door_direction = 2))
			else:
				self.houses.append(House(
				 posx - house_size_perpendicular - HOUSE_STREET_SPACING,
				 posz + occupied_tiles - 5,
				 house_size_perpendicular,
				 house_size_parallel, door_direction = 6))
		occupied_tiles = 0
		while occupied_tiles < sizeparallel:
			house_size_parallel = int(random.gauss(HOUSE_W_AVG, HOUSE_W_STD))
			house_size_tiles = random.gauss(HOUSE_SIZE_AVG, HOUSE_SIZE_STD)
			house_size_perpendicular = int(house_size_tiles / house_size_parallel)
			occupied_tiles += house_size_parallel + HOUSE_SPACING

		# Positive side
			if horizontal:
				self.houses.append(House(
				 posx + occupied_tiles - 5,
				 posz + HOUSE_STREET_SPACING + sizeperpendicular,
				 house_size_parallel,
				 house_size_perpendicular, door_direction = 8))
			else:
				self.houses.append(House(
				 posx + HOUSE_STREET_SPACING + sizeperpendicular,
				 posz + occupied_tiles - 5,
				 house_size_perpendicular,
				 house_size_parallel, door_direction = 4))
	

	def gen(self, entities):
		new_entities = Map()
		posx = self.x
		posz = self.y
		sizeparallel = self.l      # Length of the street
		sizeperpendicular = self.w  # Width of the street
		horizontal = self.h
		if horizontal:
			road_tiles = [posx, posz, posx + sizeparallel, posz + sizeperpendicular]	
		else:
			road_tiles = [posx, posz, posx + sizeperpendicular, posz + sizeparallel]

		for x in range(road_tiles[0],road_tiles[2]):
			for z in range(road_tiles[1],road_tiles[3]):
				new_entities.add(BaseMapTile('+', x, entities.yproject(x, z), z, attrs = {'road'}))

		# We'll have, on average, 6 tile wide houses
		# The size will have gaussian distibution (google it)

		# More compact and densely inhabitated towns should have thinner houses, but we'll do that later

		# +-------+
		# |       |
		# |       |
		# |       | 
		# +----=--+
		#
		# RRRRRRRRR
		# 
		# In this example:
			# Parallel house size is 8
			# Perpendicular is 4
			# Door direction is 2

		# Place houses alongside the road
		for i in self.houses:
			new_entities += i.gen(entities)
		return new_entities
	@property
	def horizontal(self):
		# Alias
		return self.h
	
	@property
	def ex(self):
		# End X
		r = self.x + self.l if self.horizontal else self.x
		return r
	
	@property
	def ey(self):
		# End Y
		r = self.y if self.horizontal else self.y + self.l
		return r
	
	@property
	def edirection(self):
		# Direction the road goes at the end
		return 4 if self.horizontal else 8
	@property
	def bdirection(self):
		# Direction the road goes at the beginning
		return 6 if self.horizontal else 2

	@staticmethod
	def from_direction(entities, sx, sy, direction, w = 3, l = 20):
		if direction == 2:
			l *= -1
			h = False
		elif direction == 4:
			l *= -1
			h = True
		elif direction == 6:
			l *= 1
			h = True
		elif direction == 8:
			l *= 1
			h = False

		return Road(entities, sx, sy, w, l, h)
class House:
	people: list # inhabitants of the house
	x: int
	y: int
	w: int
	h: int
	def __init__(self, x, z, w, h, door_direction = 2):
		self.x = x
		self.z = z
		self.w = w
		self.h = h
		self.door_direction = door_direction
	def gen(self, entities):
		x = self.x
		z = self.z
		w = self.w
		h = self.h
		door_direction = self.door_direction

		new_entities = Map()

		# The door will be in the lowest possible position in the house
		doorx, doorz = None, None
		doory = -100

		# Horizontal walls
		for i in range(x + 1, x + w - 1):
			if door_direction == 8:
				if doory < entities.yproject(i, z):
					doorx, doorz = i, z
					doory = entities.yproject(i, z)
			if door_direction == 2:
				if doory < entities.yproject(i, z + h):
					doorx, doorz = i, z + h
					doory = entities.yproject(i, z + h)

		# Vertical walls
		for i in range(z + 1, z + h - 1):
			if door_direction == 4:
				if doory < entities.yproject(x, i):
					doorx, doorz = x, i
					doory = entities.yproject(x, i)
			if door_direction == 6:
				if doory < entities.yproject(x + w, i):
					doorx, doorz = x + w, i
					doory = entities.yproject(x + w, i)

		y = doory	
		# Make the road

		for i in range(x + 1, x + w):
			for j in range(z + 1, z + h):
				new_entities.add(BaseMapTile('+', i, y, j, draw_index = -2))


		# Make the walls!
		for i in range(x + 1, x + w):
			new_entities.add(BaseMapTile(0xC4, i, y, z, draw_index = 2, passable = False))
			new_entities.add(BaseMapTile(0xC4, i, y, z + h, draw_index = 2, passable = False))

		for i in range(z + 1, z + h):
			new_entities.add(BaseMapTile(0xB3, x, y, i, draw_index = 2, passable = False))
			new_entities.add(BaseMapTile(0xB3, x + w, y, i, draw_index = 2, passable = False))

		# Person
		new_entities.add(BaseEntity('U', x + w // 2, y, z + h // 2, draw_index = 1000, desc = 'A human'))
		# Corners
		new_entities.add(BaseMapTile(0xBF, x + w, y,  z, draw_index = 2, passable = False))
		new_entities.add(BaseMapTile(0xC0, x, y, z + h, draw_index = 2, passable = False))
		new_entities.add(BaseMapTile(0xDA, x, y,  z, draw_index = 2, passable = False))
		new_entities.add(BaseMapTile(0xD9, x + w, y, z + h, draw_index = 2, passable = False))
		# We also need a door!
		new_entities.add(BaseMapTile('+', doorx, y, doorz, draw_index = -2))

		return new_entities

