#Recupera il colore assegnato dalla categorizzazione al layer selezionato
#aggiunge un campo COLOR e salva i valori dei colori
#python 3 10.04.2019 Giulio Fattori

import datetime
current_time = datetime.datetime.now()

layer = iface.activeLayer()
renderer=layer.renderer()

if layer.renderer().type() == "categorizedSymbol":
    matrix = {}
    campo=renderer.legendClassificationAttribute()

    for cat in renderer.categories():
        matrix[cat.value()] = cat.symbol().symbolLayer(0).properties()['color']

    layer.startEditing()
    if layer.fields().indexFromName('COLOR') == -1:
        layer.addAttribute(QgsField("COLOR", QVariant.String))
    for feat in layer.getFeatures():
        layer.changeAttributeValue(feat.id(),layer.fields().indexFromName('COLOR'),matrix[str(feat[campo])])
    layer.commitChanges()

    current_time = str(datetime.datetime.now() - current_time)
    iface.messageBar().pushMessage("Elaborazione terminata in  ", current_time, level=Qgis.Info, duration=5)
    iface.messageBar().pushMessage("I COLORI SONO SALVATI IN UNA NUOVA COLONNA DENOMINATA ", "COLOR", level=Qgis.Warning, duration=5)

elif layer.renderer().type() != "categorizedSymbol":
    current_time = str(datetime.datetime.now() - current_time)
    iface.messageBar().pushMessage("NON E' UN LAYER CATEGORIZZATO - Elaborazione terminata in  ", current_time, level=Qgis.Critical, duration=5)
