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
