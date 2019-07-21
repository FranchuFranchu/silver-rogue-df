# Generate a map
from noise import snoise2

def main(seed, mx, my, wx, wy, flatness = 0.4):
	mx, my = range(mx), range(my)
	octaves = 32
	freq = octaves * 8
	l = [[0 for i in my] for i in my]
	for x in mx:
		for y in my:
			l[x][y] = snoise2(
				x / freq + wx * len(mx),
			 	y / freq + wy * len(my), 
			 	octaves,
			 	base = 0) 
	return l


if __name__ == '__main__':
	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt
	import numpy as np