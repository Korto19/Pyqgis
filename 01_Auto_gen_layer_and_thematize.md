Questo script, partendo da un layer tematizzato in funzione di un campo (tipo 'A_1958') selezionato, produce tanti layer quanti sono i campi della tabella dati che han identico prefisso nel nome.
Recupera automaticamente il campo di tematizzazione e considera 2 lettere di prefisso
Per esempio se il campo della tematizzazione è 'A_1958' consegue che tutti i campi che iniziano con 'A_' verranno utilizzati
per creare n layer tematizzati.
Per la composizione di stampa occorre eseguire successivamente `02_Auto_composer_ multiple_map_layout.py`
* `MultiMap.gpkg` FILE DI ESEMPIO
