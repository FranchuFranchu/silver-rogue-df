import sys
from noise import pnoise2, snoise2

if len(sys.argv) not in (2, 3) or '--help' in sys.argv or '-h' in sys.argv:
	print('2dtexture.py FILE [OCTAVES]')
	print()
	print(__doc__)
	raise SystemExit

f = open(sys.argv[1], 'wt')
if len(sys.argv) > 2:
	octaves = int(sys.argv[2])
else:
	octaves = 16
freq = 8.0 * octaves
f.write('P2\n')
f.write('256 256\n')
f.write('255\n')
for y in range(256):
	for x in range(256):
		f.write("%s\n" % int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0))
f.close()