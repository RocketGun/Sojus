
#################################################################################################
# Nuke Environment Settings
#################################################################################################
nk_name = "unPremultWrapper"
nk_help = "Wrapp selected nodes with an Unpremult and a premult, is nothing slected just a premult"
nk_hotkey = "u"
nk_version = "0.1"
nk_call = "unPremultWrapper"
#################################################################################################


import nuke


def unPremultWrapper():
  
    
    n = nuke.selectedNodes()
    
    if len(n) > 0:
    	__setSelectState(n, False)
    	ln = n[len(n)-1]
    	ln.setSelected(True)
    	p = nuke.createNode('Premult')
    	ln.setSelected(False)
    	p.setSelected(False)
    	
    	fn = n[0]
    	try:
    		d = fn.dependencies()[0]
    		d.setSelected(True)
    		nuke.createNode('Unpremult')
    	except: pass
    else:
    	p = nuke.createNode('Premult')


def __setSelectState(nodes, state):
    for n in nodes:
    	n.setSelected(state)