"""Crea il Layout nel progetto"""
project = QgsProject.instance()             #gets a reference to the project instance
manager = project.layoutManager()           #gets a reference to the layout manager
layout = QgsPrintLayout(project)            #makes a new print layout object, takes a QgsProject as argument
layoutName = "PrintLayout"

"""Imposta il numero di colonne e righe e dimensioni in mm"""
"""scala di rappresemtazione e prefisso campo da cui tematizzare"""
""" modificare opportunamente 1,2,3"""
col = 4                     #1. numero di righe che si vogliono
rig = 2                     #2. numero di colonne che si vogliono
xm = 280/col
ym = 200/rig
#m_scala =10000000.0
layer_prefix = "A_"       #3. prefisso dei campi in cui risiedono i dati

layer_name = []
for layer in QgsProject.instance().mapLayers().values():
    if layer_prefix in layer.name():
        layer_name.append(layer.name()) 
print(layer_name)

"""Rimuove il layout se già presente"""
layouts_list = manager.printLayouts()
for layout in layouts_list:
    if layout.name() == layoutName:
        manager.removeLayout(layout)
        
layout = QgsPrintLayout(project)
layout.initializeDefaults()                 #create default map canvas
layout.setName(layoutName)
manager.addLayout(layout)

'''Imposto il contatore di anni in questo caso'''
count = 0

for r in range (rig):
    for c in range(col):
        """Aggiunge la mappa nel layout"""
        map = QgsLayoutItemMap(layout)
        map.setRect(20, 20, 20, 20)
        #Set Extent
#        rectangle = QgsRectangle(1426622,4301323,1570192,4573617)         #an example of how to set map extent with coordinates
#        map.setExtent(rectangle)
        canvas = iface.mapCanvas()
        map.setExtent(canvas.extent()) #sets map extent to current map canvas
#        map.setScale(m_scala)
        map.setId(layer_name[count])
        print('i '+ map.id())
        layout.addLayoutItem(map)
        #Move & Resize
        map.attemptMove(QgsLayoutPoint(5+xm*c, 5+ym*r, QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(xm, ym, QgsUnitTypes.LayoutMillimeters))
        
        """seleziona e blocca il layer sulla mappa"""
        print('2 '+ map.id())
        layer_set = QgsProject.instance().mapLayersByName(map.id())[0]
        map.setLayers([layer_set])
        map.setKeepLayerSet(True)
        map.setKeepLayerStyles(True)
        
        """Aggiunge il titolo alla mappa"""
        title = QgsLayoutItemLabel(layout)
        title.setText('Anno ' + map.id().replace(layer_prefix,''))
        title.setFont(QFont("Arial", 8))
        title.adjustSizeToText()
        layout.addLayoutItem(title)
        title.attemptMove(QgsLayoutPoint(5+xm*c, 5+ym*r, QgsUnitTypes.LayoutMillimeters))
        
        count += 1