# ORDINAMENTO PER TIPO E PER NOME ASCENDENTE
# se si vuole decrescente porre reverse=True alla linea 57
# crea i gruppi se non esistono
# conta quanti layer ha scansionato e di quale tipo
# ricordarsi che è un ordinamento alfabetico !!
# python 3  - Giulio Fattori - 30.01.2020

import datetime
current_time = datetime.datetime.now()
print ("Time now at greenwich meridian is :" , current_time)

root = QgsProject.instance().layerTreeRoot()
layers = QgsProject.instance().mapLayers()

count_point = 0
count_line = 0
count_poly = 0
count_table = 0
count_raster = 0


if root.findGroup("Group Point") is None:
            g_poi= root.insertGroup(0, "Group Point")
if root.findGroup("Group Line") is None:
            g_lin=root.insertGroup(1, "Group Line")
if root.findGroup("Group Polygon") is None:
            g_pol=root.insertGroup(2, "Group Polygon")
if root.findGroup("Group Table") is None:
            g_tab=root.insertGroup(3, "Group Table")
if root.findGroup("Group Raster") is None:
            g_ras=root.insertGroup(4, "Group Raster")
 
wkbtype_point = (1,1001,2001,3001,-2147483647,4,1004,2004,3004)
wkbtype_line  = (2,1002,2002,3002,-2147483646,5,1005,2005,3005)
wkbtype_poly  = (3,1003,2003,3003,-2147483645,6,1006,2006,3006)
wkbtype_table = (0,100)

for layer in layers.values():
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
        if layer.wkbType() in wkbtype_table:
            root.findGroup("Group Table").insertChildNode(4, myClone)
            count_table += 1
    if layer.type() is QgsMapLayerType.RasterLayer:
            root.findGroup("Group Raster").insertChildNode(5, myClone)
            count_raster += 1
            
    parent.removeChildNode(myblayer)
    

for child in root.children():
    if isinstance(child, QgsLayerTreeGroup):
        lyrList = [c.layer() for c in child.children()]
        lyrSortList = sorted(lyrList, key=lambda x: x.name(),reverse=False)
        for idx, lyr in enumerate(lyrSortList):
            treeLyr = child.insertLayer(idx, lyr)
        child.removeChildren(len(lyrList),len(lyrList))

if count_point == 0:
    root.removeChildNode(g_poi)
else:
    g_poi.setExpanded(False)
if count_line == 0:
    root.removeChildNode(g_lin)
else:
    g_lin.setExpanded(False)
if count_poly == 0:
    root.removeChildNode(g_pol)
else:
    g_pol.setExpanded(False)
if count_table == 0:
    root.removeChildNode(g_tab)
else:
    g_tab.setExpanded(False)
if count_raster == 0:
    root.removeChildNode(g_ras)
else:
    g_ras.setExpanded(False) 

print ("Point  layer n : ", count_point)
print ("Line   layer n : ", count_line)
print ("Poly   layer n : ", count_poly)
print ("Table  layer n : ", count_table)
print ("Raster layer n : ", count_raster)
print ("Total  layer n : ", count_point+count_line+count_poly+count_table+count_raster)

current_time = datetime.datetime.now() - current_time
print ("Time elaboration elapsed :" , current_time)

msg = QMessageBox()
msgtext=  f'Elaboration time   {current_time}'
msg.setText(msgtext)
msg.setWindowTitle ("Sei stato avvertito!!")
string= f'Point\tlayer n :\t{count_point}'
string= string + f'\nLine\tlayer n :\t{count_line}'
string= string + f'\nPoly\tlayer n :\t{count_poly}'
string= string + f'\nTable\tlayer n :\t{count_table}'
string= string + f'\nRaster\tlayer n :\t{count_raster}'
totale = count_point+count_line+count_poly+count_table+count_raster
string= string + f'\n\nTotal\tlayer n :\t{totale}'
msg.setDetailedText(string)
msg.setIcon(QMessageBox.Warning)
msg.exec()