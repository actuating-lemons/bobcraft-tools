# Generates the portal texture.
# Not a tool on its' own.

from PIL import Image
import math
import random

from tqdm import tqdm

# Used for the minecraft texturepack.
def generate_minecraft():
	portal_texture = Image.new("RGBA", (16,512))
	portalTextureData = portal_texture.load()

	random.seed(100)

	for frame in tqdm(range(32), desc="Generate portal animation frames"):
		for x in range(16):
			for y in range(16):

				rand = 0

				for l in range(2):
					
					b = (l * 16) * 0.5
					c = (l * 16) * 0.5
					d = ((x - b) / 16) * 2
					e = ((y - c) / 16) * 2

					if d < -1:
						d += 2
					
					if d >= 1:
						d -= 2
					
					if e < -1:
						d += 2
					
					if e >= 1:
						d -= 2

					f = d * d + e * e
					g = math.atan2(e, d) + (((frame / 32) * math.pi * 2 - f * 10) + (l * 2) * ( l * 2 - 1))
					g = (math.sin(g) + 1) / 2
					g = g / (f + 1.0)
					rand += g * 0.5
				
				rand += random.random() * 0.1
				
				r = rand * rand * 255
				g = rand * rand * 255
				b = rand * rand * 255
				a = rand * rand * 100 + 155

				i2 = round(y + x)

				# print(j1, k1, i1, l1)
				portalTextureData[x, y + frame * 16] = (round(r), round(g), round(b), round(a))

	return portal_texture

if __name__ == "__main__":
	generate_minecraft().show()