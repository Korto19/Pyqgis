#Recupera per il layer selezionato il colore assegnato dalla
#categorizzazione e lo salva in un csv nella bin di oswgeo
#python 3 su QgisDev 10.04.2019 Giulio Fattori

layer = iface.activeLayer()
renderer=layer.renderer()
#print (layer.name())
filepath = os.path.dirname( unicode( qgis.utils.iface.activeLayer().dataProvider().dataSourceUri()));
filepath = filepath + '/' + layer.name()
print (filepath)

msg = QMessageBox()
msg.setText('Salva in un csv nella directory del layer gli RGB - RGBA della categorizzazione')
msg.setWindowTitle ("AVVERTENZE SUL FUNZIONAMENTO DELLO SCRIPT!")
string= f'Salva il colore assegnato dalla categorizzazione al layer selezionato in un'
string= string + f'\file csv con i valori RGB o RGBA dei colori.'
string= string + f'\nSe utilizzate una tematizzazione da campo calcolato'
string= string + f'\nes: "left(CAMPO,2)" con CAMPO = "Siracusa" che restituisce "Si"'
string= string + f'\nè opportuno creare un campo virtuale con nome altrimenti l''algoritmo fallisce'
string= string + f'\nPotete ripeterlo su n campi'
msg.setDetailedText(string)
msg.setIcon(QMessageBox.Warning)
#msg.setIcon(QMessageBox.Critical)
msg.exec()


csv_color = "Cat_Value\tCat_Name\tColor\n"
for cat in renderer.categories():
    csv_color = csv_color + str(cat.value()) +"\t"+ str(cat.label()) + "\t" + str(cat.symbol().symbolLayer(0).properties()['color'])+"\n"
print (csv_color)

path_absolute = filepath + "_"+ renderer.legendClassificationAttribute() + "_RGBA.csv"
#print (path_absolute)
output_file = open(path_absolute, 'w')
 
output_file.write(csv_color)
output_file.close()

iface.messageBar().pushMessage("Fatto e salvato in ", path_absolute, level=Qgis.Info, duration=10)