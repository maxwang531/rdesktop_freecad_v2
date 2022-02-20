import csv
import numpy as np
import pandas as pd
from pandas import DataFrame,Series
from scipy.spatial import KDTree
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Base, Rotation, Vector

SsdNetfile = '/config/eingabe_model/csv_file/demo3.csv'
freeCADfile = '/config/eingabe_model/csv_file/Modelldaten-demo3.csv'
resultfile = '/config/eingabe_model/csv_file/Result-demo3.csv'
filepath_original = '/config/eingabe_model/demo3.FCStd'
Modellange= 35

#Model open
DOC=App.openDocument(filepath_original)
DOC.recompute()
DOC = App.activeDocument()
DOC.recompute()
obj = App.ActiveDocument.getObject('Part__Feature')
x_min = obj.Shape.BoundBox.XMin
y_min = obj.Shape.BoundBox.YMin
z_min = obj.Shape.BoundBox.ZMin


#Daten von SsdNet
corpusData = pd.read_csv(SsdNetfile) # 得到 DataFrame
corpus = corpusData.values.tolist()#会读取所有csv的数据为列表
corpus0 = corpus[0]#会读取第一个列表数据
x=corpusData.shape[1] #列数 从0开始，总列数-1
y=corpusData.shape[0] #行数 从0开始，总行数-1
print("Daten von SSdNet:",corpusData)

#Daten ausgeben in list
Type = corpusData.iloc[0:y,7].values.tolist()
xmin = corpusData.iloc[0:y,1].values.tolist()
xmin = [i +x_min for i in xmin]
xmax = corpusData.iloc[0:y,4].values.tolist()
xmax = [i +x_min for i in xmax]
ymin = corpusData.iloc[0:y,2].values.tolist()
ymin = [i +y_min for i in ymin]
ymax = corpusData.iloc[0:y,5].values.tolist()
ymax = [i +y_min for i in ymax]
zmin = corpusData.iloc[0:y,3].values.tolist()
zmin = [i +z_min for i in zmin]
zmax = corpusData.iloc[0:y,6].values.tolist()
zmax = [i +z_min for i in zmax]

#Daten Bearbeitung
xminnp = np.array(xmin)
xmaxnp = np.array(xmax)
yminnp = np.array(ymin)
ymaxnp = np.array(ymax)
zminnp = np.array(zmin)
zmaxnp = np.array(zmax)
#print(xmaxnp)

#bottom
bottomX = (xminnp+xmaxnp)/2
bottomX = bottomX.tolist()#转化为列表
bottomY = (yminnp+ymaxnp)/2
bottomY = bottomY.tolist()
bottomZ = zmin
#print(bottomX,bottomY,bottomZ)

#top
topX = bottomX
topY = bottomY
topZ = zmax
#print(topX,topY,topZ)

#site1
site1X = xmin
site1Y = bottomY
site1Z = (zminnp+zmaxnp)/2
site1Z = site1Z.tolist()

#site2
site2X = bottomX
site2Y = ymax
site2Z = site1Z

#site3
site3X = xmax
site3Y = bottomY
site3Z = site1Z

#site4
site4X = bottomX
site4Y = ymin
site4Z = site1Z


#DataFrame from SSD(type and centermass from each site-bottom,top,site1234)
data = {'Type':Series(Type),'bottomX':Series(bottomX),'bottomY':Series(bottomY),'bottomZ':Series(bottomZ),'topX':Series(topX),'topY':Series(topY),'topZ':Series(topZ),'site1X':Series(site1X),'site1Y':Series(site1Y),'site1Z':Series(site1Z),'site2X':Series(site2X),'site2Y':Series(site2Y),'site2Z':Series(site2Z),'site3X':Series(site3X),'site3Y':Series(site3Y),'site3Z':Series(site3Z),'site4X':Series(site4X),'site4Y':Series(site4Y),'site4Z':Series(site4Z)}
df = DataFrame(data) #DataFrame erstellen
#print(xmin,xmax)
#print(Type)
print("DataFrame von SSD:",df)

# Face and masscenter from FreeCAD
corpusData2 = pd.read_csv(freeCADfile) # 得到 DataFrame
s = corpusData2.shape[0]
#Daten Bearebeitung
Face= corpusData2.iloc[0:s,1].values.tolist()
koorX = corpusData2.iloc[0:s,2].values.tolist()
koorY = corpusData2.iloc[0:s,3].values.tolist()
koorZ = corpusData2.iloc[0:s,4].values.tolist()

data2 = {'Face':Series(Face), 'koorX':Series(koorX), 'koorY':Series(koorY), 'koorZ':Series(koorZ)}
df2 = DataFrame(data2)
#print(corpusData2)
print("Face and centermass from FreeCAD",df2)

#find the nearst point
NDIM = 3

#df2 Bearbeitung
p = df2.shape[0]
df2point = df2.iloc[0:p,1:4].values.tolist()
df2pointnp = np.array(df2point) #read point into array
#print(df2point)
#print(df2pointnp)


#df Bearbeitung 选择预测面上需要匹配的点
q = df.shape[0]
bottompoint = df.iloc[0:q,1:4].values.tolist() #只匹配了bottomXYZ
print(bottompoint)
toppoint = df.iloc[0:q,4:7].values.tolist()
#print(toppoint)
site1point = df.iloc[0:q,7:10].values.tolist()
site2point = df.iloc[0:q,10:13].values.tolist()
site3point = df.iloc[0:q,13:16].values.tolist()
site4point = df.iloc[0:q,16:19].values.tolist()

#KDTree匹配,最短点
tree = KDTree(df2pointnp, leafsize=df2pointnp.shape[0]+1)
distances, ndxbottom = tree.query([bottompoint], k=1) #k表示要找几个点，这里匹配bottom
distances, ndxtop = tree.query([toppoint], k=1)
distances, ndxsite1 = tree.query([site1point], k=1)
distances, ndxsite2 = tree.query([site2point], k=1)
distances, ndxsite3 = tree.query([site3point], k=1)
distances, ndxsite4 = tree.query([site4point], k=1)
print (df2pointnp[ndxbottom])
#print(type(df2pointnp[ndx]))
#print(ndxbottom)#ndx可能是输出数组
#print(type(ndxbottom))
bottom = (ndxbottom[0]+1).tolist()
print(ndxbottom)
print(bottom)
#print(df2pointnp[ndx][0][0][0])#会一层一层的读取数组内数据
top = (ndxtop[0]+1).tolist()
site1 = (ndxsite1[0]+1).tolist()
site2 = (ndxsite2[0]+1).tolist()
site3 = (ndxsite3[0]+1).tolist()
site4 = (ndxsite4[0]+1).tolist()

'''
aa = ndx[0].tolist()# ndx作为一个numpy数组存在一个列表，[0]也就是读取这个列表，然后把这个numpy格式的数组转化为列表
print(aa)
data3 = {'Face':Series(aa) }
df3 = DataFrame(data3)# 新建了第三个DataFrame
print(df3)
'''

# Result
data3 = {'Type':Series(Type),'Bottom':Series(bottom),'Top':Series(top),'Site1':Series(site1),'Site2':Series(site2),'Site3':Series(site3),'Site4':Series(site4)}
result = DataFrame(data3)
result.to_csv(resultfile)
print("result",result)
print(result.at[0,'Type'])#打印对应行列处的数值

Gui.doCommand('exit()')






