'''
Created on 07.08.2011

@author: jonas thorbruegge (jonas@mischlicht.com)
'''



import nuke, os, sys

nuke.pluginAddPath(os.path.dirname(__file__))

class sojus():
    def __init__(self):
        
        
        #nuke.pluginAddPath(os.path.dirname(__file__))
        
        self.setNodeDefaults()
        self.setPresets()
        self.buildNukeMenu()
        self.buildNodeMenu()
        
    def buildNukeMenu(self):
        self.NukeMenu = nuke.menu( "Nuke" ).findItem( "RG" )
        
        if not self.NukeMenu:
            self.NukeMenu = nuke.menu( "Nuke"  ).addMenu("RG")

        self._builMenuFromPath(self.NukeMenu, os.path.dirname(__file__), "NukeMenu")

    def buildNodeMenu(self):

        # set up menu
        self.NodeMenu = nuke.menu( "Nodes" ).findItem( "RocketGunNodes" )
        if not self.NodeMenu:
            self.NodeMenu = nuke.menu( "Nodes" ).addMenu("RocketGunNodes", icon="sojus.png")

        #autMenu
        self._builMenuFromPath(self.NodeMenu, os.path.dirname(__file__), "NodeMenu")



    
    def _getFunctionFromModule(self, module, name):
        f = getattr(__import__(module + "." + name), name)
        return [f.nk_name, f.nk_hotkey, f.nk_help, f.nk_version, getattr(f, f.nk_call)]
        
    def _builMenuFromPath(self, menu, basepath, module):

        items = []

        path = os.path.join(basepath,module)

        try:
            for i in os.listdir(path):
                if os.path.isdir(os.path.join(path,i)):
                    nuke.pluginAddPath(path)
                    submnu = menu.addMenu(i, icon=(i + ".png"))
                    self._builMenuFromPath(submnu, path, i)
                    
                else:
                    name, extesion = os.path.splitext(i)
    
                    if extesion.lower() in [".py"]:
                        if name != "__init__":
                            items.append(["f", name])

                            # Generate __init__.py if its not exsist.
                            initfile = os.path.join(path, "__init__.py")
                            if not os.path.exists(initfile):
                                open(initfile, "w").close()
                                
                    elif extesion.lower() == ".gizmo":
                        items.append(["g", name])
                        
                    elif extesion.lower() == ".nk":
                        items.append(["s", name])
                        
        except : print "Error while searching for items in module"

        if len(items) > 0:
            
            nuke.pluginAddPath(path)
            
            for item in items:
                ftype, fname = item
                
                if ftype == "f":
                    try:
                        name, hotkey, help, version, call = self._getFunctionFromModule(module, fname)
                        menu.addCommand(name+ " (v" + version +")", call, hotkey , icon=(fname+".png"))
                        
                    except Exception, e:
                        print "Error while loading " + fname, "\n    ",type(e), "\n    " , e,"\n"
                        
                elif ftype == "g":
                    menu.addCommand(fname, "nuke.createNode('%s')" % fname ,icon=(fname+".png"))
                    
                elif ftype == "s":
                    menu.addCommand(fname, "nuke.scriptSource('%s')" % os.path.join(path, fname + ".nk") ,icon=(fname+".png"))

    def setNodeDefaults(self):
        pass

    def setPresets(self):
        import cam_presets
        cam_presets.nodePresetCamera()

        import reformat_presets
        reformat_presets.nodePresetReformat()
                
        
