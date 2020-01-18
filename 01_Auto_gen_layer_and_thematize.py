#Sulla base delle impostazioni di un layer categorizzato
#ne produce una versione per ogni campo dati che abbia il
#medesimo prefisso Es: 'A_1958' > prefisso 2 lettere 'A_' 
#da cui tutti i campi con nome del tipo 'A_****' produrranno 
#un layer tematizzato in funzione del campo 'A_****'

import datetime
start = datetime.datetime.now()
layer = iface.activeLayer()
prefix_lenght = 2              #1. inserire lunghezza prefisso del campo

# funzione di conversione da RGBA a HEX
def RGBA_HEX (string_rgba):
    x=string_rgba.split(',')
    return  '#%02x%02x%02x' % (int(x[0]),int(x[1]),int(x[2]))
    
# define a lookup: value -> (color, label)    
#print('00 ' + layer.name())
renderer = layer.renderer()
if layer.renderer().type() == "categorizedSymbol":
    scale_col = {}
    # recupera il campo di tematizzazione e ne estrae il prefisso
    layer_prefix = renderer.legendClassificationAttribute()[0:prefix_lenght]
#    print('pp '+ layer_prefix)
    #crea il dizionario dei colori'
    for cat in renderer.categories():
        if str(cat.value()) != '':

            index_m = str(cat.value())
        else:
            index_m = 'none'
        if layer.geometryType() == 0 or layer.geometryType() == 2:
            
            scale_col[index_m] = RGBA_HEX(cat.symbol().symbolLayer(0).properties()['color']),index_m
        else:
            scale_col[index_m] = RGBA_HEX(cat.symbol().symbolLayer(0).properties()['line_color']),index_m
#print(scale_col)
    
for field in layer.fields():
    start_l = datetime.datetime.now()
    if layer_prefix in field.name():
#        print('#'+field.name())
       
        for feature in layer.getFeatures():
            categories = []
            for feature[field.name()],(color, label) in scale_col.items():
#                print('00 '+field.name(),color, label)
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
        
        
# parte opzionale per messaggio ad ogni elaborazione, utile se molti dati
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
        QgsProject.instance().layerTreeRoot().findLayer(lyr1_clone).setExpanded(False)
        print('Layer ' +lyr1_clone.name() + ' time elaboration ' + str(elapsed_l))
        
# parte opzionale per messaggio ad ogni elaborazione, utile se molti dati
#        if ret == QMessageBox.Close: break

print('Total Time elapsed ' + str(datetime.datetime.now() - start))