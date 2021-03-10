# Generates the portal texture.
# Not a tool on its' own.

from PIL import Image
import math
import random

def generate():
	portal_texture = Image.new("RGB", (32,1024))
	portalTextureData = portal_texture.load()

	for i in range(32):
		for j in range(16):
			for k in range(16):

				a = 0

				for l in range(2):
					
					b = (l * 16) * 0.5
					c = (l * 16) * 0.5
					d = ((j - b) / 16) * 2
					e = ((k - c) / 16) * 2

					if d < -1:
						d += 2
					
					if d >= 1:
						d -= 2
					
					if e < -1:
						d += 2
					
					if e >= 1:
						d -= 2

					f = d * d + e * e
					g = math.atan2(e, d) + (((i / 32) * math.pi * 2 - f * 10) + (l * 2) * ( l * 2 - 1))
					g = (math.sin(g) + 1) / 2
					g = g / (f + 1.0)
					a += g * 0.5
				
				a += random.random() * 0.1
				
				i1 = a * 100 + 155
				j1 = a * a * 200 + 55
				k1 = a * a * a * a * 255
				l1 = a * 100 + 155
				i2 = int(k * 16 + j)

				print(j1, k1, i1, l1)
				portalTextureData[i, i2] = (round(j1), round(k1), round(i1))#, l1)

	portal_texture.show()

if __name__ == "__main__":
	generate()