# ORDINAMENTO PER TIPO E PER NOME ASCENDENTE
# se si vuone decrescente porre reverse=True alla linea 57
# crea i gruppi se non esistono
# conta quanti layer ha scansionato e di quale tipo
# ricordarsi che è un ordinamento alfabetico !!
# python 3  - Giulio Fattori - 02.04.2019

import datetime
current_time = datetime.datetime.now()
print ("Time now at greenwich meridian is :" , current_time)

root = QgsProject.instance().layerTreeRoot()
layers = iface.mapCanvas().layers()

count_point = 0
count_line = 0
count_poly = 0
count_raster = 0

if root.findGroup("Group Point") is None:
            g_poi= root.insertGroup(0, "Group Point")
if root.findGroup("Group Line") is None:
            g_lin=root.insertGroup(1, "Group Line")
if root.findGroup("Group Polygon") is None:
            g_pol=root.insertGroup(2, "Group Polygon")
if root.findGroup("Group Raster") is None:
            g_ras=root.insertGroup(3, "Group Raster")
 
wkbtype_point = (1,1001,2001,3001,-2147483647,4,1004,2004,3004)
wkbtype_line  = (2,1002,2002,3002,-2147483646,5,1005,2005,3005)
wkbtype_poly  = (3,1003,2003,3003,-2147483645,6,1006,2006,3006)

activeLayer = iface.activeLayer()

for layer in layers:
    myblayer = root.findLayer(layer.id())
    myClone = myblayer.clone()
    parent = myblayer.parent()
    if layer.type() is QgsMapLayerType.VectorLayer:
        if layer.wkbType()in wkbtype_point:
            root.findGroup("Group Point").insertChildNode(1, myClone)
            count_point += 1
        if layer.wkbType()in wkbtype_line:
            root.findGroup("Group Line").insertChildNode(2, myClone)
            count_line += 1
        if layer.wkbType() in wkbtype_poly:
            root.findGroup("Group Polygon").insertChildNode(3, myClone)
            count_poly += 1
    if layer.type() is QgsMapLayerType.RasterLayer:
            root.findGroup("Group Raster").insertChildNode(4, myClone)
            count_raster += 1
    parent.removeChildNode(myblayer)

for child in root.children():
    if isinstance(child, QgsLayerTreeGroup):
        lyrList = [c.layer() for c in child.children()]
        lyrSortList = sorted(lyrList, key=lambda x: x.name(),reverse=False)
        for idx, lyr in enumerate(lyrSortList):
            treeLyr = child.insertLayer(idx, lyr)
        child.removeChildren(len(lyrList),len(lyrList))

g_poi.setExpanded(False)
g_lin.setExpanded(False)
g_pol.setExpanded(False)
g_ras.setExpanded(False)

print ("Point  layer n : ", count_point)
print ("Line   layer n : ", count_line)
print ("Poly   layer n : ", count_poly)
print ("Raster layer n : ", count_raster)
print ("Total  layer n : ", count_point+count_line+count_poly+count_raster)

current_time = datetime.datetime.now() - current_time
print ("Time elaboration elapsed :" , current_time)