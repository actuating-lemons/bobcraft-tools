"""
	Pack conv, converts a minecraft.jar's terrain.png into a texture pack for use with bobcraft.
"""

import zipfile
from PIL import Image
import os
import sys
import shutil

from tqdm import tqdm

texture_indices = {
	"stone.png": [1,0],
	"dirt.png": [2,0],
	"grass_block_side.png": [3,0],
	"planks.png": [4,0],
}

if __name__ == "__main__":

	#Ensure we have a minecraft.jar
	if not os.path.exists("minecraft.jar"):
		print("minecraft.jar not found!")
		sys.exit(-1)

	if not zipfile.is_zipfile("minecraft.jar"):
		print("minecraft.jar appears malformed! (Not a valid zip archive)")
		sys.exit(-1)

	# Open the jar file
	jar = zipfile.ZipFile("minecraft.jar", "r")

	# TODO: is there a better way to test?
	if not "terrain.png" in jar.namelist():
		print("minecraft.jar does not have a terrain.png file. What version is it from? This tool is built for 1.2.5!")
		sys.exit(-1)

	if not os.path.exists("bobcraft-minecraft-texturepack"):
		print("Output directory doesn't exist, creating...")
	else:
		print("Output directory exists, cleaning...")
		shutil.rmtree("bobcraft-minecraft-texturepack")

	os.mkdir("bobcraft-minecraft-texturepack")
	
	terrainpng = jar.open("terrain.png")
	terrainpng = Image.open(terrainpng)

	for tex in tqdm(texture_indices, desc="crop & save textures"):
		indice = texture_indices[tex]

		indice[0] = indice[0] * 16
		indice[1] = indice[1] * 16

		texture = terrainpng.crop((indice[0], indice[1],
								  indice[0]+16, indice[1]+16))
		

		texture.save(
			os.path.join("bobcraft-minecraft-texturepack", tex)
			)