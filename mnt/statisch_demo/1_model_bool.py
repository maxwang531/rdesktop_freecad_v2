#FreeCAD import
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Base, Rotation, Vector
import Part
import Path
import Draft
import Mesh

filepath_original = '/config/eingabe_model/demo3.FCStd'
filename = 'demo3'
Modellange= 35

DOC=App.openDocument(filepath_original)
DOC.recompute()
DOC = App.activeDocument()
DOC.recompute()
obj = App.ActiveDocument.getObject('Part__Feature')
xmin = obj.Shape.BoundBox.XMin
ymin = obj.Shape.BoundBox.YMin
zmin = obj.Shape.BoundBox.ZMin

box0 = DOC.addObject('Part::Box', 'Box')
box0.Width = Modellange
box0.Length = Modellange
box0.Height = Modellange

Vec = Base.Vector
pos=Vec(xmin,ymin,zmin)
rot=FreeCAD.Rotation(Vec(0,0,1),0)
center=Vec(0,0,0)
box0.Placement=FreeCAD.Placement(pos,rot,center)

cut = DOC.addObject('Part::Common', 'Common')
cut.Base = obj
cut.Tool = box0

DOC.recompute()

__objs__=[]
__objs__.append(App.getDocument(filename).getObject("Common"))
Mesh.export(__objs__,u"/config/eingabe_model/bool_model/Common.stl")
del __objs__
DOC.recompute()

App.getDocument(filename).saveAs(u"/config/eingabe_model/bool_model/Common.FCStd")
DOC.recompute()

Gui.doCommand('exit()')