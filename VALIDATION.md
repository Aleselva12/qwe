# Albero funzionale e sei viste — 3 novembre 2026

## Integrazione

Questa versione integra il branch `improve/constellation-preview` (`aaa34d1`)
e le quattro prospettive di `codex/project-perspectives` (`7da540c`), poi aggiornata
con `main` (`65d6a05`): profili portabili, evidenze e inventario esteso sono conservati.
L’albero cambia significato: capacità complessiva proposta in alto, realizzazione
intermedia, requisiti in basso. Dichiarazioni e file sono dettagli della realizzazione.
Non sono state aggiunte funzioni di pianificazione, account o stato multiutente.
I launcher conservano la distribuzione di tutti gli asset delle viste, dei profili e delle verifiche.
Categorie/colori dei profili e posizione funzionale dei nodi sono indipendenti.
La vista `flow` è valida anche come scelta iniziale portabile del profilo.

## Verifiche eseguite

Linux / Python 3.12 / Chromium reale headless, con Playwright.

- 31 test Python superati e 17 test JavaScript superati; compilazione Python e
  controllo degli spazi superati.
- Caso Calcolatrice: aggiungendo sottrazione, moltiplicazione e divisione alla
  sola addizione, rimane una capacità complessiva; le quattro operazioni
  restano dettagli interni. Nessun hardware dedotto o inventato.
- Test dei ruoli, compatibilità con overlay precedenti, direzione delle
  dipendenze e del supporto, evidenze originali, cicli, basi espanse e coordinate finite.
- Browser sui quattro progetti sotto: passaggio fra tutte e sei le viste,
  modello invariato durante il cambio, matrice, albero fisico con espansione
  separata, selezione ed espansione, ricerca, tastiera, rotella, pulsanti zoom,
  trascinamento, vista testuale, modifica e ricaricamento, import/export ripetuti,
  cartelle errate e vuote, nuovo nodo manuale.
- Screenshot e geometria controllati a 1440 × 900, 1024 × 768, 768 × 900 e
  390 × 844. Nei casi controllati, zero sovrapposizioni fra etichette mostrate,
  zero punti fuori dall’inquadratura iniziale, nessuno scorrimento orizzontale
  della pagina. Le viste fisica e matrice hanno il proprio scorrimento.
- Le etichette di dettaglio restano progressive con lo zoom. In espansione
  completa tutti i punti sono presenti, mentre molti nomi richiedono zoom,
  ricerca o vista testuale.

| Progetto | Punti nella panoramica | Nodi espansi | Etichette visibili nella panoramica | Errori scansione |
| --- | ---: | ---: | ---: | ---: |
| CodeAtlas modificato | 12 | 146 | 12 | 0 |
| Click | 8 | 1.134 | 8 | 0 |
| Full Stack FastAPI Template | 15 | 953 | 15 | 1 |
| Flask | 11 | 795 | 11 | 0 |

Le copie e revisioni dei benchmark sono le stesse documentate nel collaudo
precedente sotto. Il file `backend/app/api/deps.py` del template usa sintassi
non supportata da Python 3.12: errore segnalato, scansione di quel file parziale.
Le quantità di CodeAtlas possono cambiare aggiungendo i file di collaudo.

## Sei schemi

1. Albero funzionale: utilità sopra, processi nel mezzo, requisiti alla base.
2. Grafo delle dipendenze: dipendente → dipendenza.
3. Dipendenze a livelli: livelli statici con cicli conservati.
4. Matrice delle dipendenze: origine per riga e destinazione per colonna.
5. Struttura dei file: albero fisico grafico di cartelle, sorgenti e dichiarazioni.
6. Flusso di supporto: basi → processi → capacità utili.

La vista testuale è un ausilio aggiuntivo, non conta tra i sei schemi.
I collegamenti di appartenenza restano distinti dalle dipendenze e non dimostrano
l’ordine di esecuzione. La capacità iniziale è una proposta dal titolo del progetto,
non un’interpretazione semantica certificata. Può essere corretta e separata.

## Riproduzione e limiti

```sh
python -m unittest discover -s tests -v
npm ci --ignore-scripts
npm test
python -m compileall -q codeatlas tests
python tests/browser_smoke.py --chromium /usr/bin/chromium --output /tmp/codeatlas-six
```

Il browser test richiede Playwright; il programma resta senza dipendenze Python
aggiuntive. Ripetere `--benchmark /percorso/progetto` per le copie esterne.
Screenshot e risultati vengono salvati nella cartella indicata; la CI li carica
come artifact. L’esito remoto deve essere controllato sul commit pubblicato.
Windows/macOS e browser diversi da Chromium non collaudati in questa sessione.
Linguaggi supportati, import dinamici, cronologia limitata e persistenza browser
mantengono i limiti dichiarati nel README.

---

## Collaudo precedente (versione della costellazione)

# Collaudo della costellazione — 3 novembre 2026

## Ambiente e risultato

Collaudo effettivo in Linux, Python 3.12 e Chromium headless tramite Playwright.
Base analizzata: `b8deb32185209ede3ca7b07103be826b3c5e54a5`.

- Prima: 22 test Python superati. La vista completamente espansa sovrapponeva
  le etichette: 4 coppie su qwe, 8.673 su Click, 2.853 sul template full stack,
  2.600 su Flask, a 1440 × 900. Misura degli ingombri effettivi SVG nel browser.
- Dopo: 24 test Python superati; compilazione e `git diff --check` superati.
- Suite browser completata senza errori JavaScript sui quattro progetti.
- Controllati apertura dal percorso, responsabilità → file → dichiarazioni,
  selezione, ricerca, tastiera, zoom con rotella/pulsanti, trascinamento,
  ripristino dell'inquadratura, vista testuale, salvataggio e ricaricamento,
  esportazione e importazione ripetuta, cartella inesistente, cartella vuota,
  importazione su cartella vuota e creazione di un nodo manuale.
- Screenshot controllati nella panoramica, nell'esplorazione, nel dettaglio e
  nell'espansione completa. Dimensioni verificate: 1440 × 900, 1024 × 768,
  768 × 900 e 390 × 844. Nessuna sovrapposizione fra etichette visualizzate nei
  controlli geometrici e nessuno scorrimento orizzontale della pagina.
- Tutti i punti sono presenti nell'espansione completa e nella vista testuale.
  Le etichette sono progressive: a basso zoom se ne mostrano solo alcune,
  scelte in base allo spazio; zoom e ricerca rendono leggibili i dettagli.
  Zero sovrapposizioni non significa che migliaia di nomi siano leggibili
  contemporaneamente su uno schermo.

| Progetto | File rilevati | Nodi completamente espansi | Ridisegno misurato* | Errori scansione |
| --- | ---: | ---: | ---: | ---: |
| qwe modificato | 22 | 66 | 10 ms | 0 |
| Click | 102 | 1.059 | 113 ms | 0 |
| Full Stack FastAPI Template | 159 | 811 | 54 ms | 1 |
| Flask | 89 | 680 | 47 ms | 0 |

*Singola misura nella macchina di collaudo, inclusa lettura della geometria;
non un benchmark statistico né una garanzia sulle macchine degli utenti.
Non sono stati eseguiti i programmi o le suite dei progetti analizzati.
Le tre copie di benchmark risultano senza modifiche dopo la scansione.

## Revisioni dei progetti esterni

- `pallets/click`: `2247b35ea1c47c727d7a06e51fa280e12a863ff6`
- `fastapi/full-stack-fastapi-template`: `f4bcfaba7c85be3c6332cc74a20819f586dcdbc6`
- `pallets/flask`: `49943b5a94413a530761350f04e896f76e8d620e`

Il file `backend/app/api/deps.py` del template usa una sintassi `except`
più recente di quella accettata dal Python 3.12 usato per il collaudo.
Il programma segnala l'errore e continua la mappa; le dichiarazioni di quel
file non sono state estratte. Non è corretto considerarla una scansione completa.

## Correzioni verificate

- Gerarchia responsabilità → file → dichiarazioni, con identità indipendenti
  dalla riga e senza fondere funzioni omonime appartenenti a file diversi.
- Sottogruppi con spazio dedicato; mondo espandibile invece del vecchio recinto
  fisso, curve, alone e selezione delle dipendenze, etichette senza accavallamenti.
- Pulsanti zoom e Panoramica; barra laterale e prima apertura più curate.
- Dipendenze tra file conservate come evidenza, oltre a quelle tra responsabilità.
- Import JS/TS con `../` normalizzati correttamente.
- Importazione ripetuta dello stesso file e importazione su un progetto vuoto.
- Creazione del nodo manuale senza errore JavaScript.
- Ricerca azzerata quando cambia progetto; fallback alla mappa fresca se la
  copia locale non è valida.

## Riproduzione

```sh
python -m unittest discover -s tests -v
python -m compileall -q codeatlas tests
python -m pip install playwright==1.56.0
python -m playwright install chromium
python tests/browser_smoke.py --output /tmp/codeatlas-qa
```

Aggiungere `--chromium /percorso/chromium` per usare il browser di sistema,
oppure `--benchmark /percorso/progetto` (ripetibile) per analizzare altre copie.
La suite browser salva screenshot e `results.json`. La CI è configurata per
eseguire il collaudo e caricare gli artifact; l'esito remoto va controllato
sul commit pubblicato e non è implicato dagli esiti locali riportati qui.

## Limiti della prova da condividere

- Windows, macOS, Safari e Firefox non collaudati in questa sessione.
  Il doppio clic sul launcher Windows non è stato provato fisicamente.
- Serve Python 3.10+; nessun installer autonomo o eseguibile incluso.
- Supporto Python e JS/TS con i limiti descritti nel README. Nessuna promessa
  di funzionamento su linguaggi non supportati, grandi monorepo o sintassi
  più recenti del Python installato.
- Classificazione euristica: la forma non certifica l'architettura reale.
  Collegamenti dinamici e alias di compilazione possono mancare.
- Annotazioni nel browser ed esportazione manuale: nessun database condiviso.
- La nuova gerarchia cambia gli ID delle dichiarazioni rispetto alla prima
  versione; annotazioni vecchie possono restare come nodi manuali separati.
- Nessun adapter Graphify, analisi semantica completa o tracciamento runtime.

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

## Cora constellation — 2026-11-04

- `python -m unittest discover -s tests -q`: 38 tests passed, including desktop `/` serving the conceptual view, technical `/index.html` and JSON/JS assets.
- `npm test`: 24 tests passed. Added real Direzione DOM tests for 45-star overview, on-demand planets/moons, severity propagation, unchanged local maps and recoverable template replacement.
- `tests/cora_browser_smoke.cjs`: passed with Chromium 153 and Playwright. Actual desktop HTTP handler, desktop/mobile viewport, star/planet/moon navigation, edit and reload persistence, search, no browser errors. Requires Playwright and an available Chromium executable; command documented at top of script.
- Visually inspected desktop overview, calendar and calendar moons at 1600×1100; corrected root heading overlap and bottom clipping.
- Conceptual nodes remain unverified runtime descriptions; no Serveria deployment or operational integration tests were performed. Tests do not certify calendar notification delivery, orchestrator, external services or Debian health.

## Ricontrollo Windows del main integrato — 3 novembre 2026

Versione controllata: `85c35d0`, che include il redesign `b8deb32` e gli aggiornamenti successivi. Non sono stati sovrascritti i profili, le sei viste o la Direzione progetto.

- Python 3.13 / Windows: **31 test Python superati** e compilazione superata.
- `npm ci --ignore-scripts` e `npm test`: **18 test Node/DOM superati**. L'ambiente aveva Node 22.15, inferiore al requisito dichiarato (24.15); npm ha segnalato tale incompatibilità. Per lo sviluppo usare la versione dichiarata nel package.json. Nessuna dipendenza installata globalmente.
- Browser reale sulla versione corrente: avvio del modulo desktop, apertura qwe tramite percorso senza JSON, mappa iniziale con capacità/processi/basi, espansione Avvio e orchestrazione, scheda fissa destra con docstring ed evidenze, passaggio alla vista testuale e ritorno all'albero. Anteprima salvata localmente.
- Il precedente collaudo del redesign aveva verificato anche modifica della classificazione/scopo e ripristino dopo ricaricamento. Questi passaggi non sono stati ripetuti manualmente su ogni nuova vista; i test DOM aggiornati coprono persistenza e configurazione.
- Non collaudati qui il doppio clic fisico, tutte le interazioni della Direzione progetto, tutte le sei viste nel browser grafico o i grandi monorepo. Nessuna certificazione implicita della CI remota.
- Serveria non è stato modificato né eseguito.

## Cora/main merge — 2026-11-04

Main `9bddd41` integrated without replacing either direction view: generic `direzione.html/js` and Cora `cora-direzione.html/js`. Post-merge: 38 Python tests, 25 Node/DOM tests and the real Chromium Cora smoke check passed. The generic test confirms per-project plan persistence and unconfirmed-suggestion isolation; HTTP tests cover both pages and scripts. Cora still opens by default and preserves its local storage key.
