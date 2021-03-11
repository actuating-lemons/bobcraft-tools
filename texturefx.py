# Generates the portal texture.
# Not a tool on its' own.

from PIL import Image
import math
import random
import numpy # more math

from tqdm import tqdm

# Used for the minecraft texturepack.
def generate_portal_minecraft():
	portal_texture = Image.new("RGBA", (16,512))
	portalTextureData = portal_texture.load()

	random.seed(100)

	for frame in tqdm(range(32), desc="Generate portal animation frames"):
		for x in range(16):
			for y in range(16):

				rand = 0

				for l in range(4):
					
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
				
				r = rand * rand * 255 + 155
				g = rand * rand * 255 + 155
				b = rand * rand * 255 + 155
				a = rand * rand * 200 + 155

				i2 = round(y + x)

				# print(j1, k1, i1, l1)
				portalTextureData[x, y + frame * 16] = (round(r), round(g), round(b), round(a))

	return portal_texture

def generate_lava_minecraft():
	lava_texture = Image.new("RGB", (16,16*16))
	lava_texture_pixels = lava_texture.load()

	# Reliable output
	random.seed(69)

	# now, of-course, the lava texture is generated ON TICK, not once at start-up, like the portal.
	# So we have to sacrafice accuracy and generate some frames of it.

	# We also have four arrays, which I don't what are for.
	# Fun-fact, I use the Minecraft Coder Pack as yarn hasn't done 1.2.5!
	# There's probably more useful mappings in yarn! but that code's too new to count!
	# AAAAAAAAAAAAAAAAAA
	texture_data = [0.0]*256
	# These seem to only get interacted with in the context of x/y, so this makes sense....
	# They were also called _i and _j, which is what x and y were called, so :shrug:
	yellow = [0.0]*256
	speckles = [0.0]*256
	# I don't know what this does.
	buffer = [0.0]*256

	# we want to fill the buffers with data, so we quickly just permutate ~1000 times
	for i in range(1024):
		texture_data, yellow, speckles, buffer = do_the_lava(texture_data, yellow, speckles, buffer)

	for frame in range(16):
		texture_data, yellow, speckles, buffer = do_the_lava(texture_data, yellow, speckles, buffer)

		pixelindex = 0
		for x in range(16):
			for y in range(16):
				f1 = texture_data[pixelindex] * 2

				if f1 > 1:
					f1 = 1
				if f1 < 0:
					f1 = 0
				
				f2 = f1
				# finally, soemthing recognisable, COLOUR COMPONENTS!
				r = f2 * 100 + 155
				g = f2 * f2 * 255
				ydata = f2 * f2 * f2 * f2 * 128

				lava_texture_pixels[x,y+(frame*16)] = (round(r),round(g),round(ydata))

				pixelindex += 1 # NUCLEAR OPTION

	return lava_texture

def do_the_lava(texture_data, yellow, speckles, buffer):
	for x in range(16):
		for y in range(16):

			amplitude = 0

			xspeckler = round(math.sin(((x * math.pi * 2) / 16) * 1.2))
			yspeckler = round(math.sin(((y * math.pi * 2) / 16) * 1.2))

			for x1 in range(x-1, x+1):
				for x2 in range(y-1, y+1):
					xdata = x1 + xspeckler & 0xf
					ydata = x2 + yspeckler & 0xf

					amplitude += texture_data[xdata + ydata * 16]

			buffer[x + y * 16] = amplitude / 10 + ((
				yellow[(x + 0 & 0xf) + (y + 0 & 0xf) * 16] +
				yellow[(x + 1 & 0xf) + (y + 0 & 0xf) * 16] +
				yellow[(x + 1 & 0xf) + (y + 1 & 0xf) * 16] +
				yellow[(x + 0 & 0xf) + (y + 1 & 0xf) * 16]) / 4) * 2

			yellow[x + y * 16] += speckles[x + y * 16] * 0.01

			if yellow[x + y * 16] < 0:
				yellow[x + y * 16] = 0
			
			speckles[x + y * 16] -= 0.06

			if random.random() < 0.005:
				speckles[x + y * 16] = 1.5

	swapper = buffer
	buffer = texture_data
	texture_data = swapper

	return texture_data, yellow, speckles, buffer

# Used for bobcraft's default texture pack.
def generate_portal_bobcraft():
	portal_texture = Image.new("RGBA", (16,16*16))
	portalTextureData = portal_texture.load()

	random.seed(69) # nice

	for frame in tqdm(range(16), desc="generate bobcraft portal animation frames"):
		for x in range(16):
			for y in range(16):
				rand = 0

				for l in range(4):

					scale = 2.5
					
					octave = (l * 16) * 0.5
					octave2 = (l * 16) * 0.5
					d = ((x - octave) / 16) * scale
					e = ((y - octave2) / 16) * scale

					if d < -1:
						d += scale
					
					if d >= 1:
						d -= scale
					
					if e < -1:
						d += scale
					
					if e >= 1:
						d -= scale

					f = d * d + e * e
					g = math.atan2(e, d) + (((frame / 16) * math.pi * 2 - f * 10) + (l * 2) * ( l * 2 - 1))
					g = (math.sin(g) + 1) / 2
					g = g / (f + 1.0)
					rand += g * 0.5
				
				rand += random.random() * 0.1
				
				r = rand * rand * 255 + 155
				g = rand * rand * 255 + 155
				b = rand * rand * 255 + 155
				a = rand * rand * 255 + 200

				# print(j1, k1, i1, l1)
				portalTextureData[x, y + frame * 16] = (round(r), round(g), round(b), round(a))

	return portal_texture

if __name__ == "__main__":
	# print("Ran as main, generating bobcraft textures...")
	# image = generate_portal_bobcraft()
	# image.show()
	# image.save("portal.png")

	image = generate_lava_minecraft()
	image.show()
	image.save("lava.png")