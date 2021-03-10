"""
	Pack conv, converts a minecraft.jar's terrain.png into a texture pack for use with bobcraft.
"""

import zipfile
from PIL import Image
import os
import sys
import shutil

from tqdm import tqdm

# Generates the portal texture for us
import portaltex

block_texture_indices = {
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

	"crack_anylength.png": [0,15, 10,1],
}
item_texture_indices = {
	"flint.png": [6,0],
	"coal.png": [7,0],
	"string.png": [8,0],

	"brick.png": [6,1],
	"iron_ignot.png": [7,1],

	"gold_ingot.png": [7,2],

	"sign.png": [10,2],
	"item_door.png": [11,2],
	"bed_item.png": [13,2],

	"diamond.png": [7,3],
	"greendust.png": [8,3],
	"clay_item.png": [9,3],
	"paper.png": [10,3],
	"book.png": [11,3],

	# Food
	"apple.png": [10,0],

	"wheat_seeds.png": [9,0],
	"wheat_item.png": [9,1],
	"bread.png": [9,2],

	"porkchop.png": [7,5],
	"cooked_porkchop.png": [8,5],

	"melon_slice.png": [13,6],

	"sugarcane_item.png": [11,1],

	# Dye
	"dye_black.png": [14, 4],
	"dye_dark_grey.png": [15,4],
	"dye_red.png": [14,5],
	"dye_pink.png": [15,5],
	"dye_green.png": [14,6],
	"dye_lime.png": [15,6],
	"dye_brown.png": [14,7],
	"dye_yellow.png": [15,7],
	"dye_blue.png": [14,8],
	"dye_picton.png": [15,8],
	"dye_purple.png": [14,9],
	"dye_magenta.png": [15,9],
	"dye_cyan.png": [14,10],
	"dye_orange.png": [15,10],
	"dye_grey.png": [14,11],
	"dye_white.png": [15,11],

	# Tools
	# Swords
	"wood_sword.png": [0,4],
	"stone_sword.png": [1,4],
	"iron_sword.png": [2,4],
	"diamond_sword.png": [3,4],
	"gold_sword.png": [4,4],
	# Shovel
	"wood_shovel.png": [0,5],
	"stone_shovel.png": [1,5],
	"iron_shovel.png": [2,5],
	"diamond_shovel.png": [3,5],
	"gold_shovel.png": [4,5],
	# Pickaxe
	"wood_pickaxe.png": [0,6],
	"stone_pickaxe.png": [1,6],
	"iron_pickaxe.png": [2,6],
	"diamond_pickaxe.png": [3,6],
	"gold_pickaxe.png": [4,6],
	# Axe
	"wood_axe.png": [0,7],
	"stone_axe.png": [1,7],
	"iron_axe.png": [2,7],
	"diamond_axe.png": [3,7],
	"gold_axe.png": [4,7],
	# Hoe
	"wood_hoe.png": [0,8],
	"stone_hoe.png": [1,8],
	"iron_hoe.png": [2,8],
	"diamond_hoe.png": [3,8],
	"gold_hoe.png": [4,8],

	"sticks.png": [5,3],
}
gui_texture_indices = { # Measured in pixels
	"hotbar_bg.png": [0,0, 182, 22],
	"hotbar_fg.png": [0, 22, 24, 24],
	
	"formspec_button_bg.png": [0, 66, 200, 20],
	"formspec_button_bg_hover.png": [0, 86, 200, 20],
	"formspec_button_bg_pressed.png": [0, 86, 200, 20],
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
	if not "gui/items.png" in jar.namelist():
		print("minecraft.jar does not have an items.png file. What happened?")
		sys.exit(-1)

	if not os.path.exists("bobcraft-minecraft-texturepack"):
		print("Output directory doesn't exist, creating...")
	else:
		print("Output directory exists, cleaning...")
		shutil.rmtree("bobcraft-minecraft-texturepack")

	os.mkdir("bobcraft-minecraft-texturepack")
	
	terrainpng = jar.open("terrain.png")
	terrainpng = Image.open(terrainpng)

	itemspng = jar.open("gui/items.png")
	itemspng = Image.open(itemspng)

	guipng = jar.open("gui/gui.png")
	guipng = Image.open(guipng)

	textures = {}

	for tex in tqdm(block_texture_indices, desc="crop block textures"):
		indice = block_texture_indices[tex]

		indice[0] = indice[0] * 16
		indice[1] = indice[1] * 16
		
		# Size values
		# used for textures that are either animated or encompass more than one block
		if len(indice) < 3: indice.insert(2,1)
		indice[2] = indice[2] * 16
		if len(indice) < 4: indice.insert(3,indice[2]/16) # assume it to be an equal size
		indice[3] = indice[3] * 16

		texture = terrainpng.crop((indice[0], indice[1],
								  indice[0]+indice[2], indice[1]+indice[3]))

		textures[tex] = texture

	for tex in tqdm(item_texture_indices, desc="crop item textures"):
		indice = item_texture_indices[tex]

		indice[0] = indice[0] * 16
		indice[1] = indice[1] * 16
		
		# Size values
		# used for textures that are either animated or encompass more than one block
		if len(indice) < 3: indice.insert(2,1)
		indice[2] = indice[2] * 16
		if len(indice) < 4: indice.insert(3,indice[2]/16) # assume it to be an equal size
		indice[3] = indice[3] * 16

		texture = itemspng.crop((indice[0], indice[1],
								  indice[0]+indice[2], indice[1]+indice[3]))

		textures[tex] = texture

	for tex in tqdm(gui_texture_indices, desc="crop gui textures"):
		indice = gui_texture_indices[tex]

		texture = guipng.crop((indice[0], indice[1],
								  indice[0]+indice[2], indice[1]+indice[3]))

		textures[tex] = texture

	# Bobcraft has a few textures that minecraft technically doesn't.
	# (atleast in the terrain.png file)
	# So we'll composite them from existing textures we have in terrain.png!

	# first we composite crack_anylength.
	# I hate programming like this, But I don't know how to make this happen automagically.
	crack = Image.new("RGBA", (16,160))
	for i in tqdm(range(0,10), desc="convert crack animation"):
		frame = textures["crack_anylength.png"].crop(
				(i*16, 0,
				(i*16)+16, 16)
		)

		crack.paste(frame, (0, i*16))
	textures["crack_anylength.png"] = crack

	# Water, not a composite, but it's a seperate texture.
	# TODO: where is lava?!
	with jar.open("misc/water.png") as water:
		water = Image.open(water)
		textures["water_still.png"], textures["water_flow.png"] = water, water

	# Generate the portal texture!
	textures["portal.png"] = portaltex.generate_minecraft()

	for texturename in tqdm(textures, desc="save textures"):
		texture = textures[texturename]
		texture.save(
			os.path.join("bobcraft-minecraft-texturepack", texturename)
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