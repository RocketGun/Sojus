#################################################################################################
# Nuke Environment Settings
#################################################################################################
nk_name = "AOV Loader"                        # Function name in menu item
nk_help = "Load 3d Layer"					# Description what the function do
nk_hotkey = ""					# Shortcut
nk_version = "1.0.2"							# Versionnumber
nk_call = "loadAOV_alt"					# The main function name
#################################################################################################



'''
2012/01/11
Loading AOV functions
Breaking apart the functions

Warning: Changing the label name will break elementsetup.py

'''
__author__ = 'Alex Henning, Philip Nussbaumer, Tzuen Wu'
__maintainer__ = 'Philip Nussbaumer, Tzuen Wu'
__status__ = 'Development'
__version__ = "1.0.2"

import nuke
import os
import pprint as pp
import re

# Create list of selected read nodes in dict form
def getNodeList():
    
    node_list = nuke.selectedNodes("Read")
    
    node_info = []
    
    # check if read nodes are selected
    if len(node_list) > 0:
        
        for node in node_list:
            # make a read node dict for each node
            rnd = {}
            rnd['node'] = node
            rnd['node_name'] = node['name'].value()
            fpn = node['file'].evaluate()
            
            rnd['fd'] = os.path.split(fpn)[0]
            rnd['fn'] = os.path.split(fpn)[1]
            
            fileData = rnd['fn'].split('_')
            rnd['display_name'] = "%s_%s_%s_%s_%s_%s" % (fileData[1], fileData[2], fileData[3], fileData[4], fileData[5], fileData[-1][0:-9])
            
            # get base and ext for AOV
            rnd['base_fn'] = rnd['fn'].split('.')[0]
            rnd['ext'] = rnd['fn'].split('.')[-1]
            
            # first and last frame of beauty
            rnd['first_frame'] = '%04d' % (node['first'].value())
            rnd['last_frame'] = '%04d' % (node['last'].value())
            
            node_info.append(rnd)  
        
    else:
        nuke.message('Please select one or more read nodes, to load AOVs.')
        return
        
    return node_info

# Create AOV dict for each node 
def getAOV(rnd):
    
    aov_name = [ name for name in os.listdir(rnd['fd']) if os.path.isdir(os.path.join(rnd['fd'], name)) ]
    aovDict = {}
    
    for entry in aov_name:
        aov_dir = os.path.join(rnd['fd'], entry)
        
        # check if entry is a folder
        if os.path.isdir(aov_dir) == True:
            print 'AOV LOADER: Directory: %s' % (aov_dir)
            
            # create AOV fpn
            aov_file = rnd['base_fn'] + '.' + entry + '.%04d.' + rnd['ext']
            aov_fpn = os.path.join(aov_dir, aov_file)
                    
            # check if AOV file exists and if add to list - creating checkAovFpn with file number in order to check file
            checkAovFpn = aov_fpn.replace('.%04d.', '.'+ rnd['first_frame']+'.')
            print checkAovFpn
            if os.path.exists(checkAovFpn):
                        
                # if file sequence is only one frame use fpn with frame number
                if (int(rnd['last_frame'])-int(rnd['first_frame'])) <= 1:
                    aov_fpn = checkAovFpn
                        
                aov_fpn = aov_fpn.replace('\\','/')
                aovDict[entry] = aov_fpn
    
    print 'AOV LOADER: AOVs found for %s:' % (rnd['fn'])
    pp.pprint(aovDict)

    return aovDict

# Bring in AOVs: zdepth, GI, lighting


# Bring AOVs into the group node, standard        
def buildAOVGroup(aovkey, filepath, first, last, lastShuffle, xpos_read):
    
    xpos_shuffle = lastShuffle['xpos'].value()
    
    # set vars
    aovPass = str(aovkey)
    aovFpn = str(filepath)
    aovPassGreen = str(aovPass+".green")
    aovPassRed = str(aovPass+".red")
    aovPassBlue = str(aovPass+".blue")
    aovPassAlpha = str(aovPass+".alpha")
    aovFirstFrame = first
    aovLastFrame = last
    aovReadNodeName = str(aovPass + '_Read')
    
    # create AOV read node
    readNode = nuke.nodes.Read(name = aovReadNodeName, file = aovFpn, xpos = xpos_read, ypos = lastShuffle.ypos()+100, postage_stamp = False, first = aovFirstFrame, last = aovLastFrame, origfirst =  aovFirstFrame, origlast = aovLastFrame)
    
    # create AOV layer in nuke
    nuke.Layer(aovPass, [aovPassRed, aovPassGreen, aovPassBlue, aovPassAlpha])
    
    # create shuffle and shuffle in aov pass
    shuffleNode = nuke.nodes.ShuffleCopy(name = aovPass, out = aovPass, red = 'red', green = 'green', blue = 'blue', selected = True, xpos = xpos_shuffle, ypos = lastShuffle.ypos()+100)
    
    shuffleNode.setInput(1, readNode)
    shuffleNode.setInput(0, lastShuffle)
    
    lastShuffle = shuffleNode
        
    return lastShuffle

# Repetitive. Function to do same as buildAOVGroup except this divides. Need better idea.
def buildAOVDivide(aovkey, filepath, first, last, lastShuffle, xpos_read, dot):
    xpos_shuffle = lastShuffle['xpos'].value()
    
    aovPass = str(aovkey)
    aovFpn = str(filepath)
    aovPassGreen = str(aovPass+".green")
    aovPassRed = str(aovPass+".red")
    aovPassBlue = str(aovPass+".blue")
    aovPassAlpha = str(aovPass+".alpha")
    aovFirstFrame = first
    aovLastFrame = last
    aovReadNodeName = str(aovPass[3:] + '_Read')

    # create AOV read node
    readNode = nuke.nodes.Read(name = aovReadNodeName, file = aovFpn, xpos = xpos_read, ypos = lastShuffle.ypos()+100, postage_stamp = False, first = aovFirstFrame, last = aovLastFrame, origfirst =  aovFirstFrame, origlast = aovLastFrame)

    # create AOV layer in nuke
    nuke.Layer(aovPass, [aovPassRed, aovPassGreen, aovPassBlue, aovPassAlpha])

    # create shuffle and shuffle in aov pass, except for light, gi, zDepth
    shuffleNode = nuke.nodes.ShuffleCopy(name = aovPass, out = aovPass, red = 'red', green = 'green', blue = 'blue', selected = True, xpos = xpos_shuffle, ypos = lastShuffle.ypos()+100)
    
    diffuse = nuke.toNode('diffuse_Read')
    lightDiv = nuke.nodes.Merge(name = "lightDiv", operation = 'divide', selected = True, xpos = readNode['xpos'].value()+150, ypos = shuffleNode['ypos'].value())
    lightDiv.setInput(0, diffuse)
    lightDiv.setInput(1, readNode)
    copyAlpha_light = nuke.nodes.Copy(from0 = 'rgba.alpha', to0 = 'rgba.alpha', selected = True, xpos = readNode['xpos'].value()+300, ypos = shuffleNode['ypos'].value()-10)
    copyAlpha_light.setInput(0, lightDiv)
    copyAlpha_light.setInput(1, dot)
    premultLight = nuke.nodes.Premult(selected = True, xpos = readNode['xpos'].value()+450, ypos = shuffleNode['ypos'].value())
    premultLight.setInput(0, copyAlpha_light)
    
    shuffleNode.setInput(1, premultLight)
    shuffleNode.setInput(0, lastShuffle)
    aovPass2 = aovPass.replace('raw', '').replace('t', 'ting').replace('L', 'l')
    aovPass2Green = str(aovPass2+".green")
    aovPass2Red = str(aovPass2+".red")
    aovPass2Blue = str(aovPass2+".blue")
    aovPass2Alpha = str(aovPass2+".alpha")
    nuke.Layer(aovPass2, [aovPass2Red, aovPass2Green, aovPass2Blue, aovPass2Alpha])
    shuffleNode2 = nuke.nodes.ShuffleCopy(name = aovPass2, out = aovPass2, red = 'red', green = 'green', blue = 'blue', selected = True, xpos = xpos_shuffle, ypos = shuffleNode.ypos()+50)
    shuffleNode2.setInput(1, readNode)
    shuffleNode2.setInput(0, shuffleNode)
    
    lastShuffle = shuffleNode2
    return lastShuffle

# May be Deprecated, new depthz in beauty exr
def buildzDepth(aovkey, filepath, first, last, lastShuffle, xpos_read):
    xpos_shuffle = lastShuffle['xpos'].value()
    
    aovPass = str(aovkey)
    aovFpn = str(filepath)
    aovPassGreen = str(aovPass+".green")
    aovPassRed = str(aovPass+".red")
    aovPassBlue = str(aovPass+".blue")
    aovPassAlpha = str(aovPass+".alpha")
    aovFirstFrame = first
    aovLastFrame = last
    aovReadNodeName = str(aovPass + '_Read')

    readNode = nuke.nodes.Read(file = aovFpn, xpos = xpos_read, ypos = lastShuffle.ypos()+100, postage_stamp = False, first = aovFirstFrame, last = aovLastFrame, origfirst =  aovFirstFrame, origlast = aovLastFrame)
                    
    # create shuffle and shuffle in aov pass, except for light, gi, zDepth
    shuffleNode = nuke.nodes.Copy(name = aovPass, from0 = 'red', to0 = 'depth.Z', selected = True, xpos = xpos_shuffle, ypos = lastShuffle.ypos()+100)
    shuffleNode.setInput(1, readNode)
    shuffleNode.setInput(0, lastShuffle)
                    
    lastShuffle = shuffleNode
    return lastShuffle
    

def makeAOVGroup(node, aovDict, aovGroup):
    #set position and look of AOV group
    aovGroup.setXYpos(node.xpos(), node.ypos()+90)
    aovGroup.setInput(0, node)
    aovGroup['tile_color'].setValue(0x75ffff)
    aovGroup['note_font'].setValue("bold")
    aovGroup['note_font_color'].setValue(0xffaf00ff)
    aovGroup['note_font_size'].setValue(10)
    
    # make list for group tab
    aovList = aovDict.keys()
    aovList.sort()
    stringbuilder = "\n"
    for item in aovList:
        stringbuilder = stringbuilder + item + '\n'
    
    aovGroupTab = nuke.Tab_Knob('AOVs')
    aovGroupDivider = nuke.Text_Knob('')
    aovGroupInfo = nuke.Text_Knob('i:','Info:', 'Adds AOV channels to a beauty. Acts from now downstream like a multilayer EXR')
    aovGroupButtonUpdate = nuke.PyScript_Knob('btn2', '  Update  ', 'import aovloader; aovloader.update()')
    aovGroupPasses = nuke.Text_Knob('i2:','AOVs:', stringbuilder)
    aovGroupButton = nuke.PyScript_Knob('btn', '  Info  ', 'import webbrowser; webbrowser.open(\'http://wiki.pxm-lax.intra/tools/nuke/faq/working_with_AOV%27s_in_Nuke\')')
    aovGroup.addKnob(aovGroupTab)
    aovGroup.addKnob(aovGroupDivider)
    aovGroup.addKnob(aovGroupInfo)
    aovGroup.addKnob(nuke.Text_Knob(' '))
    aovGroup.addKnob(aovGroupButtonUpdate)
    aovGroup.addKnob(nuke.Text_Knob(' '))
    aovGroup.addKnob(aovGroupPasses)
    aovGroup.addKnob(nuke.Text_Knob(' '))
    aovGroup.addKnob(aovGroupButton)

def update():
    n = nuke.thisNode()
    label = n['label'].value()
    dependents = n.dependencies()
    for d in dependents:
        if d.Class() == 'Read':
            if d['file'].value().find(label) != -1:
                nuke.message('Version is the same.')
            else:
                new_version = re.findall('v\d\d\d', d['file'].value())[0]
                old_version = re.findall('v\d\d\d', label)[0]
                count = 0
                for child in n.nodes():
                    if child.Class() == 'Read':
                        count += 1
                        fpn = child['file'].value()
                        print fpn
                        fpn = fpn.replace(old_version, new_version)
                        child['file'].setValue(fpn)
                        print 'AOVLOADER: %s added.' % fpn
                newlabel = label.replace(old_version, new_version)
                n['label'].setValue(newlabel)
                folder = os.path.split(d['file'].value())[0]
                contents = os.listdir(folder)
                readfolder = []
                for c in contents:
                    print c
                    if os.path.isdir(os.path.join(folder, c).replace('\\', '/')):
                        if c != 'alpha':
                            readfolder.append(c)

                readcount = len(readfolder)
                print readcount
                print count
                if readcount != count:
                    nuke.message('The number of AOVs are different.\nPlease re-run aovloader (Alt+Q)')
                        
    

# Builds in conversion - HUG / FNT 
def loadAOV_alt():
    
    node_info = getNodeList()
    
    node_groups = []
    
    if len(node_info) > 0:
        for rnd in node_info:
            aovDict = getAOV(rnd)
            
            if len(aovDict) > 0:
                aovGroup = nuke.nodes.Group(name = 'AOV', label = rnd['display_name'])
                aovGroup.setName('AOV')
                
                # put scope to AOVgroup level
                nuke.Group.begin(aovGroup)
                n_input = nuke.nodes.Input()
                n_output = nuke.nodes.Output()
                
                lastShuffle = n_input
                
                aovSubDict = aovDict.copy()
                aovExtraDict = {} 
                
                # Delete items to not be iterated over
                if 'zDepth' in aovSubDict:
                    del aovSubDict['zDepth']
                    aovExtraDict['zDepth'] = aovDict['zDepth']
                else:
                    print 'AOV LOADER: No zDepth pass found. Go find your lighter.'
                
                # fix for Dan, he wants to keep the lighting pass
                if 'lighting' in aovSubDict:
                    aovExtraDict['rawLight'] = aovDict['lighting']
                    del aovSubDict['lighting']
                else:
                    print 'AOV LOADER: No lighting pass found. Go find your lighter.'
                
                if 'GI' in aovSubDict:
                    aovExtraDict['rawGI'] = aovDict['GI']
                    del aovSubDict['GI']
                else:
                    print 'AOV LOADER: No GI pass found. Go find your lighter.'
                    
                if 'diffuse' in aovSubDict:
                    #del aovSubDict['diffuse']
                    pass
                else:
                    print 'AOV LOADER: No diffuse pass found. Go find your lighter.'
                
                dot = nuke.nodes.Dot(xpos = n_input.xpos()-200, ypos = (n_input.ypos()))
                dot.setInput(0, n_input)
                
                print 'Where are my extra dicts?'
                pp.pprint(aovSubDict)
                
                # make Diffuse
                xpos_read = n_input.xpos()-450
                if 'diffuse' in aovSubDict:
                    print 'AOV LOADER: building diffuse.'
                    lastShuffle = buildAOVGroup('diffuse', aovDict['diffuse'], rnd['first_frame'], rnd['last_frame'], lastShuffle, xpos_read)
                    del aovSubDict['diffuse']
                else:
                    pass
                
                # divide in filtered lighting and gi with diffuse to make raw
                xpos_read = n_input.xpos()-700
                for aovkey, filepath in aovExtraDict.iteritems():
                    if aovkey != 'zDepth':
                        try:
                            lastShuffle = buildAOVDivide(aovkey, filepath, rnd['first_frame'], rnd['last_frame'], lastShuffle, xpos_read, dot)
                        except:
                            pass
                # add in zDepth
                xpos_read = lastShuffle.xpos()-100
                try:
                    lastShuffle = buildzDepth('zDepth', aovDict['zDepth'], rnd['first_frame'], rnd['last_frame'], lastShuffle, xpos_read)
                except:
                    pass
                
                # Everything else
                for aovkey, filepath in aovDict.iteritems():
                    lastShuffle = buildAOVGroup(aovkey, filepath, rnd['first_frame'], rnd['last_frame'], lastShuffle, xpos_read)
                
                n_output.setXYpos(n_input.xpos(), lastShuffle.ypos()+100)
                n_output.setInput(0, lastShuffle)
                
                # bring back scope to root level
                nuke.Group.end(aovGroup)
                
                makeAOVGroup(rnd['node'], aovDict, aovGroup)
                
                node_groups.append(aovGroup)
            
            else:
                nuke.message('No AOVs found in Folder '+rnd['fd']+' for Node '+rnd['node_name'])
                return
    
    return node_groups


# Does the same as Philip N's original loader
def loadAOV():
    
    node_info = getNodeList()

    for rnd in node_info:
        aovDict = getAOV(rnd)
        
        if len(aovDict) > 0:
            aovGroup = nuke.nodes.Group(name = 'AOV', label = rnd['display_name'])
            
            # put scope to AOVgroup level
            nuke.Group.begin(aovGroup)
            n_input = nuke.nodes.Input()
            n_output = nuke.nodes.Output()
            
            lastShuffle = n_input
            xpos_read = lastShuffle.xpos()-100
            
            for aovkey, filepath in aovDict.iteritems():
                lastShuffle = buildAOVGroup(aovkey, filepath, rnd['first_frame'], rnd['last_frame'], lastShuffle, xpos_read)

            n_output.setXYpos(n_input.xpos(), n_input.ypos()+(len(aovDict)+1)*100)
            n_output.setInput(0, lastShuffle)
            
            # bring back scope to root level
            nuke.Group.end(aovGroup)
            
            makeAOVGroup(rnd['node'], aovDict, aovGroup)
            
        else:
            nuke.message('No AOVs found in Folder '+rnd['fd']+' for Node '+rnd['node_name'])
            return

