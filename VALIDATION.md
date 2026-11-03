# Verifica del redesign — 3 novembre 2026

## Risultati eseguiti

- Recuperati codice e storia della repository `Aleselva12/qwe`, branch `main`.
- Prima delle modifiche: 18 test esistenti superati.
- Dopo le modifiche: 22 test superati su Windows / Python 3.13. Compilazione Python superata.
- Nuovi test: classificazione deterministica compatibile con schema, sottopunti e runtime, nessuna intenzione inventata, cartelle vuote/sconosciute, import relativi Python e sottopunti TypeScript, nessuna scrittura nella cartella analizzata, flusso HTTP desktop con token/origine, apertura, GET successivo, percorso errato senza perdere il report precedente.
- Browser reale, server `python -m codeatlas.desktop`: apertura di qwe dal campo percorso senza JSON; costellazione iniziale; espansione Analisi e classificazione; scheda destra con dipendenze e commit pertinenti; modifica della categoria a Tronco; vista testuale; ricaricamento con correzione preservata; modifica dello scopo e verifica dopo un ulteriore ricaricamento.
- Il collaudo ha trovato e corretto due difetti: report desktop perso tra richieste, e SVG che nascondeva i pulsanti all'accessibilità. Corretto anche il salvataggio dei campi durante l'editing e l'altezza della mappa nelle finestre strette.

## Limiti residui

- La classificazione è una proposta basata su convenzioni e nomi, non ricostruzione semantica dell'architettura. Le aree generiche devono essere rinominate e riorganizzate.
- Scopo, evoluzione e problemi non possono essere ricostruiti attendibilmente senza dichiarazioni umane. Il programma li rende editabili e li mantiene distinti dalle evidenze.
- Sottopunti da dichiarazioni, non ancora una classificazione semantica autonoma delle sottofunzioni.
- Cronologia limitata ai commit recenti associati ai riferimenti; nessun confronto semantico fra revisioni.
- Nessun adapter Graphify, parser completo JS/TS, tracciamento runtime o rilevamento hardware.
- Persistenza locale al browser e al percorso, esportazione manuale per backup; nessun database multiutente.
- Avvio mediante launcher richiede Python; non è un eseguibile installabile autonomo. Collaudato il modulo chiamato dal launcher, non un doppio clic fisico sul file batch.
- Il collaudo browser è manuale assistito, non una suite browser automatizzata in CI. Non certificati i tre benchmark Click/full-stack/Dify né macOS/Linux.
- Il repository analizzato durante il collaudo è qwe. Serveria non è stato aperto, eseguito o modificato.

La suite CI esistente continua a eseguire i test unitari e la compilazione. L'esito remoto va controllato sul commit pubblicato; non è sostituibile con l'esito locale.

## Viste complementari — 3 novembre 2026

- Albero principale predefinito preservato; aggiunti grafo orientato, livelli di dipendenza con cicli, matrice DSM e struttura fisica con ritorno alle responsabilità.
- 23 test Python superati su Linux, inclusa distribuzione HTTP di `views.js` dal launcher desktop; compilazione Python superata.
- 4 test Node superati: aggregazione delle dipendenze dei figli senza mutare il modello, esclusione delle relazioni non `depends_on`, cicli/self-loop/isolati, catena di 5.000 nodi senza ricorsione e parsing dello script UI. Controlli Node aggiunti alla CI.
- Collaudo DOM con jsdom: rendering delle sei viste, selezione del nodo, scheda comune, ispezione di una relazione, file e ritorno all’albero, ricerca senza risultati e mappa vuota. Tutti superati. È un controllo funzionale DOM, non una verifica grafica.
- Verifica visiva in un browser reale **non completata**: Chromium assente nell’ambiente; download Playwright non valido. Nessuna certificazione del layout desktop/mobile per queste nuove viste.
- Matrice quadratica rispetto ai nodi visibili; grafo a disposizione circolare deterministica, non force-directed Graphify. Nessun benchmark su grandi monorepo. I cicli interni ai rami chiusi si vedono espandendoli.

## Profili universali e verifiche associate — 3 novembre 2026

- Profili v1: categorie/etichette/colori, campi delle schede, vista iniziale, nodi proposti, regole glob e associazioni test. Anteprima con dettagli prima/dopo, applicazione atomica rispetto alla quota del browser, ripristino della mappa precedente, esportazione e persistenza per progetto.
- JUnit XML e singoli report JSON: esiti, messaggi, metadati dichiarati, versione Git della scansione e incertezza, storico di 20 report, deduplicazione, confronto dei casi comuni, collegamenti manuali/IA e corrispondenze dei percorsi distinti dalla copertura.
- Inventario a livello file per ulteriori linguaggi, senza fingere di disporre dei relativi parser; rilevazione aggiuntiva di configurazioni e convenzioni test.
- **26 test Python + 13 test Node/DOM superati**; compilazione Python e `git diff --check` superati. CI aggiornata per installare soltanto le dipendenze di sviluppo e controllare profili, risultati e UI.
- Test DOM automatici: anteprima senza mutazione, nuova categoria e campi, conservazione dopo una scansione, ripristino, parsing JUnit, associazione e scheda, deduplicazione, mappe corrotte e quota del browser esaurita. Aggiunti alla suite, non solo eseguiti manualmente.
- HTTP desktop: tutti e quattro gli asset JavaScript serviti correttamente. CLI reale `--junit` sulla demo: HTML, quattro script e report HTTP 200; caricamento delle risorse con jsdom e risultati della fixture visibili nel pannello Verifiche.
- Fixture XML ed esempio profilo sono didattici; non rappresentano un progetto realmente verificato.
- Resta non effettuata la verifica visiva tramite browser grafico. jsdom verifica comportamento/DOM, non geometria, colori o rendering mobile.
- Limiti: nessuna esecuzione dei test del progetto, autenticazione CI, import coverage o plugin eseguibili. Associazioni esplicite/percorso, non deduzione semantica della copertura. Persistenza soggetta alla quota del browser; le applicazioni che eccedono la quota non sostituiscono la mappa corrente. Primi 200 casi elencati per report; tutti conteggiati e conservati. Nessun benchmark su monorepo molto grandi.
