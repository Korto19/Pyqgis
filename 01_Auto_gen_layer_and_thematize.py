import datetime

start = datetime.datetime.now()
layer = iface.activeLayer()
layer_prefix ='A_'                #1. inserire quello che occorre

# define a lookup: value -> (random color, label)
scale_col = {
    '0': ("#f7fbff", '0'),
    '1': ("#e4eff9", '1'),
    '2': ("#d1e3f3", '2'),
    '3': ("#bad6eb", '3'),
    '4': ("#9ac8e1", '4'),
    '5': ("#73b3d8", '5'),
    '6': ("#529dcc", '6'),
    '7': ("#3585c0", '7'),
    '8': ("#1c6cb1", '8'),
    '9': ("#08519c", '4'),
    '':("#08306b",''),
    }
    
for field in layer.fields():
    start_l = datetime.datetime.now()
    if layer_prefix in field.name():
        print(field.name())
       
        for feature in layer.getFeatures():
            categories = []
            for feature[field.name()],(color, label) in scale_col.items():
                symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                symbol.setColor(QColor(color))
                category = QgsRendererCategory(feature[field.name()], symbol, label)
                categories.append(category)
            
        #create and assign the renderer to the layer
        lyr1_clone = QgsVectorLayer(layer.source(), field.name(), layer.providerType())
        QgsProject.instance().addMapLayer(lyr1_clone, False)
        treeRoot = QgsProject.instance().layerTreeRoot()
        treeRoot.insertChildNode(-1, QgsLayerTreeLayer(lyr1_clone))
        
        # create the renderer
        expression = field.name() # field name
        renderer = QgsCategorizedSymbolRenderer(field.name(), categories)
        lyr1_clone.setRenderer(renderer)
        lyr1_clone.triggerRepaint()
        
            
#        msg = QMessageBox()
        elapsed_l = datetime.datetime.now() - start_l
#        msgtext=  f'{field.name()}\n{elapsed}'
#        msg.setGeometry(1500, 800, 200, 200)
#        msg.setText(msgtext)
#        msg.setWindowTitle ("Done!!")
#        msg.setIcon(QMessageBox.Warning)
#        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Close)
#        ret = msg.exec()
        
        """ spegne layer"""
        QgsProject.instance().layerTreeRoot().findLayer(lyr1_clone).setItemVisibilityChecked(False)
        print(elapsed_l)
#        print('u ' + str(ret))
#        if ret == QMessageBox.Close: break
print(datetime.datetime.now() - start)