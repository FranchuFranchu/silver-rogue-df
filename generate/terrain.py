from noise import snoise2
import random

def main(seed, mx, my, wx, wy):
	mx, my = range(mx), range(my)
	octaves = 16
	freq = octaves * 16
	l = [[0 for i in my] for i in my]
	for x in mx:
		for y in my:
			l[x][y] = snoise2(x / freq + wx * len(mx), y / freq + wy * len(my), octaves,base = seed) 
	return l
