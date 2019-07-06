from noise import snoise2
import random

def main(mx,my):
	seed = random.random() * 1000
	mx, my = range(mx), range(my)
	octaves = 8
	freq = octaves * 16
	l = [[0 for i in my] for i in my]
	for x in mx:
		for y in my:
			l[x][y] = snoise2(x / freq, y / freq, octaves,base = seed)
	return l
