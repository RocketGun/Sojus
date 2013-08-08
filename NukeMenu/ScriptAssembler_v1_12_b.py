#################################################################################################
# RocketGun Nuke Environment Settings
#################################################################################################
nk_name = "Assemble Script"             # Function name in menu item
nk_help = "Assemble Scripts in to a folder"              # Description
nk_hotkey = ""                           # Shortcut
nk_version = "0.12"                      # Versionnumber
nk_call = "assembleScript()"             # The main function name
#################################################################################################




'''
Created on 19.05.2011


@author: Jonas Thorbruegge (jonas@mischlicht.com)

v0.1 (19.05.2011)
v0.12 (25.02.2012)
'''

import sys, os,shutil

import nuke


def addLogLine(log, msg):
    if msg:
        return log + msg +"\n"
    else:
        return log

def copyNodeFileTo(node, dstPath, section):
    
    subsection_images = "images"
    subsection_3dassets = "3dassets"
    subsection_luts = "luts"
    
    
    f = None
    subsection = None
    fileknob = None
    nclass = node.Class()
    
    try:
    
        if nclass == "Read":
            f = pdwFile(nuke.filename(node), int(node['first'].getValue()), int(node['last'].getValue()))
            subsection = subsection_images
            fileknob = node["file"]
        
        elif nclass == "Write":
            root = nuke.root()
            frame = int(node['frame'].getValue())
            first_frame = int(root['first_frame'].getValue())
            last_frame = int(root['last_frame'].getValue())
            
            if node["frame_mode"].getValue() == 0: # Expression
                first = first_frame
                last = last_frame
            
            elif node["frame_mode"].getValue() == 1: # Start at
                first = frame
                last = first_frame - last_frame + 1 + frame
        
            elif node["frame_mode"].getValue() == 2: # offset
                first = first_frame + frame
                last = last_frame + frame

            f = pdwFile(nuke.filename(node), first, last)
            subsection = subsection_images
            fileknob = node["file"]

        elif nclass == "ReadGeo2":
            f = pdwFile(nuke.filename(node))
            subsection = subsection_3dassets
            fileknob = node["file"]
        
        elif nclass == "Camera2":
            f = pdwFile(nuke.filename(node))
            subsection = subsection_3dassets
            fileknob = node["file"]
        
        elif nclass == "Vectorfield":
            f = pdwFile(node['vfield_file'].getValue())
            subsection = subsection_luts
            fileknob = node['vfield_file']
    except:
        pass
    
    
    if f and subsection:
        lastPath =  node.name()
        
        sys.stdout.write("Copy %s: " % node.name())
        
        newF, copystate = f.copyTo(os.path.join(dstPath, section, subsection, lastPath))
        
        if newF:
            fileknob.setValue(os.path.join("..", section,subsection, lastPath, newF.FileName))
        else:
            pass
        
        return "Copy %s: %s" % (node.name(), copystate)
        
    #else:
    #    return "%s has not Fileknob" % node.name()

class pdwFile():
    File = ""
    Path = ""
    FileName = ""
    FirstFrame = -1
    LastFrame = -1
    
    def __init__(self, file, firstframe = -1, lastframe = -1):
        self.File = file
        self.Path, self.FileName = os.path.split(self.File)
        self.FirstFrame = firstframe
        self.LastFrame = lastframe
        self.Handles = 0
    
    def __normalisedFilename(self):
        first = self.FileName.find("#")
        last = self.FileName.rfind("#")
        
        if (first < 0) or (last < 0):
            return self.FileName
        else:
            return "%s%%0%dd%s" % (self.FileName[:first] , last-first+1 ,self.FileName[last+1:])
    
    def __copy(self, srcFile, dstFile):
        isCopied = -1 # -1 = Error, 0 = File(s) does not exist,  1 = Done, 2 = Exist
        doCopy = False
        
        
        dstPath, dump = os.path.split(dstFile)
        
        if not os.path.exists(srcFile):
            return 0

        if self.isAbsolut() == True:
            if os.path.exists(dstFile):
                if (os.path.getsize(srcFile) != os.path.getsize(dstFile)) or (os.path.getmtime(srcFile)>os.path.getmtime(dstFile)):
                    doCopy = True
                else: 
                    return 2 
            else:
                doCopy = True
        
        
        if doCopy:
            try:
                os.makedirs(dstPath)
            except:
                pass
            try:
                shutil.copy(srcFile, dstFile)
                return 1
            except:
                return -1
                
        return isCopied
    
    def isSequence(self):
        
        if (self.FileName.find("%")>0) or (self.FileName.find("#")>0):
            return True
        else:
            return False
        
    def isAbsolut(self):
        if self.Path.find("..") == -1:
            return True
        else:
            return False


    def copyTo(self, dstPath):
        copystate = ""
        isCopied = -1

        if self.isSequence():        
            File = self.__normalisedFilename()
            
    
            for i in range(self.FirstFrame, self.LastFrame+1):
                curFileName = File % i
                srcFile = os.path.join(self.Path, curFileName)
                dstFile = os.path.join(dstPath, curFileName)
                
                isCopied = self.__copy(srcFile, dstFile)
        else:
            isCopied = self.__copy(self.File, os.path.join(dstPath, self.FileName))
        
        if isCopied == 0:
            copystate =  "Source File(s) does not exist"
        elif isCopied == 1:
            copystate =  "Done"
        elif isCopied == 2:
            copystate =  "Destination File(s) already exist"
        elif isCopied == -1:
            copystate =  "Unrecognized Error"
        
        if isCopied > 0:
            return pdwFile(os.path.join(dstPath, self.FileName), self.FirstFrame, self.LastFrame), copystate
        else:
            return None, copystate

def assembleScript(dstPath=None):
    
    log = ""
    
    if not dstPath:
        dstPath = nuke.getFilename("Select Destination Path")
    
    
    
    addLogLine(log, "--[ Und Los! ]--")
    
    # copy Files
    
    # Selected Outs
    for node in nuke.selectedNodes():
        if node.Class() == "Write":
            log = addLogLine(log, copyNodeFileTo(node, dstPath, "outs"))
    
    
    # Reads
    for node in nuke.allNodes():
        if node.Class() != "Write":
            log = addLogLine(log, copyNodeFileTo(node, dstPath, "source"))
    
    for group in nuke.allNodes('Group'):
        with group:
            for node in nuke.allNodes():
                if node.Class() != "Write":
                    log = addLogLine(log, copyNodeFileTo(node, dstPath, "source"))
    

    # Save Script
    nr = nuke.root()
    
    nr["project_directory"].setValue("[python {nuke.script_directory()}]")
    
    scriptpath, scriptname = os.path.split(nr["name"].getValue())
    
    if scriptname =="":
        scriptname = "shotscript_v01.nk"
    
    try:
        os.makedirs(os.path.join(dstPath, "setup"))
    except:
        pass
    
    nuke.scriptSaveAs(os.path.join(dstPath, "setup", scriptname) )
    
    # Fettig
    
    log = addLogLine(log, "--[ fin ]--")
    
    nuke.message(log)


