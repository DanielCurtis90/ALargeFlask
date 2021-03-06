#Python file 

import os, sys
from entityprocessor import *

def shifted_bounds(shifted_dict):
	#Make sure this is shifted (no negative coords!)
	y_coords = []
	x_coords = []
	for value in shifted_dict.values():
		#dig into the first and second entries of the embedded coordinate list to get the x and y coordinates
		x_coords.append(value.xpoint)
		y_coords.append(value.ypoint)	
	bounds = [min(x_coords), max(x_coords), min(y_coords), max(y_coords)]
	return bounds

def blocks_to_eps(block_dict, INSERT):
	block_string = []
	Refd_Block = block_dict[INSERT.name]
	#Check entities to draw
	block_string.append(f"{INSERT.xpoint} {INSERT.ypoint} moveto\n({INSERT.ID}) show\n2 setlinewidth\n0.5 setgray\nstroke\n")
	if hasattr(Refd_Block, 'lwpolylines'):
		for lwp in Refd_Block.lwpolylines:
			#get the starting point and move to it
			first_x = lwp.vertices[0].xpoint
			first_y = lwp.vertices[0].ypoint
			block_string.append(f"{first_x + INSERT.xpoint} {first_y + INSERT.ypoint} moveto\n")
			#iterate over remaining vertices (based on where the x coordinate for the second vertex is stored)
			for vertex in lwp.vertices[1:]:
				block_string.append(f"{vertex.xpoint + INSERT.xpoint} {vertex.ypoint + INSERT.ypoint} lineto\n")
			block_string.append(f"closepath\n2 setlinewidth\n0.5 setgray\nstroke\n")
	if hasattr(Refd_Block, 'lines'):
		for ln in Refd_Block.lines:
			#get the starting point and move to it
			first_x = ln.vertices[0].xpoint
			first_y = ln.vertices[0].ypoint
			block_string.append(f"{first_x + INSERT.xpoint} {first_y + INSERT.ypoint} moveto\n")
			#iterate over remaining vertices (based on where the x coordinate for the second vertex is stored)
			for vertex in ln.vertices[1:]:
				block_string.append(f"{vertex.xpoint + INSERT.xpoint} {vertex.ypoint + INSERT.ypoint} lineto\n")
			block_string.append(f"closepath\n2 setlinewidth\n0.5 setgray\nstroke\n")
	return block_string

def draw_eps(shifted_dict, block_dict, dxffile):
	bounds = shifted_bounds(shifted_dict)
	with open(os.path.splitext(dxffile)[0] + ".eps", "w") as outputfile:
		#Write the start and bounding box
		outputfile.write(f"%!PS-Adobe-3.1 EPSF-3.0\n%%BoundingBox: {bounds[0]} {bounds[2]} {bounds[1]} {bounds[3]}\n/Times-Roman findfont\n24 scalefont\nsetfont\n")
		for value in shifted_dict.values():
			#Draw the block at the coordinates of the INSERT, send the key to find the right block
			block_string = blocks_to_eps(block_dict, value)
			for code_line in block_string:
				outputfile.write(f"{code_line}")
		outputfile.write("showpage")

	return None