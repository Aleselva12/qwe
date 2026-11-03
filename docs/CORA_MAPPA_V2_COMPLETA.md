# Cora / Serveria — Mappa concettuale completa V2

**Versione:** 3 novembre 2026 · **Fonte dati:** `cora-plan.json` sul branch `progetti/cora-serveria`.

Questo documento è la **copia leggibile e completa della struttura** da far utilizzare a Work, non un nuovo schema alternativo. Per gli ID, i link tra componenti e l'integrazione software si considera autorevole il JSON. La mappa descrive ciò che intendiamo costruire; **non è un certificato del funzionamento della versione installata sul Debian**.

## Decisioni vincolanti

- **Radici:** sei aree: R1 macchine, R2 dati, R3 motori IA e modelli, R4 ambiente operativo, R5 affidabilità della base, R6 sicurezza.
- **Tronco:** tredici stelle T1–T13 con responsabilità condivise e stabili. Le applicazioni usano queste capacità tramite collegamenti: non le duplicano.
- **Rami:** A Conversazione, B File/documenti/conoscenza, C Comunicazione/organizzazione, D Programmi esterni autonomi, E Clienti/commerciale, F Lavoro distribuito, G **soltanto Programmatore**.
- **Stelle, pianeti e lune:** l'inquadratura iniziale mostra le stelle; pianeti e lune solo quando si esplora una stella. Un pianeta può diventare stella, e viceversa, mantenendo ID/storia.
- **Futuro non è un ramo:** i placeholder restano nelle aree funzionali e conservano obiettivi e progressi nel pannello passato/presente/futuro. M3 spesso è all'inizio del ramo, M4 verso le estremità: non è una regola rigida.
- **Colori per priorità dichiarata:** grigio da valutare/placeholder; verde tutto ok; giallo aggiornamento pianificato; arancione malfunzionamento minore; rosso problema. La presenza del codice o di un test non attribuisce automaticamente verde.
- **Status di realizzazione distinti:** `present`, `partial`, `planned`, `idea` e `unverified` sono indipendenti dal colore. “Presente nel codice” e “verificato sul Debian” sono condizioni diverse.
- **No duplicazioni:** un'unica collocazione canonica per ciascuna funzione e un unico registro dei controlli; le dipendenze fra stelle sono relazioni, non copie del componente.
- **Evoluzione semiautomatica:** nuovi commit, PR e test possono proporre modifiche alla pianta, non spostare automaticamente il tronco o cancellare la storia.

## Panoramica

| Livello | Elementi |
| --- | --- |
| Radici | R1–R6: 14 stelle |
| Tronco | T1–T13: 13 stelle |
| Rami | A–G: 18 stelle |
| Totale | **45 stelle** con pianeti e lune |
| Collegamenti | 37 proposte concettuali, non attestate a runtime |

### Come leggere lo stato

- `present`: risorsa/codice presente; da solo non significa funzionante.
- `partial`: realizzazione parziale o collaudo end-to-end ancora aperto.
- `planned`: sviluppo deciso ma ancora non disponibile.
- `idea`: possibilità discussa, non decisione implementativa.
- Priorità `unknown`: nessuna valutazione di salute attribuita; **non è un problema rosso** e non è verde.

## RADICI — risorse e requisiti

### R1 · Macchine e infrastruttura fisica

Dispositivi e risorse, non selezione dei task

#### R1.1 · Server Debian — `partial`

Nodo centrale operativo per Cora e servizi; GPU locale futura

- **Pianeta: Macchina centrale**
  - Luna: Debian
  - Luna: Applicazioni
  - Luna: Servizi 24/7
- **Pianeta: Risorse hardware**
  - Luna: CPU e RAM
  - Luna: Espansione GPU futura
- **Pianeta: Continuità**
  - Luna: Indipendenza da worker esterni
  - Luna: Accesso SSH controllato

#### R1.2 · Desktop — `partial`

RX 6800 con inferenza GPU riportata dall’utente; modello effettivo non sempre attestato

- **Pianeta: Capacità GPU**
  - Luna: RX 6800 16 GB
  - Luna: Profili VRAM
- **Pianeta: Disponibilità**
  - Luna: Attivazione esplicita
  - Luna: Verifica inferenza
- **Pianeta: Prestazioni**
  - Luna: Modello eseguito
  - Luna: Tempi misurati

#### R1.3 · Laptop — `partial`

Worker GPU già provato; futuro dispositivo per agente locale

- **Pianeta: Capacità GPU**
  - Luna: Inferenza provata dall’utente
  - Luna: Profili del worker
- **Pianeta: Disponibilità**
  - Luna: Stato online e offline
  - Luna: Tailscale
- **Pianeta: Espansione futura**
  - Luna: Agenti operativi locali
  - Luna: Tool autorizzati

#### R1.4 · NAS dedicato — `planned`

Nodo futuro per foto file cloud e backup; non tutti i database per forza sul NAS

- **Pianeta: Hardware NAS**
  - Luna: Dischi e ridondanza
  - Luna: Acquisti e alimentazione
- **Pianeta: Archiviazione**
  - Luna: Fotografie e file
  - Luna: Backup Serveria
- **Pianeta: Servizi opzionali**
  - Luna: Valutazione per servizio
  - Luna: Non migrare automaticamente PostgreSQL

### R2 · Dati e archiviazione

Collocazione fisica e persistenza, non strumenti documentali

#### R2.1 · Database e persistenza — `partial`

PostgreSQL pgvector e SQL aziendali; collocazione Debian NAS da decidere

- **Pianeta: PostgreSQL**
  - Luna: Memoria e runtime
  - Luna: Log e registri
- **Pianeta: Database applicativi**
  - Luna: Database SQL clienti
  - Luna: Evita doppie anagrafiche
- **Pianeta: Schema e collocazione**
  - Luna: Versioni e migrazioni
  - Luna: Database Debian NAS per singolo servizio

#### R2.2 · Archiviazione dei file — `partial`

Filesystem Debian Libreria IA e futuro NAS

- **Pianeta: Storage Debian**
  - Luna: Condivisioni e percorsi
  - Luna: Originali e copie
- **Pianeta: Integrità**
  - Luna: Disponibilità mount
  - Luna: Conflitti e versioni
- **Pianeta: NAS futuro**
  - Luna: Storage condiviso
  - Luna: Migrazione controllata

### R3 · Motori IA e modelli

Software e modelli eseguibili, non routing fra agenti

#### R3.1 · Motori di inferenza — `partial`

Ollama motori audio ed embeddings locali o remoti

- **Pianeta: Ollama e LLM**
  - Luna: API modelli
  - Luna: Inferenza reale
- **Pianeta: Trascrizione**
  - Luna: Whisper e prerequisiti
  - Luna: Diarizzazione opzionale
- **Pianeta: Embeddings**
  - Luna: Indicizzazione vettoriale
  - Luna: Verifica del retrieval

#### R3.2 · Modelli IA — `partial`

Modelli installati requisiti hardware e valutazione nuovi modelli

- **Pianeta: Catalogo**
  - Luna: Versione e identità
  - Luna: Compatibilità RAM VRAM
- **Pianeta: Valutazione**
  - Luna: Qualità e latenza
  - Luna: Benchmark ripetibili
- **Pianeta: Ricerca futura**
  - Luna: Colibrì da valutare
  - Luna: Licenze e disponibilità

### R4 · Ambiente operativo

Sistema operativo, container, dipendenze e servizi host

#### R4.1 · Sistema operativo e servizi host — `present`

Debian processi servizi amministrativi e systemd

- **Pianeta: Debian**
  - Luna: Utenti e permessi host
  - Luna: Aggiornamenti OS
- **Pianeta: systemd**
  - Luna: Updater host
  - Luna: Avvio stop e log
- **Pianeta: Amministrazione**
  - Luna: SSH
  - Luna: Configurazione dei servizi

#### R4.2 · Ambiente applicativo — `present`

Docker Compose Python FastAPI React Vite

- **Pianeta: Docker Compose**
  - Luna: Immagini e container
  - Luna: Deploy e variabili
- **Pianeta: Backend**
  - Luna: Python e FastAPI
  - Luna: Dipendenze e profili
- **Pianeta: Frontend**
  - Luna: React Vite PWA
  - Luna: Build e compatibilità

### R5 · Affidabilità della base

Backup, restore, aggiornamenti e rilascio sicuro

#### R5.1 · Backup e ripristino — `partial`

Copie e procedure presenti o previste; restore completo da provare

- **Pianeta: Backup**
  - Luna: Database
  - Luna: File e configurazioni
- **Pianeta: Ripristino isolato**
  - Luna: Database vuoto
  - Luna: Verifica dati e hash
- **Pianeta: NAS futuro**
  - Luna: Politica copie
  - Luna: Frequenza e retention

#### R5.2 · Aggiornamenti e rilasci — `partial`

Updater Cora presente; aggiornamenti Immich Nextcloud lavoro W2

- **Pianeta: Updater Cora**
  - Luna: Commit e deploy
  - Luna: Rollback
- **Pianeta: CI e verifica**
  - Luna: Test codice
  - Luna: Collaudo versione Debian
- **Pianeta: App esterne**
  - Luna: Immich e Nextcloud
  - Luna: Backup conferma e health finale

### R6 · Sicurezza

Rete privata, identità, credenziali e Permission Engine

#### R6.1 · Rete privata identità credenziali — `partial`

Tailscale e accessi privati non equivalgono ai permessi dell’applicazione

- **Pianeta: Tailscale**
  - Luna: Accesso remoto
  - Luna: Connessione tra nodi
- **Pianeta: Identità**
  - Luna: Account e dispositivi
  - Luna: Chiavi e segreti
- **Pianeta: Futuro trust**
  - Luna: Identità per agente
  - Luna: Revoca e rotazione

#### R6.2 · Permessi e autorizzazioni — `partial`

Permission Engine indipendente dal modello e approvazioni esplicite

- **Pianeta: Permission Engine**
  - Luna: Automatico richiesta bloccato
  - Luna: Regole deterministiche
- **Pianeta: Ambito**
  - Luna: Tool e agente
  - Luna: File database dispositivo
- **Pianeta: Audit e revoca**
  - Luna: Operazioni con effetti
  - Luna: Revocare accessi

## TRONCO — capacità condivise e stabili

### T1 · Supervisor e orchestrazione — `partial`

Supervisor LangGraph e router shadow; collaudo causale Debian aperto

- **Pianeta: Supervisor**
  - Luna: Ingresso richieste
  - Luna: Delega a specialisti
- **Pianeta: Router shadow**
  - Luna: Routing proposto non autorevole
  - Luna: Escalation verificabile
- **Pianeta: Larva v0**
  - Luna: Osservatore deterministico
  - Luna: Niente azioni autonome

### T2 · Capability Registry e strumenti — `partial`

Unico registro delle capacità e contratti di tool

- **Pianeta: Capability Registry**
  - Luna: Tool realmente esposti
  - Luna: Identità e descrizioni
- **Pianeta: Contratti**
  - Luna: Parametri e errori
  - Luna: Permessi richiesti
- **Pianeta: Collegamenti**
  - Luna: Agente chiama tool corretto
  - Luna: Errori di delega

### T3 · System Coordinator — `partial`

Coordinamento proprietà e stato dei componenti oggi read-only

- **Pianeta: Ownership**
  - Luna: Responsabilità dei moduli
  - Luna: Nessuno stato duplicato
- **Pianeta: Panoramica**
  - Luna: Coordinator osserva
  - Luna: Stato servizi
- **Pianeta: Evoluzioni**
  - Luna: Integrazioni distribuite
  - Luna: Nuovi componenti

### T4 · Runtime e State Machine — `partial`

Esecuzioni stati transizioni e controllo degli effetti

- **Pianeta: Runtime persistente**
  - Luna: Identità run
  - Luna: Risultati e revisioni
- **Pianeta: State Machine**
  - Luna: Transizioni lecite
  - Luna: Annullamento e ripresa
- **Pianeta: Effetti**
  - Luna: Retry idempotente
  - Luna: Stato incerto mai ripetuto ciecamente

### T5 · Event Bus e Component Bus — `partial`

Messaggi eventi e collegamenti tipizzati nel processo

- **Pianeta: Event Bus**
  - Luna: Eventi e sottoscrizioni
  - Luna: Origine timestamp
- **Pianeta: Component Bus**
  - Luna: Messaggi tipizzati
  - Luna: Risposta al destinatario
- **Pianeta: Futuro distribuito**
  - Luna: Bus tra nodi
  - Luna: Disconnessioni

### T6 · Context Manager — `partial`

Contratti ContextRequest ContextPacket; retrieval progressivo non completo

- **Pianeta: Contratti di contesto**
  - Luna: Richiesta e pacchetto
  - Luna: Budget
- **Pianeta: Selezione progressiva**
  - Luna: Recupero rilevante
  - Luna: Escalation
- **Pianeta: Letterale e rielaborato**
  - Luna: Fonte originale
  - Luna: Interpretazione distinta

### T7 · Memoria — `partial`

Quattro livelli e revisioni ancora da collaudare nell’uso

- **Pianeta: Permanente**
  - Luna: Identità
  - Luna: Revisione
- **Pianeta: Semantica**
  - Luna: Conoscenza
  - Luna: Provenienza
- **Pianeta: Episodica**
  - Luna: Eventi e passaggi
  - Luna: Collegamento ai run
- **Pianeta: Di lavoro**
  - Luna: Task correnti
  - Luna: Scadenza
- **Pianeta: Custodia futura**
  - Luna: Mente saggia o Custode idea
  - Luna: Versionamento governato

### T8 · Registro e configurazione degli agenti — `partial`

Ruoli strumenti modelli e configurazione agenti

- **Pianeta: Registro agenti**
  - Luna: Ruolo e capability
  - Luna: Specialisti presenti
- **Pianeta: Modello per agente**
  - Luna: Selezione e salvataggio
  - Luna: Profilo worker
- **Pianeta: Verifica effettiva**
  - Luna: Modello eseguito
  - Luna: Macchina usata

### T9 · Planner e pianificazione task — `planned`

Plan multi step code persistenti scheduler failover fase 2

- **Pianeta: Plan**
  - Luna: Multi step strutturato
  - Luna: Persistenza e ripresa
- **Pianeta: Code e priorità**
  - Luna: Limiti e concorrenza
  - Luna: Nessun effetto doppio
- **Pianeta: Scheduling**
  - Luna: Worker spento o acceso
  - Luna: Failover controllato

### T10 · Tracciabilità ed errori — `partial`

Attività trace decisioni e diagnosi causale da collaudare

- **Pianeta: Run e trace**
  - Luna: Richiesta verso risposta
  - Luna: Correlazione degli hop
- **Pianeta: Causa errore**
  - Luna: Individuare primo passaggio fallito
  - Luna: Timeout fallback
- **Pianeta: Prestazioni**
  - Luna: Tempi per fase
  - Luna: Regressioni tra versioni

### T11 · Registro unico test e salute — `partial`

Catalogo e cicli periodici nel codice; non tutto E2E collaudato

- **Pianeta: Catalogo unico**
  - Luna: ID test e componenti
  - Luna: Nessun monitor duplicato
- **Pianeta: Test sicuri**
  - Luna: Preflight e contratti
  - Luna: Sintetici E2E isolati
- **Pianeta: Storico**
  - Luna: Ambiente e commit
  - Luna: Stato dopo riavvio
- **Pianeta: Regressioni**
  - Luna: Chat orchestratore agente
  - Luna: Audio Word Calendar worker

### T12 · Interfaccia comune Cora — `partial`

Home navigazione Impostazioni Architettura Attività e PWA

- **Pianeta: Home e roadmap**
  - Luna: W1 W2 W3
  - Luna: Obiettivi M1 M4
- **Pianeta: Architettura Impostazioni**
  - Luna: Modelli e agenti
  - Luna: Gestione Memoria
- **Pianeta: PWA**
  - Luna: Telefono e notifiche
  - Luna: Aggiorna Cora
- **Pianeta: Attività**
  - Luna: Collegamento a trace
  - Luna: Errori

### T13 · Motore comune automazioni — `partial`

Editor e validazione; esecutore generico da realizzare

- **Pianeta: Bozze grafiche**
  - Luna: Editor
  - Luna: Validazione
- **Pianeta: Esecutore**
  - Luna: Tool con permessi
  - Luna: Annullamento
- **Pianeta: Trigger**
  - Luna: Pianificazione periodica
  - Luna: Condizioni ed eventi

## RAMI — capacità funzionali

### A · Conversazione

Chat e sessioni di dialogo

#### A1 · Chat e interazione — `partial`

Ingresso utente e risposta Cora con strumenti e deleghe

- **Pianeta: Conversazione**
  - Luna: Inviare richieste
  - Luna: Ricevere risposte
  - Luna: Gestire errori
- **Pianeta: Strumenti della chat**
  - Luna: Allegati e tool
  - Luna: Deleghe agli specialisti
- **Pianeta: Risposta verificabile**
  - Luna: Chat supervisor agente modello risposta
  - Luna: Streaming annullamento timeout

#### A2 · Conversazioni e sessioni — `partial`

Cronologia thread transcript e continuità

- **Pianeta: Cronologia**
  - Luna: Elenco conversazioni
  - Luna: Riapertura sessioni
- **Pianeta: Identità thread**
  - Luna: Persistenza e ricerca
  - Luna: Versioni transcript
- **Pianeta: Continuità**
  - Luna: Contesto e memoria
  - Luna: Rimozione autorizzata

### B · File documenti e conoscenza

File Libreria IA documenti e lettura

#### B1 · Gestione file — `partial`

File server e NAS consultabili modificabili con permessi

- **Pianeta: Esplorazione**
  - Luna: Directory e ricerca
  - Luna: Anteprime
- **Pianeta: Operazioni**
  - Luna: Leggere e scaricare
  - Luna: Modificare rinominare ed eliminare con conferma
- **Pianeta: Risorse distribuite**
  - Luna: NAS e mount
  - Luna: Controllo conflitti

#### B2 · Libreria IA e Local Reader — `partial`

Copie IA recupero fonti e lettura documenti

- **Pianeta: Libreria**
  - Luna: Copia e originale separati
  - Luna: Indicizzazione
- **Pianeta: Local Reader**
  - Luna: Ricerca e fonti
  - Luna: Rilevanza e attendibilità
- **Pianeta: Sincronizzazione copie**
  - Luna: Controllo modifiche
  - Luna: Conflitti e versioni

#### B3 · Gestione documentale — `partial`

Word PDF e OCR futuro

- **Pianeta: Word DOCX**
  - Luna: Lettura e modifica protetta
  - Luna: Proposte su copia con backup
- **Pianeta: PDF**
  - Luna: Lettura e generazione
  - Luna: Validazione del documento
- **Pianeta: OCR futuro**
  - Luna: PDF scansionati
  - Luna: Formati avanzati
- **Pianeta: Versioni**
  - Luna: Hash e conflitti
  - Luna: Ripristino

### C · Comunicazione e organizzazione

Calendario email audio e appunti

#### C1 · Calendario — `partial`

Caso guida: dichiarare appuntamento vederlo una sola volta e ricevere notifica telefonica

- **Pianeta: Interpretare la richiesta**
  - Luna: Lingua naturale e proposta
  - Luna: Data ora cliente
- **Pianeta: Registrare o modificare evento**
  - Luna: Approvazione
  - Luna: Idempotenza e duplicati
- **Pianeta: Consegnare notifica**
  - Luna: PWA e telefono
  - Luna: Verifica ricezione
- **Pianeta: Riorganizzare la settimana con IA** — `idea`
  - Luna: Proposta di pianificazione
  - Luna: Conferma prima di modificare
- **Pianeta: Calendario digitale in camera via API** — `idea`
  - Luna: Schermo e dispositivo futuro
  - Luna: Integrazione da decidere
- **Pianeta: Sincronizzazione**
  - Luna: Google e Cora
  - Luna: Log esportazioni

#### C2 · Email e agente Mail — `partial`

Gmail strumenti ricerca lettura bozze presenti; flusso reale non provato

- **Pianeta: Accesso Gmail**
  - Luna: Autorizzazione account
  - Luna: Ricerca e lettura
- **Pianeta: Riepiloghi e bozze**
  - Luna: Riassunto giornaliero
  - Luna: Composizione messaggi
- **Pianeta: Invio approvato**
  - Luna: Destinatari verificati
  - Luna: Conferma esplicita
- **Pianeta: Connessioni commerciali**
  - Luna: CRM clienti
  - Luna: Preventivi

#### C3 · Audio e agente Audio — `partial`

Caricamento e trascrizione riferiti funzionanti; Word reale da collaudare

- **Pianeta: Acquisizione audio**
  - Luna: Telefono e PC
  - Luna: Data e interlocutori
- **Pianeta: Trascrizione**
  - Luna: Whisper e correzioni
  - Luna: Diarizzazione opzionale
- **Pianeta: Appunti strutturati**
  - Luna: Riepilogo cliente
  - Luna: Proposte azioni
- **Pianeta: Pubblicazione**
  - Luna: Approvazione Word su copia
  - Luna: Future schede cliente

### D · Programmi esterni e autonomi

Immich Nextcloud Magazzino Tele Preventivi e CodeAtlas come stelle autonome e parallele. Il loro codice può appartenere ad altre repository.

#### D1 · Immich — `partial`

Archivio fotografie già usato; agenti e aggiornamenti da completare

- **Pianeta: Foto e archivio**
  - Luna: Memoria foto originali
  - Luna: Accesso mobile
- **Pianeta: Integrazione agentica**
  - Luna: Ricerca autorizzata
  - Luna: Nessuna duplicazione degli originali
- **Pianeta: Aggiornamenti W2**
  - Luna: Versione e backup
  - Luna: Conferma e test finale

#### D2 · Nextcloud — `partial`

Cloud condiviso presente; collegamento File e aggiornamenti da perfezionare

- **Pianeta: File cloud**
  - Luna: Accesso da telefono e desktop
  - Luna: Condivisione
- **Pianeta: Sincronizzazione**
  - Luna: Client e conflitti
  - Luna: Collegamento pagina File
- **Pianeta: Agenti**
  - Luna: Tool autorizzati
  - Luna: Accesso corretto ai file
- **Pianeta: Aggiornamenti W2**
  - Luna: Backup versione
  - Luna: Verifica successiva

#### D3 · Magazzino Tele — `partial`

App esterna con bridge Cora e import da verificare

- **Pianeta: Articoli e disponibilità**
  - Luna: Magazzino e movimenti
  - Luna: Anagrafiche
- **Pianeta: Ordini e import**
  - Luna: Excel e righe
  - Luna: Duplicati e dati mancanti
- **Pianeta: Accesso Cora**
  - Luna: Bridge e permessi
  - Luna: Test del servizio esterno

#### D4 · Preventivi — `partial`

Programma esterno per preventivi PDF collegamento Cora ancora incompleto

- **Pianeta: Preparazione preventivi**
  - Luna: Prodotti e listini
  - Luna: Prezzi e revisioni
- **Pianeta: PDF**
  - Luna: Documento di prova
  - Luna: Generazione controllata
- **Pianeta: Interoperabilità**
  - Luna: Database clienti
  - Luna: Email con invio approvato

#### D5 · CodeAtlas — `partial`

Programma indipendente per vedere struttura codice e direzione Cora

- **Pianeta: Analisi repository**
  - Luna: File moduli e dipendenze
  - Luna: Sei viste tecniche
- **Pianeta: Pianta concettuale**
  - Luna: Radici tronco rami stelle pianeti lune
  - Luna: Classificazione semiautomatica con conferma
- **Pianeta: Evidenze e storia**
  - Luna: Commits e problemi
  - Luna: Test ed esiti di provenienza distinta
- **Pianeta: Integrazione Serveria**
  - Luna: Link da Home
  - Luna: Versionamento della pianta

### E · Clienti e lavoro commerciale

Dal CRM M3 alle capacità agentiche M4

#### E1 · Anagrafica clienti e CRM — `planned`

M3: database unico e schede clienti collegando SQL aziendale e Word

- **Pianeta: Archivio strutturato**
  - Luna: Identità contatti stabilimenti
  - Luna: Storico commerciale
- **Pianeta: Riuso SQL aziendale**
  - Luna: Schema e chiavi
  - Luna: Fonte autorevole e deduplica
- **Pianeta: Schede cliente**
  - Luna: Appuntamenti note documenti
  - Luna: Preventivi e attività
- **Pianeta: Transizione Word**
  - Luna: Conservare gli originali
  - Luna: Import progressivo verificato

#### E2 · Assistente commerciale — `planned`

M4: workflow email preventivi cliente con autorizzazioni

- **Pianeta: Gestione richieste**
  - Luna: Associare email audio clienti
  - Luna: Proposta attività
- **Pianeta: Preventivo assistito**
  - Luna: Email PDF e revisione
  - Luna: Invio autorizzato
- **Pianeta: Follow up**
  - Luna: Promemoria e richiami
  - Luna: Aggiornamento schede

### F · Lavoro distribuito

Worker GPU distinti da agenti operativi installati sui dispositivi.

#### F1 · Worker IA e collaborazione macchine — `partial`

Una stella per lavorare con più GPU; inferenza provata, routing da attestare

- **Pianeta: Collegare un worker su un altro dispositivo**
  - Luna: Registrazione identità
  - Luna: Stato connesso
- **Pianeta: Assegnare lavoro ai worker**
  - Luna: Scelta macchina e modello
  - Luna: Verifica modello effettivo
- **Pianeta: Modelli e limiti**
  - Luna: Profili VRAM e tempo
  - Luna: Risorse abilitate dall utente
- **Pianeta: Scheduler multi worker**
  - Luna: Code priorità
  - Luna: Offline fallback controllato

#### F2 · Agenti operativi sui dispositivi — `planned`

M4: distribuzione di agenti capaci di usare strumenti locali con permessi minimi

- **Pianeta: Deploy verificato**
  - Luna: Installare runtime fidato
  - Luna: Aggiornare revocare rimuovere
- **Pianeta: Tool locali**
  - Luna: Allowlist file cartelle e database
  - Luna: Credenziali restano sul laptop
- **Pianeta: SQL clienti dal laptop**
  - Luna: Lettura sola lettura
  - Luna: Staging e approvazione import
- **Pianeta: Audit**
  - Luna: Trace e log
  - Luna: Bloccare controllo generale

### G · Agente programmatore

Ramo riservato al Programmatore e alle sue evoluzioni

#### G1 · Agente programmatore — `partial`

Programmatore con tool e workflow controllati; lavoro W3 dopo aggiornamenti

- **Pianeta: Comprensione repository**
  - Luna: Ricerca file e analisi
  - Luna: Dipendenze e obiettivi
- **Pianeta: Modifiche controllate**
  - Luna: Creare e modificare file
  - Luna: Branch commit revert rollback
- **Pianeta: Verifiche**
  - Luna: Test autorizzati
  - Luna: Regressioni e report
- **Pianeta: Espansione**
  - Luna: Più repository e dispositivi
  - Luna: Collegamento Atlas

## Collegamenti concettuali fra stelle

Sono **collegamenti proposti** da discutere e da validare sul codice; non rappresentano automaticamente chiamate osservate a runtime. Ogni funzione mantiene un solo proprietario canonico.

| Da | Tipo | A | Scopo |
| --- | --- | --- | --- |
| A1 | uses | T1 | Chat → supervisor → agente → risposta |
| A1 | uses | T2 | Tool autorizzati e deleghe |
| A1 | uses | T10 | Diagnosi causa errore |
| A2 | uses | T7 | Storia della chat distinta dalla memoria di Cora |
| B1 | depends_on | R2.2 | Filesystem e mount dati |
| B2 | uses | T6 | Recupero del contesto |
| B3 | uses | B1 | Accesso sicuro ai file |
| C1 | uses | T2 | Tool calendario |
| C1 | communicates_with | C3 | Proposte appuntamenti da audio |
| C1 | communicates_with | E1 | Associare appuntamenti cliente |
| C2 | communicates_with | E1 | Email cliente |
| C2 | communicates_with | D4 | Invio preventivo |
| C3 | uses | B3 | Scrittura appunti Word |
| C3 | produces_for | E1 | Appunti CRM futuro |
| D1 | depends_on | R2.2 | Storage foto |
| D2 | communicates_with | B1 | Pagina File e cloud |
| D2 | depends_on | R2.2 | Dati persistenti |
| D3 | communicates_with | E1 | Anagrafiche clienti senza doppioni |
| D4 | uses | E1 | Preventivo da cliente autorevole |
| E2 | uses | E1 | Assistente commerciale usa CRM |
| E2 | uses | C2 | Bozze ed email |
| E2 | uses | D4 | PDF generati da Preventivi |
| F1 | depends_on | R1.2 | GPU desktop disponibile |
| F1 | depends_on | R1.3 | GPU laptop disponibile |
| F1 | uses | T9 | Coda e scheduling |
| F2 | depends_on | R6.2 | Permessi locali e revoca |
| F2 | produces_for | E1 | Import SQL clienti approvato |
| G1 | uses | T11 | Test condivisi |
| G1 | communicates_with | D5 | Atlas e analisi impatto |
| D5 | uses | T10 | Tracce e diagnostica |
| D5 | uses | T11 | Import esiti con provenienza |
| R5.2 | uses | T11 | CI e prove deploy |
| T1 | depends_on | R6.2 | Autorizzazioni indipendenti dai modelli |
| T8 | depends_on | R3.2 | Modello presente e identificabile |
| T9 | uses | T4 | Piano eseguito dal runtime |
| T11 | communicates_with | T10 | Regressione e causa |
| T12 | communicates_with | D5 | Collegamento Home Atlas |

## Informazioni raccolte anche nell'altra conversazione

Nel documento `docs/MEMORIA_CORA.md` sono presenti precisazioni che questa mappa conserva:

1. **Caso Calendario:** dire un appuntamento, registrarlo una sola volta e ricevere la notifica sul telefono. In C1 i pianeti interpretazione, registrazione e notifica sono distinti. Le idee future “riorganizzare la settimana con IA” e “calendario digitale in camera tramite API” sono mantenute come `idea`, non come funzionalità.
2. **Una sola stella Worker per le macchine:** i punti di connessione e assegnazione lavoro restano pianeti della F1. Separata F2, che riguarda agenti **operativi** distribuiti, con autorizzazioni di scrittura e lettura locali.
3. **Programmi indipendenti:** Immich, Nextcloud, Magazzino Tele, Preventivi e CodeAtlas sono stelle del ramo D, anche quando il codice dei programmi si trova in altre repository.
4. **Tronco stabile:** una responsabilità può appartenere al tronco anche quando oggi la usa un solo ramo; l'espansione avviene principalmente tramite pianeti/lune.
5. **Storia e futuro:** la scheda di ciascuna stella deve conservare vecchi commit, decisioni, regressioni e obiettivi, senza cancellare lavori risolti o idee non ancora sviluppate.

## Priorità operative già decise

- **W1:** orchestratore V1. La base è presente nel codice, ma prima di chiudere W1 serve test repository coerente e un run reale sul Debian verificato in Attività (route → contesto/tool → componente → modello/macchina → esito). La fase 2 comprende scheduler multi-worker, Context Manager progressivo, piano persistente e failover.
- **W2:** dopo W1, aggiornamenti Immich e Nextcloud dalla Home con gestore host autorizzato, backup, conferma, test e gestione degli errori. Non sono già implementati dal gestore corrente.
- **W3:** dopo W2 e l'upgrade hardware, riprendere l'agente Programmatore. Esiste un segnaposto distinto dalla pagina Programma attuale.
- **M3:** database strutturato per clienti E1, potenzialmente riutilizzando SQL aziendale senza duplicare anagrafiche. Non è stato importato.
- **M4:** assistente commerciale E2 e agenti installabili su dispositivi F2. Primo caso: SQL clienti del laptop in sola lettura → proposta di import in staging → approvazione esplicita.

## Problemi e verifiche che non devono perdersi

- Routing Chat → Supervisor → tool → agente → modello → risposta: il contratto strutturale non prova il risultato funzionale reale.
- Configurazione per agente: modello richiesto e modello effettivamente eseguito sul desktop/laptop devono essere confrontati.
- Word: trascrizione audio riferita funzionante dall'utente, scrittura Word reale sotto approvazione ancora da collaudare su copia.
- Gmail: strumenti di lettura/ricerca/bozza presenti nel codice, integrazione account e flusso completo non ancora attestati.
- Calendario: modifiche tramite tool, idempotenza e prevenzione duplicati; distinguere notifiche consegnate e sola creazione evento.
- Memoria: riavvio, recupero, versionamento, differenza letterale/rielaborato e qualità del contesto.
- Immich/Nextcloud: servizio esterno distinto dall'integrazione agentica; eventuali aggiornamenti restano W2.
- NAS: non spostare automaticamente PostgreSQL o tutti i database. Valutare collocazione e restore per servizio.
- Test e log: una sola fonte per esito e cronologia, con versione/ambiente/provenienza, causa e dipendenze del guasto.
- Agenti distribuiti: distinta disponibilità di GPU da permessi per file/SQL, con revoca e operazioni in scrittura approvate.
- `CodeAtlas`: il programma di analisi è in sola lettura rispetto alla repository analizzata; non spacciarne la scansione euristica per analisi semantica completa.

## Cosa **non** contiene ancora questa V2

La classificazione è completa come **prima proposta concettuale**, ma i nodi non sono ancora verificati uno a uno sul server o legati tutti a funzioni del repository. Non sono ancora implementati nel visualizzatore di Direzione Cora:
- la costellazione 2D definitiva con pianeti visibili soltanto quando selezionati e scheda laterale di tutte le informazioni;
- un archivio condiviso/versionato della pianta con riconciliazione delle modifiche locali;
- il collegamento completo fra ID concettuale, file/funzione, run reali, test CI e risultati operativi sul Debian;
- la generazione semiautomatica di proposte basata su commit/PR con conferma esplicita.

Le sezioni storiche di `docs/MEMORIA_CORA.md` vanno conservate come fonte di decisioni e contesto. Questa mappa V2 **non** deve sovrascriverle né trasformare in implementazioni le idee che contengono.
