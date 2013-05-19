
#################################################################################################
# Nuke Environment Settings
#################################################################################################
nk_name = "Transform from Tracker"
nk_help = "Wrapp selected nodes with an Unpremult and a premult, is nothing slected just a premult"
nk_hotkey = "alt+t"
nk_version = "1.0"
nk_call = "TransformFromTracker"
#################################################################################################


import nuke

def TransformFromTracker():
	for a in nuke.selectedNodes():
		if a.Class().find("Tracker")  > -1 :
			n = nuke.createNode("Transform" , inpanel = False)
			link = "parent." + a.knob('name').getValue() + "."
			n.knob('translate').setExpression(link+"translate")
			n.knob('rotate').setExpression(link+"rotate")
			n.knob('scale').setExpression(link+"scale")
			n.knob('center').setExpression(link+"center")
			for j in range(n.inputs()): 
				n.setInput(j, None) 
			