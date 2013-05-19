
#################################################################################################
# Nuke Environment Settings
#################################################################################################
nk_name = "Read from Write"
nk_help = "Wrapp selected nodes with an Unpremult and a premult, is nothing slected just a premult"
nk_hotkey = "ctrl+shift+r"
nk_version = "1.0"
nk_call = "ReadFromWrite"
#################################################################################################


import nuke

def ReadFromWrite():
    for a in nuke.selectedNodes():
		if a.Class()=="Write":
			f = a.knob( "file" ).getValue()
			i = int(nuke.root().knob( "first_frame" ).getValue())
			o = int(nuke.root().knob( "last_frame" ).getValue())
			n = nuke.createNode("Read", inpanel = False)
			n.knob('file').setValue(f)
			n.knob('first').setValue(i)
			n.knob('last').setValue(o)