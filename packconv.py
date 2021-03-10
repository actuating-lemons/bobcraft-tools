"""
	Pack conv, converts a minecraft.jar's terrain.png into a texture pack for use with bobcraft.
"""

import zipfile
from PIL import Image
import os
import sys

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
	
	terrainpng = jar.open("terrain.png")
	terrainpng = Image.open(terrainpng)
	terrainpng.show()