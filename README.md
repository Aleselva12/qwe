# CodeAtlas

Mappa locale dei componenti di un programma: costellazione 2D nera, classificazione semiautomatica in **radici, tronco e rami**, sottopunti espandibili e scheda individuale a destra. CodeAtlas è indipendente da Serveria e non modifica né esegue il progetto analizzato.

## Avvio

Richiede Python 3.10+ e Git solo per leggere la cronologia. Nessun pacchetto Python aggiuntivo, account o modello necessario.

1. Scarica/clona questa repository.
2. Su Windows fai doppio clic su **Avvia CodeAtlas.bat**.
3. Nel browser inserisci il percorso completo della cartella e premi **Apri progetto**.
4. Appare subito la mappa proposta; non occorre preparare o importare JSON.

Il percorso è quello del computer che esegue CodeAtlas; il selettore è un campo testuale, non una finestra nativa. Su macOS/Linux: `python3 -m codeatlas.desktop`. Il file `.command` richiede il permesso di esecuzione su macOS.

Alternativa da terminale:

```sh
python -m codeatlas.app /percorso/progetto
```

Il server ascolta solo su `127.0.0.1:8765`. Chiudi la sua finestra o premi Ctrl+C per terminarlo. Se la porta è occupata: `python -m codeatlas.desktop --port 8766`.

## Esplorazione

- All'inizio compaiono solo i componenti principali. Clic o Invio su un nodo apre la scheda ed espande/richiude i sottopunti. La ricerca rende visibili anche i risultati nascosti con i loro antenati.
- Layout automatico deterministico con separazione delle posizioni; rotella per zoom, trascinamento dello sfondo e **Centra**. Nessun limite arbitrario che nasconda parte dei nodi.
- Colori per classificazione, mai per certificare test passati. Linee continue per gerarchia; tratteggiate per dipendenze statiche/proposte o dichiarate. Non vengono inventate connessioni per riempire il disegno.
- La scheda contiene cosa fa, scopo, futuro, problemi, dipendenze, sottopunti e timeline individuale. Le note iniziali derivano da docstring quando disponibili, altrimenti sono proposte esplicitamente incerte.
- **Modifica classificazione e scheda** permette di cambiare nome, categoria, genitore, descrizioni, problemi e dipendenze. **Aggiorna scheda** aggiorna il dettaglio visibile. Per dipendenze usa gli ID dei nodi mostrati nelle evidenze. **+ Nodo** crea anche radici manuali per hardware, modelli e servizi non rilevati.
- **Evidenze tecniche e limiti** mantiene i riferimenti ai file e gli errori di scansione in secondo piano. La **Vista testuale** offre una navigazione equivalente senza il grafo.

Le correzioni vengono conservate nel localStorage del browser, separatamente per percorso assoluto. Ricaricare la pagina conserva anche il progetto selezionato finché il server rimane acceso. Riscansionare rigenera le proposte e mantiene le correzioni manuali, aggiornando i riferimenti dei nodi ancora rilevati. **Esporta mappa** crea una copia portabile; **Importa** la ripristina dopo aver aperto il progetto. Il salvataggio nel browser non è un database condiviso e cancellare i dati del browser lo elimina. Cambiare porta/browser richiede reimportare la copia.

## Punti di vista sul progetto

Il selettore **Punto di vista** affianca all’**Albero principale**, sempre iniziale, quattro rappresentazioni classiche. La vista testuale rimane disponibile.

| Vista | Domanda a cui risponde |
| --- | --- |
| Grafo delle dipendenze | Quali componenti dipendono da quali altri, anche fra rami diversi? |
| Dipendenze a livelli | Quali catene di dipendenze e quali cicli collegano i componenti? |
| Matrice delle dipendenze (DSM) | Quali coppie di componenti sono accoppiate? Riga = origine, colonna = destinazione. |
| Struttura dei file | Dove sono cartelle, file e dichiarazioni rilevate? A quali responsabilità sono associati? |

Grafo, livelli e matrice proiettano la stessa mappa editabile, con gli stessi filtri, nodi selezionati, schede e sottopunti espandibili. Usano solo relazioni `depends_on`: una relazione generica `related_to` o `supports` non diventa una dipendenza. Le frecce vanno dal componente dipendente alla dipendenza. Il clic su una linea o una cella mostra le relazioni originali e la provenienza.

Chiudendo un ramo, le dipendenze verso altri rami vengono aggregate sul primo antenato visibile; quelle interamente interne al ramo chiuso non vengono mostrate. Il numero in una cella conta le relazioni della mappa, non le chiamate a runtime. Espandi i sottopunti per analizzare i dettagli. La ricerca può nascondere gli estremi di una relazione: non è una prova di indipendenza. Nessun nodo corrispondente viene troncato deliberatamente.

La vista a livelli raggruppa i cicli prima di calcolare i livelli; i nodi coinvolti sono marcati **Ciclo**. La struttura fisica ha una propria espansione e permette di tornare all’albero dalle responsabilità associate al file o simbolo. Questa vista è un inventario dei soli file supportati.

Le viste grafiche alternative si scorrono; **Centra** adatta il disegno alla finestra. Albero e vista testuale mantengono il comportamento precedente. L’esportazione salva il modello comune, senza duplicarlo per ogni vista.

**Limite deliberato:** non sono diagrammi di sequenza, flowchart del controllo o diagrammi entità-relazioni. Per questi servono dati su chiamate, condizioni, eventi e schema del database che l’analizzatore attuale non ricostruisce. Le dipendenze statiche non dimostrano l’ordine di esecuzione.

## Provenienza e limiti

La classificazione usa regole trasparenti su nomi, percorsi e dichiarazioni: non comprende semanticamente ogni progetto. Le aree sconosciute restano **da classificare**, senza inventare funzioni. Gli scopi e gli obiettivi futuri restano da definire dall'utente. Le docstring sono dichiarazioni dell'autore, non prove di comportamento. Una modifica manuale viene indicata come tale.

Python usa AST per dichiarazioni e import; JavaScript/TypeScript usa euristiche conservative, non un compilatore completo. Manifest infrastrutturali sono inventariati, hardware/versioni runtime/modelli installati non vengono verificati. Import relativi/dinamici possono rimanere irrisolti. HTML/CSS e altri linguaggi non sono ancora inventariati. I sottopunti generati dai nomi delle dichiarazioni richiedono revisione umana e possono essere riorganizzati.

La timeline mostra al massimo otto commit pertinenti fra gli ultimi quindici letti, più le modifiche annotate alla scheda. Riporta messaggi dei commit, non sintesi semantiche di versioni precedenti. Non è un confronto storico completo. I test trovati nel progetto non vengono eseguiti e non provano che funzioni. Nessun LLM o integrazione Graphify/Backstage/LikeC4 è incluso.

L'API Python e le opzioni CLI per overlay, impatto, snapshot e JUnit rimangono disponibili (`python -m codeatlas.app --help`). Le vecchie viste frammentate di import, confronto e ricerca tecnica sono state sostituite dalla mappa; questi risultati avanzati non hanno ancora un pannello dedicato nella nuova UI.

## Verifica

```sh
python -m unittest discover -s tests -v
python -m compileall -q codeatlas tests
node --test tests/test_views.cjs
```

Vedi [VALIDATION.md](VALIDATION.md) per esiti effettivi, prove browser e lavoro ancora da fare. Nessuna dichiarazione di affidabilità su grandi monorepo senza un benchmark separato.

## Riferimenti progettuali

- [Backstage: catalog graph](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/): componenti e risorse distinti; generazione iniziale con manutenzione umana.
- [LikeC4: views](https://likec4.dev/dsl/views/): modello architetturale separato dalle sue viste, esplorazione a diversi livelli.
- Graphify: riferimento discusso dall'utente per il grafo tecnico come evidenza. Non è stato scelto né installato un adapter: più progetti condividono questo nome.
- Immagini CORA fornite nella conversazione: riferimento visivo per sfondo scuro, punti e collegamenti. Nessuna immagine di riferimento è redistribuita.

Nessuna licenza concessa al momento: definirla prima di distribuire codice di terzi o invitare al riuso pubblico.
