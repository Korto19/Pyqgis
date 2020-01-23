# TOC TABLE

## Cosa Fa
Recupera alcuni dati dei layer del progetto e ne popola una tabella utile per la documentazione del progetto

## Spiegazione campi

I campi della tabella prodotta contengono:

* `Layer_N`             numero progressivo attribuito al layer nella scansione della TOC
* `Layer_Group_Level`   struttura della toc in gruppi e sottogruppi
* `Layer_Name`          nome del layer
* `Geometry_Not_Valid`  numero di geometrie non valide
* `Layer_Crs`           epsg del layer
* `Layer_Type`          tipo di layer come da codifica QgsLayerType
* `Layer_Type_Name`     tipo di layer come da codifica QgsLayerTypeName
* `Layer_Source`        percorso di memorizzazione del layer (se su postgis o server remoti anche pwd fare attenzione)
* `Layer_Fetaure_Count` numero delle feature del layer (es numero di punti, linee, ecc)
* `Layer_Meta_ecc`      tutti i dati dalla prima schermata dei metadati dalle proprietà del layer
* `Layer_Group_Level`   struttura della canvas toc in gruppi e sottogruppi

agg. 24.12.2019
