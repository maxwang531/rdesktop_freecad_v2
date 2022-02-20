#FreeCAD import
import FreeCAD as App
import FreeCADGui as Gui
import Part

FreeCAD.loadFile("/config/eingabe_model/demo3.stp")
App.getDocument("Unnamed").saveAs(u"/config/eingabe_model/demo3.FCStd")
Gui.doCommand('exit()')




