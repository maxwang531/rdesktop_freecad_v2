#import sys
import sys

#FreeCAD import
from FreeCAD import Base, Rotation, Vector
from math import pi, sin, cos
import csv
import numpy as np
import pandas as pd
import FreeCAD as App
import FreeCADGui as Gui


filename = '/config/eingabe_model/bool_model/Common.FCStd'
csvfilename = '/config/eingabe_model/csv_file/Modelldaten-demo3.csv'

DOC=FreeCAD.openDocument(filename)
DOC.recompute()

DOC = FreeCAD.activeDocument()

DOC.recompute()


#obj = App.ActiveDocument.getObject('Part__Feature')
obj = App.ActiveDocument.getObject('Common') #TODO 需要注意的是对不是标准立方体的模型进行布尔运算后，选择的模型必须是布尔运算的名称，partfeature会选择原始模型

template  ='Face {}: CenterOfMass --> ({:.1f}, {:.1f}, {:.1f})' #format格式化函数，https://www.runoob.com/python/att-string-format.html，1f保留小数一位
list=[]
for i, face in enumerate(obj.Shape.Faces, start=1):
    centerofmass = face.CenterOfMass
    list.append([i, '%.1f' % centerofmass.x , '%.1f' % centerofmass.y , '%.1f' % centerofmass.z])
    #print(list)
    test2 = pd.DataFrame( data=list, columns=['Face','X','Y','Z'])
    test2.to_csv(csvfilename) 

Gui.doCommand('exit()')