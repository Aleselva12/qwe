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
