# Generate a map
from noise import snoise2

def main(seed, mx, my, wx, wy, flatness = 0.4):
    MAP_ROUND = 4
    mx, my = range(mx * MAP_ROUND), range(my * MAP_ROUND)
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
    fl = []
    for x in range(len(l) // MAP_ROUND):
        fl.append([])
        for y in range(len(l[0]) // MAP_ROUND):
            avg = 0
            c = 0
            for i in range(MAP_ROUND):
                for j in range(MAP_ROUND):
                    c += 1
                    avg += l[MAP_ROUND * x + i][MAP_ROUND * y + j]

            fl[x].append(avg / c)

    return l


if __name__ == '__main__':
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import numpy as np