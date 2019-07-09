from noise import snoise2
from game_classes import BaseEntity, Map
from random import choice

def main(entities):
	new_entities = Map()
	# Make a "main street"
	# horizontal = true, vertical = false
	sx = 10
	sz = 10
	horizontal = choice([True, False])

	if horizontal:
		road_tiles = [sx, sz, sx + 20, sz + 3]	
	else:
		road_tiles = [sx, sz, sx + 3, sz + 20]

	for x in range(road_tiles[0],road_tiles[2]):
		for z in range(road_tiles[1],road_tiles[3]):
			new_entities.add(BaseEntity('=', x, entities.yproject(x, z), z, attrs = {'terrain'}))



	# Place a house
	return house(entities, 20,20,10,10, door_direction = 4) + new_entities
def house(entities, x, z, w, h, door_direction):
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
	print(doorx, doorz)		
	# Make the floor

	for i in range(x, x + w):
		for j in range(z, z + h):
			new_entities.add(BaseEntity('+', i, y, j, draw_index = -2, attrs = {}))

	# Make the walls!
	for i in range(x, x + w):
		new_entities.add(BaseEntity(0xC4, i, y, z, draw_index = 2, passable = False))
		new_entities.add(BaseEntity(0xC4, i, y, z + h, draw_index = 2, passable = False))


	for i in range(z, z + h):
		new_entities.add(BaseEntity(0xB3, x, y, i, draw_index = 2, passable = False))
		new_entities.add(BaseEntity(0xB3, x + w, y, i, draw_index = 2, passable = False))

	# We also need a door!
	new_entities.add(BaseEntity('+', doorx, y, doorz, draw_index = -2))

	return new_entities