# Consegna a Work — integrazione della mappa Cora V2 con CodeAtlas e Serveria

**Data:** 3 novembre 2026  
**Repository da cui partire:** `Aleselva12/qwe`  
**Branch:** `progetti/cora-serveria`  
**Repository da analizzare/integrare successivamente:** `Aleselva12/serveria1`  
**Scopo del presente lavoro:** tramandare completamente decisioni e classificazione, non effettuare da questa conversazione il deploy.

## File da leggere, in questo ordine

1. **`docs/CORA_MAPPA_V2_COMPLETA.md`** — classificazione leggibile completa, comprese le lune, rapporti tra stelle, storia e problemi.
2. **`cora-plan.json`** — struttura v1 compatibile con il caricamento corrente, ora estesa con 45 stelle, pianeti, lune, dati di status distinti dalla priorità, collegamenti incrociati e ID persistenti. È la sorgente strutturata per implementare la pianta; **non crearne una copia concorrente**.
3. **`docs/MEMORIA_CORA.md`** — contributi e decisioni dell'altra conversazione, preservati integralmente; conserva casi guida e razionali.
4. **`README.md`** — comportamento reale dell'applicazione generica CodeAtlas e limiti di analisi.
5. **`docs/AI_CUSTOMIZATION.md`**, `codeatlas/concepts.py`, `index.html`, `views.js`, `profiles.js`, `evidence.js`, `workbench.js` — motore tecnico e interfaccia generica esistente. Non reimplementarlo inutilmente.
6. **`Aleselva12/serveria1:docs/project-status.json`** e `docs/HOME_PROJECT_STATUS.md` — stato roadmap W1–W3 e M1–M4, da verificare rispetto al commit realmente analizzato.

## Decisioni già confermate da rispettare

- 6 aree nelle radici: R1 Macchine, R2 Dati, R3 IA, R4 Ambiente, R5 Affidabilità, R6 Sicurezza. Un livello intermedio 'area' nelle radici permette di vedere 14 stelle senza confondere la categoria R1 con la macchina R1.1.
- 13 stelle nel tronco T1–T13, stabili, con un solo proprietario per funzione. Permission Engine nella radice R6, non sotto l'orchestratore; il tronco lo utilizza tramite collegamento.
- 7 rami A–G; D comprende programmi esterni paralleli e CodeAtlas; G **solo Agente programmatore**, nessun ramo genericamente 'futuro'.
- 18 stelle applicative, per un totale di **45 stelle**. 151 pianeti e 304 lune sono una *prima scomposizione* da correggere col tempo, non limiti o target per obbligare a nuovi nodi.
- I pianeti e le lune **non devono essere visualizzati tutti insieme** nella panoramica; aprirli selezionando una stella. Una stella può essere promossa/ridotta senza perdere figli, ID o cronologia.
- M3 all'inizio di molti rami e M4 come evoluzione verso le estremità sono un suggerimento, **non** un algoritmo di posizionamento. Nuovi obiettivi entrano nelle stelle pertinenti, altrimenti in una coda "da classificare".
- Colori: unknown=grigio, ok=verde, plan=giallo, minor=arancione, problem=rosso. La priorità di una stella non va assegnata automaticamente da status, file o test.
- Storia/presente/futuro nella scheda della stessa stella; le migliorie completate, i problemi risolti e le scelte abbandonate devono restare consultabili con origine, data e versione.
- Servizi esterni: mantenere Immich, Nextcloud, Magazzino Tele, Preventivi e CodeAtlas come stelle autonome; non duplicare il codice/servizio in Cora.
- Nessun LLM richiesto per l'analisi di base o per decidere la classificazione; il sistema può **proporre**, l'utente conferma le modifiche concettuali.
- Non inserire indiscriminatamente tutti i DB nel NAS: scegliere singolarmente la collocazione; file/foto/backup principalmente sul NAS futuro, DB operativi anche sul Debian.

## Contributi dell'altra conversazione e riconciliazione

Il documento `docs/MEMORIA_CORA.md` esplicitava una **ricostruzione V2 parziale**. Questo lavoro aggiunge ciò che mancava senza cancellarla:

| Elemento già presente | Scelta applicata |
| --- | --- |
| `radici` e `tronco` | Conservati con gli stessi ID; aggiunte stelle e sottolivelli |
| R1–R6, T1–T13 | ID conservati; sostituiti testi generici con descrizioni/pianeti/lune |
| D chiamato `programmi` | ID `programmi` conservato, `code: D`; D1–D3 mantengono gli ID `immich`, `nextcloud`, `magazzino` |
| F chiamato `macchine` | ID `macchine` conservato, `code: F`; F1 mantiene `id: worker` |
| `installare`, `assegnare` | Mantenuti come pianeti di F1, anziché crearne copie |
| C1a, C1b, C1c | Mantengono gli ID per interpretare richiesta, registrare evento, consegnare notifica |
| C1d, C1e | Mantengono le due idee future su riorganizzazione settimana e calendario in camera via API, con `status: idea` |
| Colori, no sovrappopolazione, tronco stabile | Conservati e applicati; nessun cambio automatico di priorità |
| Distinzione operatività vs codice | Aggiunta colonna `status`, separata da `priority`; `partial` NON è semaforo arancione |

Le vecchie note non identiche alla nuova `note` sono conservate anche come `earlierNote` sui nodi già esistenti. La presenza di un vecchio ID non attesta automaticamente che un componente software oggi funzioni.

## Schema dati di Direzione Cora (non schema generale dei profili CodeAtlas)

`cora-plan.json` mantiene `version:1` per compatibilità con la prima Direzione Cora, ma la `revision` identifica questa pianta V2.

- `nodes[]`: `id` immutabile, `parent` per la gerarchia, `title`, `role` sui nodi top-level, `classification` area/star/planet/moon, `code` per i codici visibili, `note`, `status`, `priority`, `sourceType`, `earlierNote` quando presente. Il campo `trunkLinks` sulle stelle è una proiezione minima dei collegamenti al tronco disponibile nella UI precedente.
- `relations[]`: relazioni concettuali cross-stella con `from`, `to`, `kind` (uses, depends_on, communicates_with, produces_for) e `note`. **Non** equiparare queste relazioni a chiamate runtime provate.
- `visibility`: la panoramica mostra radici/aree, tronco, rami e stelle; pianeti/lune si aprono per selezione.
- `priority` e `status` sono separati. Evitare di tradurre automaticamente `partial` in arancione o `planned` in giallo.
- Dati di schema non ancora implementati in Direzione: prove/versione/ambienti per singola stella, cronologia dettagliata e convalida delle fonti. Prima di aggiungere dati reali progettare un formato incrementale e migrabile, non sovraccaricare `note` arbitrariamente.

- `timeline` per ogni stella: `past` (vuoto finché non abbiamo commit/decisioni documentate), `present.statement` e `present.runtimeVerified:false`, `future` (obiettivi conosciuti). Non riempire il passato con eventi inventati né trasformare la descrizione corrente in certificazione di collaudo.
- `knownIssues[]` conserva difetti e dubbi da non perdere. `roadmapRefs[]` rimanda agli identificativi dei macro-obiettivi di serveria1. `observations[]` contiene soltanto conferme riferite dall'utente, con `commit:null` e `observedAt:null` finché non sappiamo versione/data della prova. Sono *provenienze*, non test E2E registrati.
- I nodi più importanti per i lavori prossimi sono T1/T9/T10 (W1), R5.2/Immich/Nextcloud (W2), G1 (W3), E1 (M3 clienti), F2 (M4 agenti distribuiti).

**Profondità:** radici → area → stella → pianeta → luna (5 livelli). Tronco → stella → pianeta → luna e ramo → stella → pianeta → luna (4). Il JS di Direzione è stato adattato per questi limiti e per l'apertura iniziale senza espansione dei pianeti.

## Come effettuare l'integrazione senza distruggere dati

1. **Confrontare commit e stato working tree** di qwe e serveria1. Tenere separate branch Cora e generic main: il codice dell'analizzatore generico va modificato solo quando migliora anche altri progetti.
2. **Non fondere automaticamente modelli concettuali e file scanning.** Il codice può suggerire associazioni e nodi, non decidere il significato architetturale né chiudere un problema.
3. **Usare `cora-plan.json` come bozza strutturata corrente**, senza duplicarlo in altri file manualmente editabili. Se si aggiunge persistenza sul server, scegliere proprietario unico/versioning/revisioni e una migrazione esplicita.
4. **Proteggere localStorage esistente.** La prima versione di Direzione salva nel browser in `codeatlas:cora:direction:v1`; questa copia locale potrebbe prevalere sul JSON aggiornato. Non scartarla: esportarla, confrontarla con il V2 e proporre un merge/import approvato. Non sovrascrivere il localStorage senza backup e conferma.
5. **Riutilizzare i motori esistenti** di scansione, viste e importazione di test nel CodeAtlas generico. La vista di direzione è ancora una pagina testuale espandibile: la costellazione 2D scura e la scheda fissa a destra sono da implementare.
6. **Integrare in Cora via modalità protetta.** Tailscale non è un permesso di amministrazione; controllare autorizzazioni e accesso a dati/repository. CodeAtlas legge il progetto analizzato, non esegue file del progetto, non modifica Cora e non riceve privilegi Docker/SSH indiscriminati.
7. **Gestire test e commit come evidenze con provenance:** commit SHA, ambiente, timestamp e tipo di verifica. Una prova CI su branch non certifica il Debian attivo. I test importati dal browser e le note utente hanno provenienze diverse. Associarli alle stelle, senza creare un secondo motore di test in Atlas.
8. **Non assegnare un colore positivo automaticamente.** In presenza di anomalie, evidenziare il nodo interessato e le sue dipendenze senza dichiarare guasto l'intero ramo; eventuale propagazione dei colori resta una decisione aperta.
9. **Prove e rollback:** diff di albero prima/dopo, ID preservati, import/export ripetuti, progetti semplici e complessi, browser mobile/desktop, l'originale della pianta sempre recuperabile.

## Casi di accettazione da non saltare

- La panoramica mostra 6 aree R1–R6, 13 stelle T1–T13 e 7 rami con 18 stelle principali, senza mostrarne subito 151 pianeti e 304 lune.
- Clic su C1 Calendario apre i pianeti C1a (interpretare), C1b (registrare una volta), C1c (consegnare notifica) e mostra anche C1d/C1e come *idee future*.
- Clic su F1 mostra **una** stella worker e le operazioni di collegamento e assegnazione come pianeti, senza perdere gli ID `worker`, `installare`, `assegnare`.
- R6.2 Permission Engine resta nelle radici anche se T1 Supervisor, F2 agenti remoti e G1 Programmatore lo utilizzano.
- G contiene solo G1, senza sezione separata per altri progetti futuri.
- I programmi esterni sono stelle di D; un loro problema non colora automaticamente tutta Serveria di rosso.
- Spostando un pianeta sotto una stella nuova restano ID, sottoelementi, storico, decisioni e riferimenti ai test.
- Le informazioni “presente nel codice”, “verificato in CI” e “collaudato sul Debian” sono distinte. Il verde va solo a seguito di una decisione o evidenza compatibile con la policy approvata.
- Un test regressivo della Chat deve poter associare il fallimento all'hop corretto; no doppie fonti di monitoraggio.
- L'appuntamento di prova è creato una volta e la notifica arriva sul telefono: questa è una **verifica futura**, non una prova già superata.
- Per il CRM (E1), i Word originari non vengono cancellati e il SQL aziendale non viene modificato durante la scoperta.
- Per F2, SQL laptop soltanto read-only e nessuna distribuzione autonoma di agenti o credenziali.
- Integrando la UI sul server, l'autenticazione e il perimetro dati restano esplicitamente controllati, senza esposizione dell'analisi a Internet pubblico.

## Questioni concettuali aperte da sottoporre all'utente

- La rappresentazione esatta delle 6 radici e 13 stelle del tronco nella costellazione: non fissare coordinate né numero di collegamenti “decorativi” prima dell'esperimento visivo.
- Regola di propagazione di problemi e priorità dei pianeti verso la stella/genitore.
- Se mantenere gli stati `partial` e `planned` esposti visivamente in aggiunta ai colori, oppure solo nella scheda.
- Schema persistente completo della dimensione temporale e riconciliazione di versioni concorrenti.
- Dove memorizzare le associazioni confermate fra mappa concettuale e sorgenti/commit di serveria1, per non duplicare il database dei controlli già esistente.
- La verifica operativa dei componenti per i quali disponiamo solo di stato documentale o prova riferita dall'utente.

## Prossima attività operativa

L'ordine della roadmap Cora rimane invariato: **W1 Orchestratore V1 e suo collaudo causale reale → W2 Aggiornamenti Immich/Nextcloud → W3 Programmatore**. Questo lavoro di mappa non implica che W1 sia concluso o che W2/W3 siano avviati.

Non applicare merge su main e non fare deploy sul Debian per il solo fatto che la pianta V2 sia completa.
