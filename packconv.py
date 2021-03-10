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
	"bricks.png": [7,0],
	"cobweb.png": [11,0],
	"rose.png": [12,0],
	"oak_sapling.png": [15,0],

	"cobblestone.png": [0,1],
	"bedrock.png": [1,1],
	"sand.png": [2,1],
	"gravel.png": [3,1],
	"log_side.png": [4,1],
	"log_top.png": [5,1],
	
	"iron_block.png": [6,1],
	"gold_block.png": [7,1],
	"diamond_block.png": [8,1],

	"chest_top.png": [9,1],
	"chest_side.png": [10,1],
	"chest_front.png": [11,1],

	"gold_ore.png": [0,2],
	"iron_ore.png": [1,2],
	"coal_ore.png": [2,2],
	"bookshelf.png": [3,2],

	"obsidian.png": [5,2],
	"grass_block_side_overlay.png": [6,2],
	"grass.png": [7,2],
	"grass_block_top_overlay.png": [8,2],

	"crafting_table_top.png": [11,2],
	"furnace_front.png": [12,2],
	"furnace_side.png": [13,2],

	"sponge.png": [0,3],
	"glass.png": [1,3],
	"diamond_ore.png": [2,3],
	"greendust_ore_active.png": [3,3],
	"leaves.png": [4,3],

	"stone_brick.png": [6,3],
	"deadbush.png": [7,3],
	"crafting_table_side.png": [11,3],
	# 12, 3 is also a valid choice, but we only use one texture
	"furnace_front_active.png": [13,3],
	"furnace_top.png": [14,3],

	"wool_white.png": [0,4],
	"snow.png": [2,4],
	"grass_block_top_snowy.png": [2,4], # duplicate texture! eek!
	"ice.png": [3,4],
	"grass_block_side_snow.png": [4,4],
	"cactus_top.png": [5,4],
	"cactus_side.png": [6,4],
	"clay.png": [8,4],
	"sugarcane.png": [9,4],

	"torch.png": [0,5],
	"door_top.png": [1,5],
	"ladder.png": [3,5],
	"trapdoor.png": [4,5],
	"iron_bars.png": [5,5],
	"farmland_wet.png": [6,5],
	"farmland.png": [7,5],
	
	# wheat!
	"wheat_plant_0.png": [8, 5],
	"wheat_plant_1.png": [9, 5],
	"wheat_plant_2.png": [10,5],
	"wheat_plant_3.png": [11,5],
	"wheat_plant_4.png": [12,5],
	"wheat_plant_5.png": [13,5],
	"wheat_plant_6.png": [14,5],
	"wheat_plant_7.png": [15,5],

	"door_bottom.png": [1,6],
	"pumpkin_top.png": [6,6],

	"hellstone.png": [7,6],
	"hellsand.png": [8,6],
	"vibrantstone.png": [9,6],
	
	"wool_black.png": [1,7],
	"wool_dark_grey.png": [2,7],

	"pumpkin_side.png": [6,7],
	"jackolantern_face.png": [7,7],
	"jackolantern_face_lit.png": [8,7],

	"wool_red.png": [1,8],
	"wool_pink.png": [2,8],

	"bed_top_bottom.png": [6,8],
	"bed_top_top.png": [7,8],
	"melon_side.png": [8,8],
	"melon_top.png": [9,8],

	"wool_green.png": [1,9],
	"wool_lime.png": [2,9],

	"bed_end_bottom.png": [5,9],
	"bed_side_bottom.png": [6,9], # nice
	"bed_side_top.png": [7,9],
	"bed_end_top.png": [8,9],

	"wool_brown.png": [1,10],
	"wool_yellow.png": [2,10],
	
	"sandstone_top.png": [0,11],
	"wool_blue.png": [1,11],
	"wool_picton.png": [2,11],

	"sandstone_side.png": [0,12],
	"wool_purple.png": [1,12],
	"wool_magenta.png": [2,12],
	
	"sandstone_bottom.png": [0,13],
	"wool_cyan.png": [1,13],
	"wool_orange.png": [2,13],
	
	"chiseled_stone_brick.png": [5,13],

	"wool_grey.png": [1,14],
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

	textures = {}

	for tex in tqdm(texture_indices, desc="crop textures"):
		indice = texture_indices[tex]

		indice[0] = indice[0] * 16
		indice[1] = indice[1] * 16
		
		# Size values
		# used for textures that are either animated or encompass more than one block
		if not 2 in indice: indice.insert(2,1)
		indice[2] = indice[2] * 16
		if not 3 in indice: indice.insert(3,1)
		indice[3] = indice[3] * 16

		texture = terrainpng.crop((indice[0], indice[1],
								  indice[0]+indice[2], indice[1]+indice[3]))

		textures[tex] = texture

	for texture in tqdm(textures, desc="save textures"):
		texture = textures[texture]
		texture.save(
			os.path.join("bobcraft-minecraft-texturepack", tex)
			)
	
	# Now create a description.txt
	desc = """Texture Pack intended for the 'bobcraft' subgame.
Generated from a minecraft.jar file!
NOTE: May cause issues with certain games/mods due to its' non-namespaced texture names.
NOTE: Will NOT work in its current state with minetest_game.
	"""
	txt = open(os.path.join("bobcraft-minecraft-texturepack", "description.txt"), "w")
	txt.write(desc)
	txt.close()