# Adattare CodeAtlas con un assistente IA

CodeAtlas legge un progetto senza eseguirlo. Per personalizzarlo non occorre modificare il motore: produrre un profilo JSON da importare in **Profili**, esaminarne l’anteprima e applicarlo. Un fork/branch è utile per modificare il programma; non serve per modificare la configurazione.

## Procedura per Claude o altri assistenti

1. Leggere README, questo documento e `examples/team-profile.json`.
2. Chiedere all’utente il progetto di riferimento, le categorie utili e gli obiettivi. Leggere il codice disponibile prima di dichiarare che qualcosa è implementato.
3. Preparare un profilo schema v1. Conservare ID stabili. Separare proposte (`source: ai_suggestion`, `status: idea/planned`) da codice trovato. Non assegnare `verified` in base a import, nomi dei file o intenzioni.
4. Associare file con `code_refs` esatti dell’inventario oppure regole `path_glob`. Le regole aggiungono riferimenti: non spostano file, non cancellano gli altri raggruppamenti e non certificano la funzione.
5. Collegare test tramite selettori esatti; una proposta IA resta indicata come tale. Non inventare risultati di test, SHA di commit, date o ambienti.
6. Consegnare il profilo. L’utente apre la cartella in CodeAtlas, importa il profilo, controlla l’anteprima e applica. **Esporta mappa** crea un backup completo, comprensivo di risultati. **Ripristina precedente** recupera l’ultima mappa prima di un’importazione/applicazione.

## Contratto del profilo

- `schema_version`: 1. Le versioni sconosciute vengono rifiutate.
- `name`: nome non vuoto; `default_view`: `graph` (predefinita), `text`, `network`, `layers`, `matrix`, `files`.
- `categories`: `{id, label, color}`. ID semplici minuscoli; colore `#RRGGBB`. Le quattro categorie stabili `roots`, `trunk`, `branches`, `unassigned` restano disponibili per i nodi generati, ma etichette e colori possono cambiare. Altre categorie sono ammesse. L’ordine delle categorie non è un editor libero delle coordinate.
- `fields`: `{id, label}`. Campi di testo nella scheda, salvati nel nodo sotto `custom_fields`.
- `nodes`: nodi aggiunti/aggiornati per ID. Obbligatori `id`, `name`, `source` (`manual`/`ai_suggestion`), `status`. `lens` indica una categoria. `parent` è null o un ID esistente; cicli e riferimenti sconosciuti sono rifiutati nell’anteprima. `code_refs` contiene ID come `file:src/client.py`.
- `rules`: `{path_glob, group_id}`. Percorsi relativi POSIX. `*` non attraversa `/`; `**` attraversa anche directory. Solo file presenti nell’inventario. Nessuna espressione JavaScript, shell, regex arbitraria o download.
- `test_links`: `{group_id, name?, classname?, file?, source}`. Almeno un selettore non vuoto, confronto esatto dei selettori non vuoti (AND); nessuna euristica sul nome della funzionalità. Due casi con lo stesso nome/classe/file condividono l’associazione. La UI consente di creare associazioni manuali; il profilo permette di cambiarle/rimuoverle.

Un profilo **aggiunge o aggiorna** i nodi elencati; rimuovere un nodo dalla lista del profilo non elimina un nodo già presente nella mappa. Per sostituire l’intero modello si importa una mappa completa con anteprima. Regole e nodi del profilo vengono applicati quando si applica il profilo; dopo una nuova scansione si può riapplicarlo per includere nuovi file corrispondenti. La sola esportazione del profilo non esporta tutte le modifiche manuali alle schede: usare **Esporta mappa** per questo.

## Verifiche

Importare JUnit XML in **Verifiche**, o un singolo report JSON precedentemente esportato. Il file può provenire da CI, ma non viene scaricato né autenticato automaticamente da CodeAtlas. Metadati opzionali del report JUnit: proprietà alla radice `commit`, `environment`, `workspace_clean` (`true`/`false`), attributo `timestamp`. Si possono dichiarare anche nella schermata di importazione. Il commit non viene riempito con quello attuale per evitare di attribuire un vecchio test a nuovo codice.

Esiti: pass/fail/skip per caso; errore/failure → fail. Un file vuoto di casi non è una verifica positiva. SHA, ambiente e data importati sono dichiarazioni. Commit diverso → versione diversa; SHA mancante → non verificabile; modifiche locali non escluse → incertezza esplicita. Il confronto Git riguarda la scansione effettuata, non osserva in tempo reale modifiche successive o file ignorati da Git.

La corrispondenza fra `testcase.file` e un riferimento del nodo identifica il file del test: **non misura copertura**. I rapporti non aggiornano gli stati dichiarati dei nodi. Le associazioni mancanti restano visibili. Storico massimo 20 report per progetto, deduplicato per contenuto XML/ID JSON; esportare prima di rimuovere. L’ordine dello storico è di importazione e non viene spacciato per ordine di esecuzione.

## Modificare il programma

- Motore: `codeatlas/`; UI: `index.html`, `workbench.js`; proiezioni: `views.js`; profili: `profiles.js`; evidenze: `evidence.js`.
- Una nuova vista deve leggere il modello comune, preservare ID/provenienza e dichiarare i limiti; aggiungerla al selettore, al profilo e ai test.
- Un nuovo analizzatore deve limitarsi alla lettura statica. Non importare/eseguire codice del progetto per scoprirne l’architettura.
- Validare i cambiamenti: `python -m unittest discover -s tests -v`, `python -m compileall -q codeatlas tests`, `npm ci --ignore-scripts`, `npm test` (Node 24.15+ solo per sviluppo). Verificare visivamente l’interfaccia quando un browser è disponibile.
- Nessuna migrazione silenziosa di schemi sconosciuti. Aggiungere test per compatibilità dei vecchi export, import non validi, ripristino e separazione fra evidenze e proposte.

Il sistema non contiene ancora plugin eseguibili, esecuzione automatica dei test, import di coverage o sincronizzazione diretta con CI.

## Posizione funzionale e sei schemi

Il campo opzionale `role` di un nodo distingue `capability` (capacità utile),
`process` (realizzazione) e `foundation` (base/requisito). È indipendente da
`lens`, che continua a scegliere la categoria e il colore del profilo. Un nome
di funzione del sorgente non equivale a una capacità utile: una calcolatrice
può avere una capacità complessiva e quattro operazioni interne. L'assenza
di `role` mantiene la compatibilità con le mappe precedenti.

`default_view` accetta anche `flow`: mostra basi → processi → capacità.
Gli altri schemi sono `graph`, `network`, `layers`, `matrix`, `files`; `text`
resta un ausilio aggiuntivo. Le frecce di `flow` leggono le dipendenze nel verso
del supporto; evidenze originali e associazioni di appartenenza restano distinte.
