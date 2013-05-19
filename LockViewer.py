# LockViewer 1.0
# locks a viewer to a selected node.
# Description:
# > LockViewer locks a selected node to a choosen viewer (1-10).
# > Pressing the same viewer number on a different node results
# > in showing up the 'locked' node.
# Usage:
# > select one node and choose a viewer(1-10) to lock to from the custom Nuke-Menu
# Installation:
# > save the script in your Nuke Plugin path
# > and add the following line to your menu.py
# > nuke.load('X:/----path----/-to-/-plugin-/LockViewer.py')
# > don't forget to setup the custom menu_name, see line 19
#
# scripted by Marc Gutowski
# website:    www.ewok1.com
# last update 14.02.2011 / v1.0

menu_name = "RG"

import nuke
menubar = nuke.menu("Nuke");
m = menubar.addMenu(menu_name)
msub = m.addMenu("Lock Selected Node to Viewer")
msub.addCommand("1","LockViewer1()")
msub.addCommand("2","LockViewer2()")
msub.addCommand("3 (Original Plate)","LockViewer3()")
msub.addCommand("4 (Out)","LockViewer4()")
msub.addCommand("5 (Last Render)","LockViewer5()")
msub.addCommand("6 (Ref)","LockViewer6()")
msub.addCommand("7","LockViewer7()")
msub.addCommand("8","LockViewer8()")
msub.addCommand("9","LockViewer9()")
msub.addCommand("10","LockViewer10()")

#Viewerbuffer are offsetted in Nuke by 1 -> for example: viewer1=0, viewer2=1, viewer3=2
#	line to edit - nuke.activeViewer().node().setInput(0, nuke.toNode(selectednodename)) // setInput(#VIEWERNR, ...

def LockViewer1():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer1():
		nuke.activeViewer().node().setInput(0, nuke.toNode(selectednodename))
	def callbackLockThisViewer1():
		nuke.addKnobChanged(LockThisViewer1,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer1()

def LockViewer2():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer2():
		nuke.activeViewer().node().setInput(1, nuke.toNode(selectednodename))
	def callbackLockThisViewer2():
		nuke.addKnobChanged(LockThisViewer2,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer2()

def LockViewer3():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer3():
		nuke.activeViewer().node().setInput(2, nuke.toNode(selectednodename))
	def callbackLockThisViewer3():
		nuke.addKnobChanged(LockThisViewer3,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer3()

def LockViewer4():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer4():
		nuke.activeViewer().node().setInput(3, nuke.toNode(selectednodename))
	def callbackLockThisViewer4():
		nuke.addKnobChanged(LockThisViewer4,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer4()
		
def LockViewer5():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer5():
		nuke.activeViewer().node().setInput(4, nuke.toNode(selectednodename))
	def callbackLockThisViewer5():
		nuke.addKnobChanged(LockThisViewer5,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer5()
		
def LockViewer6():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer6():
		nuke.activeViewer().node().setInput(5, nuke.toNode(selectednodename))
	def callbackLockThisViewer6():
		nuke.addKnobChanged(LockThisViewer6,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer6()
		
def LockViewer7():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer7():
		nuke.activeViewer().node().setInput(6, nuke.toNode(selectednodename))
	def callbackLockThisViewer7():
		nuke.addKnobChanged(LockThisViewer7,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer7()
		
def LockViewer8():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer8():
		nuke.activeViewer().node().setInput(7, nuke.toNode(selectednodename))
	def callbackLockThisViewer8():
		nuke.addKnobChanged(LockThisViewer8,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer8()
		
def LockViewer9():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer9():
		nuke.activeViewer().node().setInput(8, nuke.toNode(selectednodename))
	def callbackLockThisViewer9():
		nuke.addKnobChanged(LockThisViewer9,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer9()
		
def LockViewer10():
	selectednodename = nuke.selectedNode().name()
	def LockThisViewer10():
		nuke.activeViewer().node().setInput(9, nuke.toNode(selectednodename))
	def callbackLockThisViewer10():
		nuke.addKnobChanged(LockThisViewer10,nodeClass='Viewer')
	if __name__ == '__main__':
		callbackLockThisViewer10()