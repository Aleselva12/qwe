# CodeAtlas

**Branch Cora.** Per riprendere il progetto da un’altra conversazione, leggere [Memoria e decisioni Cora](docs/MEMORIA_CORA.md) e la [pianta parziale](cora-plan.json).

Mappa locale del programma: **capacità utili verso l’utente, processi che le realizzano e requisiti alla base**. Sei schemi navigabili, dettagli espandibili e schede modificabili. CodeAtlas è indipendente da Serveria e non modifica né esegue il progetto analizzato.

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

- All'inizio è aperta la capacità complessiva proposta, con i processi principali e le basi. Clic o Invio su un nodo apre la scheda ed espande/richiude i sottopunti. La ricerca rende visibili anche i risultati nascosti con i loro antenati.
- L’albero si legge dall’alto: **capacità utile → processi → requisiti**. I file e le dichiarazioni si esplorano come dettagli della realizzazione. Una calcolatrice rimane una capacità complessiva anche quando implementa quattro operazioni aritmetiche.
- La proposta iniziale contiene una capacità con il nome del progetto, ricavato dal README o dalla cartella. Non deduce automaticamente gli obiettivi degli utenti. Puoi rinominarla, separare altre capacità e modificare ruoli e associazioni nelle schede. L’hardware si inserisce manualmente: non viene indovinato.
- Layout deterministico, collegamenti curvi, evidenza del nodo selezionato; rotella o **+ / −** per zoom, trascinamento dello sfondo e **Centra**. **Panoramica** richiude i dettagli. Le etichette si adattano allo spazio per non accavallarsi: avvicinati con lo zoom o usa ricerca/vista testuale per leggere i dettagli. Nessun limite al numero dei nodi visibili imposto dal layout.
- Colori per classificazione, mai per certificare test passati. Linee continue per gerarchia; tratteggiate per dipendenze statiche/proposte o dichiarate. Non vengono inventate connessioni per riempire il disegno.
- La scheda contiene cosa fa, scopo, futuro, problemi, dipendenze, sottopunti e timeline individuale. Le note iniziali derivano da docstring quando disponibili, altrimenti sono proposte esplicitamente incerte.
- **Modifica classificazione e scheda** permette di cambiare nome, categoria, genitore, descrizioni, problemi e dipendenze. **Aggiorna scheda** aggiorna il dettaglio visibile. Per dipendenze usa gli ID dei nodi mostrati nelle evidenze. **+ Nodo** crea anche radici manuali per hardware, modelli e servizi non rilevati.
- **Evidenze tecniche e limiti** mantiene i riferimenti ai file e gli errori di scansione in secondo piano. La **Vista testuale** offre una navigazione equivalente senza il grafo.

Le correzioni vengono conservate nel localStorage del browser, separatamente per percorso assoluto. Ricaricare la pagina conserva anche il progetto selezionato finché il server rimane acceso. Riscansionare rigenera le proposte e mantiene le correzioni manuali, aggiornando i riferimenti dei nodi ancora rilevati. **Esporta mappa** crea una copia portabile; **Importa** la ripristina dopo aver aperto il progetto. Il salvataggio nel browser non è un database condiviso e cancellare i dati del browser lo elimina. Cambiare porta/browser richiede reimportare la copia.

## Punti di vista sul progetto

Il selettore **Schema** offre **sei rappresentazioni: Albero funzionale più cinque alternative**. La vista testuale rimane disponibile.

| Vista | Domanda a cui risponde |
| --- | --- |
| Albero funzionale | Come si appoggia l’utilità del programma su processi e requisiti? |
| Grafo delle dipendenze | Quali componenti dipendono da quali altri, anche fra rami diversi? |
| Dipendenze a livelli | Quali catene di dipendenze e quali cicli collegano i componenti? |
| Matrice delle dipendenze (DSM) | Quali coppie di componenti sono accoppiate? Riga = origine, colonna = destinazione. |
| Struttura dei file | Dove sono cartelle, file e dichiarazioni rilevate? A quali elementi della mappa sono associati? |
| Flusso di supporto | Come si collegano basi, realizzazione e utilità, da sinistra a destra? |

Grafo, livelli e matrice proiettano la stessa mappa editabile, con gli stessi filtri, nodi selezionati, schede e sottopunti espandibili. Usano solo relazioni `depends_on`: una relazione generica `related_to` o `supports` non diventa una dipendenza. Le frecce vanno dal componente dipendente alla dipendenza. Il clic su una linea o una cella mostra le relazioni originali e la provenienza.

Chiudendo un ramo, le dipendenze verso altri rami vengono aggregate sul primo antenato visibile; quelle interamente interne al ramo chiuso non vengono mostrate. Il numero in una cella conta le relazioni della mappa, non le chiamate a runtime. Espandi i sottopunti per analizzare i dettagli. La ricerca può nascondere gli estremi di una relazione: non è una prova di indipendenza. Nessun nodo corrispondente viene troncato deliberatamente.

La vista a livelli raggruppa i cicli prima di calcolare i livelli; il dettaglio dei nodi coinvolti riporta **Ciclo**. La struttura fisica ha una propria espansione e permette di tornare all’albero dalle responsabilità associate al file o simbolo. Questa vista è un inventario dei soli file supportati.

Albero, grafo, livelli e flusso condividono zoom, trascinamento, evidenza della selezione e stile scuro a punti luminosi. **Centra** ripristina l’inquadratura; **Panoramica** richiude i dettagli mantenendo aperta la capacità complessiva. La struttura fisica è un albero grafico con espansione indipendente e scorrimento; la matrice si scorre come tabella. L’esportazione salva il modello comune, senza duplicarlo per ogni vista.

Nel **Flusso di supporto** le frecce delle dipendenze sono lette nel verso opposto: dal requisito verso il componente che se ne serve. Le associazioni gerarchiche arrivano alla capacità. Nel grafo e nei livelli le frecce mantengono invece il verso `dipendente → dipendenza`. Il dettaglio di un collegamento conserva sempre le evidenze originali; la gerarchia prova soltanto l’appartenenza proposta o dichiarata, non l’esecuzione di un percorso.

**Limite deliberato:** non sono diagrammi di sequenza, flowchart del controllo o diagrammi entità-relazioni. Per questi servono dati su chiamate, condizioni, eventi e schema del database che l’analizzatore attuale non ricostruisce. Le dipendenze statiche non dimostrano l’ordine di esecuzione.

## Personalizzare per altri progetti

**Profili** permette di cambiare nome del profilo, vista iniziale, etichette e colori delle categorie e campi delle schede. Le categorie di base possono essere rinominate; categorie aggiuntive sono ammesse. I campi sono testo libero (es. responsabile, priorità). Nell’area avanzata si definiscono nodi/obiettivi, regole sui percorsi e associazioni test. **Importa profilo** accetta configurazioni preparate da un assistente IA. Ogni applicazione presenta un’anteprima e conserva la mappa precedente per il ripristino. Nessuna configurazione esegue comandi.

Le proposte IA, le euristiche e le dichiarazioni dell’utente restano distinte. Lo stato del nodo è dichiarato, non certificato dai test. **Esporta mappa** include personalizzazioni, profilo e storico delle verifiche; **Esporta profilo** salva la sola configurazione riutilizzabile. Il salvataggio è locale al browser/percorso; esportare per condividere e prima di cancellare i dati del browser.

Esempio: [profilo team](examples/team-profile.json). Guida e contratto per Claude/altri assistenti: [AI_CUSTOMIZATION.md](docs/AI_CUSTOMIZATION.md).

## Test collegati alla mappa

**Verifiche** elenca file di test e configurazioni individuate e importa JUnit XML o un report JSON CodeAtlas esportato. Il risultato può essere scaricato da una CI; CodeAtlas non si collega autonomamente alla CI e non autentica i report. Si possono dichiarare commit, ambiente, data di esecuzione e assenza di modifiche locali. Se mancano o non coincidono, l’incertezza è esplicita.

Ogni caso mostra esito, messaggio e nodi associati. **Associa** collega un test a un nodo; i selettori del profilo permettono associazioni ripetibili, manuali o proposte IA. La scheda del nodo mostra i risultati collegati, mantenendo separate le esecuzioni storiche. Una corrispondenza per percorso è un legame al file del test, non una misura di copertura. Nessun nodo diventa automaticamente “verificato”.

Sono conservati fino a 20 report distinti, con esportazione/rimozione e confronto degli esiti dei casi comuni fra report dello stesso nome e ambiente. Lo storico è ordinato per importazione. I primi 200 casi di ogni report sono elencati nel pannello per limitarne il peso; tutti sono conservati e conteggiati. Per casi successivi usare i selettori nel profilo. Limite import file: 10 MB; lo spazio effettivo del browser può essere inferiore. Un errore di salvataggio durante l’applicazione mantiene la mappa corrente.

La CLI `--junit risultati.xml` produce risultati dello stesso formato, visibili anche nella UI. Il file [test-run.xml](examples/test-run.xml) è soltanto una fixture didattica.

**Nessuna esecuzione dei test del progetto:** CodeAtlas resta in sola lettura. Node/npm sono richiesti solo per sviluppare e verificare CodeAtlas, non per avviarlo con Python.

## Provenienza e limiti

La classificazione usa regole trasparenti su nomi, percorsi e dichiarazioni: non comprende semanticamente ogni progetto. Le aree sconosciute restano **da collocare**, senza inventare funzioni. Gli scopi e gli obiettivi futuri restano da definire dall'utente. Le docstring sono dichiarazioni dell'autore, non prove di comportamento. Una modifica manuale viene indicata come tale.

Python usa AST per dichiarazioni e import; JavaScript/TypeScript usa euristiche conservative, non un compilatore completo. Manifest infrastrutturali sono inventariati, hardware/versioni runtime/modelli installati non vengono verificati. Import relativi/dinamici possono rimanere irrisolti. Go, Rust, Java, C#, C/C++, Ruby, PHP, Swift, Kotlin, SQL, HTML/CSS, Vue e Svelte sono inventariati a livello file, senza parser semantico dedicato. I sottopunti generati dai nomi delle dichiarazioni richiedono revisione umana e possono essere riorganizzati.

La timeline mostra al massimo otto commit pertinenti fra gli ultimi quindici letti, più le modifiche annotate alla scheda. Riporta messaggi dei commit, non sintesi semantiche di versioni precedenti. Non è un confronto storico completo. I test trovati nel progetto non vengono eseguiti e non provano che funzioni. Nessun LLM o integrazione Graphify/Backstage/LikeC4 è incluso.

L'API Python e le opzioni CLI per overlay, impatto, snapshot e JUnit rimangono disponibili (`python -m codeatlas.app --help`). Le vecchie viste frammentate di import, confronto e ricerca tecnica sono state sostituite dalla mappa; confronto e impatto avanzati restano nella CLI; i risultati JUnit hanno ora un pannello Verifiche e collegamenti alle schede.

## Verifica

```sh
python -m unittest discover -s tests -v
python -m compileall -q codeatlas tests
npm ci --ignore-scripts
npm test
```

Il collaudo browser opzionale è riproducibile con `python tests/browser_smoke.py` dopo aver installato Playwright e Chromium (istruzioni nello script). Non sono dipendenze del programma. La CI conserva screenshot e risultati come artifact.

Per distribuire una prova, includi anche [LEGGIMI - Per iniziare.txt](LEGGIMI%20-%20Per%20iniziare.txt).

Vedi [VALIDATION.md](VALIDATION.md) per esiti effettivi, prove browser e lavoro ancora da fare. Nessuna dichiarazione di affidabilità su grandi monorepo senza un benchmark separato.

## Riferimenti progettuali

- [Backstage: catalog graph](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/): componenti e risorse distinti; generazione iniziale con manutenzione umana.
- [LikeC4: views](https://likec4.dev/dsl/views/): modello architetturale separato dalle sue viste, esplorazione a diversi livelli.
- Graphify: riferimento discusso dall'utente per il grafo tecnico come evidenza. Non è stato scelto né installato un adapter: più progetti condividono questo nome.
- Immagini CORA fornite nella conversazione: riferimento visivo per sfondo scuro, punti e collegamenti. Nessuna immagine di riferimento è redistribuita.

Nessuna licenza concessa al momento: definirla prima di distribuire codice di terzi o invitare al riuso pubblico.
