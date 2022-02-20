#FreeCAD import
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Base, Rotation, Vector
import Part
import Path
import Draft
import Mesh
filepath_original = '/config/eingabe_model/vorfuhrung_2.FCStd'

DOC=App.openDocument(filepath_original)
DOC.recompute()
DOC = App.activeDocument()
DOC.recompute()
obj = App.ActiveDocument.getObject('VORFUHRUNG')

box0 = DOC.addObject('Part::Box', 'Box')
box0.Width = 40
box0.Length = 40
box0.Height = 40

cut = DOC.addObject('Part::Common', 'Common')
cut.Base = obj
cut.Tool = box0

DOC.recompute()

__objs__=[]
__objs__.append(App.getDocument("vorfuhrung_2").getObject("Common"))
Mesh.export(__objs__,u"/config/eingabe_model/bool_model/Common.stl")
del __objs__
DOC.recompute()

App.getDocument("vorfuhrung_2").saveAs(u"/config/eingabe_model/bool_model/Common.FCStd")
DOC.recompute()

Gui.doCommand('exit()')