import csv
from typing import List

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

#FreeCAD import
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Base, Rotation, Vector
import Part
import Path
import Draft
from PathScripts import PathJob
from PathScripts import PathJobGui


from PathScripts import PathAdaptive

import PathScripts.PathDressupDogbone as PathDressupDogbone
import PathScripts.PathDressupHoldingTags as PathDressupHoldingTags
from PathScripts import PathGeom
from PathScripts import PathPostProcessor
from PathScripts import PathUtil

from PathScripts import PathToolBit
from PathScripts import PathToolController
modell_länge = 35

filepath_original = '/config/eingabe_model/demo3.FCStd'
file_name_1 = 'demo3'
file_name_2 = 'Part__Feature'
toolpath1 = "/usr/lib/freecad/Mod/Path/Tools/Bit/157mm_Endmill.fctb"
toolpath2 = "/usr/lib/freecad/Mod/Path/Tools/Bit/157mm_Ball_End.fctb"
gcodePath_top = '/config/ausgabe_ngc/txt/top_operation.txt'

#打开真正的模型文件
DOC=App.openDocument(filepath_original)
DOC.recompute()
DOC = App.activeDocument()
DOC.recompute()
obj = App.ActiveDocument.getObject(file_name_2)
face_anzahl_list = obj.Shape.Faces
#模型中心
xmin = obj.Shape.BoundBox.XMin
xmax = obj.Shape.BoundBox.XMax
ymin = obj.Shape.BoundBox.YMin
ymax = obj.Shape.BoundBox.YMax
zmin = obj.Shape.BoundBox.ZMin
zmax = obj.Shape.BoundBox.ZMax
centervector = ((xmin+xmax)/2,(ymin+ymax)/2,(zmin+zmax)/2)
print(centervector)

#在原始模型中各个面的坐标

Part1 = DOC.getObject(file_name_2)

#operation definition
def werkzeug(toolpath,name2,horizrapid = "15mm/s",vertrapid = "2mm/s",horizfeed="10mm/s",vertfeed ="10mm/s"):
    name1 = PathToolBit.Declaration(toolpath)

    tool = PathToolController.Create(name2)
    tool.setExpression('HorizRapid', None)
    tool.HorizRapid = horizrapid
    tool.setExpression('VertRapid', None)
    tool.VertRapid = vertrapid
    tool.setExpression('HorizFeed', None)
    tool.VertRapid = horizfeed
    tool.setExpression('VertFeed', None)
    tool.VertRapid = vertfeed



    name3 = tool.Tool
    name3.Label = name1['name']
    name3.BitShape = name1['shape']
    name3.CuttingEdgeHeight = name1['parameter']['CuttingEdgeHeight']
    name3.Diameter = name1['parameter']['Diameter']
    name3.Length = name1['parameter']['Length']
    name3.ShankDiameter = name1['parameter']['ShankDiameter']
    name3.recompute()
    name3.ViewObject.Visibility = True
    name3.recompute()
    return name3.Diameter

def adaptive_operation(facName, use_outline, werkzeugname, finishing_profile = 0,stepdown = 5,force_inside_out = 1,helixangle = 5,
                       helixconeangle = 0,helixdiameterlimit = 0, keeptooldownratio = 3,
                       liftdistance = 0 ,operation_type = 0, si_de = 0, stepover = 20 ,stocktoleave = 0,
                       tolerance = 0.1 ,use_helix_arcs = 1 , finishdepth = 0, name = 0):
    adaptive = PathAdaptive.Create('Adaptive%d'%(name))
    adaptive.Base = (Part1,facName)

    finishingprofile = ['true' , '']
    adaptive.FinishingProfile = bool(finishingprofile[finishing_profile])


    forceinsideout = ['true','']
    adaptive.ForceInsideOut = bool(forceinsideout[force_inside_out])

    adaptive.setExpression('HelixAngle',None)
    adaptive.HelixAngle = helixangle

    adaptive.setExpression('HelixConeAngle',None)
    adaptive.HelixConeAngle = helixconeangle

    adaptive.setExpression('HelixDiameterLimit',None)
    adaptive.HelixDiameterLimit = helixdiameterlimit

    adaptive.setExpression('KeepToolDownRatio',None)
    adaptive.KeepToolDownRatio = keeptooldownratio

    adaptive.setExpression('LiftDistance',None)
    adaptive.LiftDistance = liftdistance

    operationtype = ['Clearing','Profiling']
    adaptive.OperationType = operationtype[operation_type]

    side = ['Inside','Outside']
    adaptive.Side = side[si_de]

    adaptive.setExpression('StepOver',None)
    adaptive.StepOver = stepover

    adaptive.setExpression('StockToLeave',None)
    adaptive.StockToLeave = stocktoleave

    adaptive.setExpression('Tolerance',None)
    adaptive.Tolerance = tolerance

    usehelixarcs = ['true','']
    adaptive.UseHelixArcs = bool(usehelixarcs[use_helix_arcs])

    useoutline = ['true','']
    adaptive.UseOutline = bool(useoutline[use_outline])

    adaptive.setExpression('FinishDepth',None)
    adaptive.FinishDepth = finishdepth

    adaptive.setExpression('StepDown',None)
    adaptive.StepDown = stepdown

    Gui.Selection.addSelection(file_name_1, 'Adaptive%d'%(name))
    App.getDocument(file_name_1).getObject('Adaptive%d'%(name)).ToolController = App.getDocument(file_name_1).getObject(werkzeugname)

    DOC.recompute()


#Operation Bearbeitung
#Step1 top face bearbeitung
#Job erstellen
#Job creat
Gui.activateWorkbench("PathWorkbench") #Path Workbrench activate
job = PathJob.Create('Job_top', [Part1], None)
job.ViewObject.Proxy = PathJobGui.ViewProvider(job.ViewObject)

#operation about Stock
stock = job.Stock
stock.setExpression('ExtXneg',None)
stock.ExtXneg = 0.00
stock.setExpression('ExtXpos',None)
stock.ExtXpos = 0.00
stock.setExpression('ExtYneg',None)
stock.ExtYneg = 0.00
stock.setExpression('ExtYpos',None)
stock.ExtYpos = 0.00
stock.setExpression('ExtZneg',None)
stock.ExtZneg = 0.00
stock.setExpression('ExtZpos',None)
stock.ExtZpos = 0.00
#Werkzeug Aufladen
tool1_diameter = werkzeug(toolpath1, 'tool1') #3mm_endmill
tool2_diameter = werkzeug(toolpath2, 'tool2') #5mm_endmill
App.getDocument(file_name_1).getObject('ToolBit001').ShapeName = "endmill"
App.getDocument(file_name_1).getObject('ToolBit002').ShapeName = "ballend"
DOC.recompute()
werkzeuglist = ['tool1','tool2']

#Face Selection

import math
Gui.Selection.addSelection(file_name_1,file_name_2)
objs = Gui.Selection.getSelection()
_angTol_ = math.pi * 1e-9
faceid = []

for obj in objs:
    zmin = obj.Shape.BoundBox.ZMin
    zmax = obj.Shape.BoundBox.ZMax
    _disTol_ = max(1e-9 * max(abs(zmin), abs(zmax)), 0.0)
    for i, fac in enumerate(obj.Shape.Faces):
        facType = fac.Surface

        if not isinstance(facType, Part.Plane):
            continue
        facAxis = fac.Surface.Axis
        _ZVec_ = App.Vector(0, 0, 1)
        if abs(facAxis.getAngle(_ZVec_) % math.pi) > _angTol_:
            continue
        facPos = fac.Surface.Position.z
        if facPos <= zmin + _disTol_ or facPos >= zmax - _disTol_ or facPos == 20:
            continue
        if fac.Orientation == 'Reversed':
            #facName = 'Face{:d}'.format(i + 1)
            faceid.append(i)
        print(fac.Orientation)
print("gg",faceid)


for i in range(0, len(faceid)):
    facName = 'Face{:d}'.format(faceid[i] + 1)
    adaptive_operation(facName,0,werkzeuglist[0],0,name=i)



job.PostProcessorOutputFile = gcodePath_top
job.PostProcessor = 'linuxcnc'
job.PostProcessorArgs = '--no-show-editor'
postlist = []
currTool = None

for obj in job.Operations.Group:
    print( obj.Name)
    tc = PathUtil.toolControllerForOp(obj)
    if tc is not None:
        if tc.ToolNumber != currTool:
            postlist.append(tc)
            currTool = tc.ToolNumber
    postlist.append(obj)

post = PathPostProcessor.PostProcessor.load(job.PostProcessor)
gcode = post.export(postlist, gcodePath_top , job.PostProcessorArgs)
DOC.recompute()
print("--- done ---")
App.closeDocument(file_name_1)




Gui.doCommand('exit()')















