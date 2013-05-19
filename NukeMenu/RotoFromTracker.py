
#################################################################################################
# Nuke Environment Settings
#################################################################################################
nk_name = "Rotonode from Tracker"
nk_help = "Create a Roto Node with an Expression in Transform"
nk_hotkey = "alt+o"
nk_version = "1.0"
nk_call = "RotoFromTracker"
#################################################################################################


import nuke

def RotoFromTracker():
	for a in nuke.selectedNodes():
		if a.Class().find("Tracker")  > -1 :
			n = nuke.createNode("Roto" , inpanel = False)
			link = "parent." + a.knob('name').getValue() + "."
			#n=n.knob("curves")
			n.knob('curves.translate').setExpression(link+"translate")
			n.knob('curves.rotate').setExpression(link+"rotate")
			n.knob('curves.scale').setExpression(link+"scale")
			n.knob('curves.center').setExpression(link+"center")
			for j in range(n.inputs()): 
				n.setInput(j, None)
			