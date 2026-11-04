> **Aggiornamento 3 novembre 2026 — V2 completa:** questa pagina conserva la ricostruzione storica *parziale* dell'altra conversazione. La classificazione estesa e riconciliata (45 stelle, pianeti, lune, 37 link) è in [CORA_MAPPA_V2_COMPLETA.md](CORA_MAPPA_V2_COMPLETA.md) e la consegna per Work è in [CORA_WORK_HANDOFF.md](CORA_WORK_HANDOFF.md). Gli ID degli appunti precedenti sono conservati nella [pianta V2](../cora-plan.json); **non interpretare la parola “parziale” nelle sezioni storiche come stato dell'attuale mappa completa**. I collaudi reali del software restano separati dalla classificazione.

# Cora in CodeAtlas · consegna alle prossime conversazioni

**3 novembre 2026 · Ricostruzione parziale.** Per riprendere il lavoro leggere questo documento e `cora-plan.json` sul branch `progetti/cora-serveria` di Aleselva12/qwe. Il programma da comprendere è Aleselva12/serveria1. La pianta registra intenzioni e scelte di direzione. Le condizioni operative di Cora richiedono una verifica distinta. Le foto inviate mostrano l’uso di Atlas e non costituiscono una lista di difetti.

## Decisioni di Alessandro

- L’analogia guida è la pianta di una casa: comprendere tutto ciò che si è discusso di costruire, anche se una funzionalità ha zero file. Distingui idea, obiettivo scelto, lavoro in corso, implementazione ed evidenza di funzionamento.
- La scansione tecnica è utile per IA/programmatore e per rintracciare prove. La vista di direzione serve ad Alessandro per scegliere dove intervenire. Un ramo merita autonomia quando più stelle hanno senso viste insieme. Possono essere tappe consecutive oppure lavori paralleli.
- Stella = punto importante per la funzione del ramo; pianeta = sottofunzione, implementazione successiva o aggiunta; luna = ulteriore dettaglio. Evitare la sovrappopolazione. Trenta o quaranta stelle possono avere senso se aiutano a decidere: non sono un obiettivo numerico. Pianeti e lune si esplorano entrando nella stella.
- Promozioni, accorpamenti, biforcazioni e ricollocazioni devono conservare identità, figli e storia. Il numero di lune suggerisce una revisione, non decide il livello. Evitare sette biforcazioni corte quando un ramo con stelle parallele risulta più leggibile.
- Tronco unico e stabile per responsabilità generali. Una capacità comune può starci già quando un solo ramo la usa. Collegare le singole stelle ai componenti effettivamente pertinenti. Radici per macchine, dati, dipendenze/librerie, modelli, ambiente e requisiti.
- Priorità crescente: verde tutto ok, giallo aggiornamento pianificato, arancio malfunzionamento minore, rosso problema. Grigio per punti da valutare e placeholder. Conservare la distinzione tra idea futura e capacità attuale non ancora verificata. La priorità di ogni punto è esplicita; la politica di propagazione al genitore resta aperta.
- La pianta cambia per decisioni o progressi rilevanti. Commit, merge request, lavoro di altri e test possono suggerire aggiornamenti. La riclassificazione della pianta passa per una scelta esplicita. Un assistente esterno può preparare una proposta condivisibile; un LLM integrato non è un prerequisito.

## Applicazione a Cora · parziale

Lo schema V2 della conversazione **Pianifica macroobiettivi futuri** è una proposta di lavoro. Alessandro ha chiesto di distinguere R4 ambiente operativo presente, R5 affidabilità della base e ha prospettato R6 sicurezza. Ha chiesto più punti nel tronco oltre T5 e un ramo G esclusivamente per il programmatore. La nomenclatura R1–R6, T1–T13 e A–G nel JSON serve da base di confronto, non attesta che ogni collocazione sia approvata o implementata. L’elenco di stelle, pianeti, lune e collegamenti è incompleto. In particolare per F è riportata soltanto la parte recuperata con sufficiente chiarezza.

- **Worker.** Una stella per far lavorare insieme più macchine. Collegare un dispositivo e assegnargli lavoro sono pianeti. Selezione modello, disponibilità e uso da parte degli agenti sono candidati da approfondire. La prova che un desktop risponde all’inferenza e quella che un agente lo sceglie per un lavoro sono verifiche diverse.
- **Calendario.** Il risultato atteso è poter dire un appuntamento, ritrovarlo una sola volta nel calendario e riceverne la notifica sul telefono. Interpretazione del modello, tool/scrittura e consegna della notifica sono punti importanti; il livello preciso dipende dal ramo scelto. L’organizzazione automatica della settimana e il calendario digitale in camera via API sono possibilità future discusse.
- **Programmi esterni.** Immich, Nextcloud e Magazzino Tele sono stelle parallele. Preventivi e CodeAtlas figurano nella proposta estesa. Software mantenuto altrove può comunque far parte della pianta. Per approfondirlo occorre distinguere l’applicazione esterna, la sua integrazione con Cora e il risultato atteso dall’utente.
- **Orizzonte temporale.** Nessun ramo generico “futuro”. I placeholder grigi restano nel ramo cui appartengono. M3 tende all’inizio dei rami e M4 alle estremità: indicazione di lettura, non regola meccanica. La “terza dimensione” desiderata è la scheda della stella con passato (resoconti e commit pertinenti), presente (scopo, uso, prove, problemi) e futuro (piani e obiettivi).

## Cosa esiste e cosa manca

| Tema | Situazione sul branch Cora |
| --- | --- |
| Direzione Cora | Pianta v1 editabile con gerarchia, priorità, spostamento dei sottoalberi, collegamenti al tronco, import/export e salvataggio locale. La pagina di direzione presenta oggi un elenco espandibile. |
| Aspetto desiderato | **Parziale.** Costellazione 2D su sfondo scuro, nodi colorati, linee e pannello fisso a destra. La vista tecnica già offre una rappresentazione grafica. La pianta di direzione deve ancora offrire questa esperienza completa. |
| Evidenze, profili e viste | Nel visualizzatore tecnico esistono profili, mappa funzionale, grafo, livelli, matrice, struttura file, import JUnit/JSON e associazioni test. **Parziale** il raccordo con le stelle della pianta. Un test verde copre il suo caso specifico. |
| Storia e futuro per stella | **Parziale.** La scheda tecnica ha una timeline e la pianta ha note e obiettivi testuali. Restano da collegare versioni precedenti, prove e piani futuri alla stessa identità di direzione. |
| Proposte semiautomatiche | **Parziale.** Su main Direzione progetto suggerisce componenti dalla scansione, da confermare. Sul branch Cora la pianta parte dal JSON dedicato. L’aggiornamento delle stelle da commit/merge request non è attestato. |
| Collaudi e uso in Cora | Restano da documentare il collaudo visivo in browser reale, i tre casi semplice/medio/complesso simile a ServerIA e l’integrazione nella Home di Cora. La prova manuale sulle schermate non completa questi collaudi. |

## Procedura per chi riprende

1. Identificare branch e commit di Atlas e di serveria1. Confrontare la pianta con la repository, la Roadmap e le decisioni dell’utente. Registrare la fonte e i dubbi per punto.
2. Proporre integrazioni per ID stabile. Separare quanto deciso da Alessandro dalle proposte dell’assistente; marcare “parziale” una ricostruzione incompleta. Nessuna priorità positiva si deduce dalla sola presenza di file, import o test.
3. Valutare i risultati trasversali usando prove pertinenti, per esempio un unico appuntamento e la consegna sul telefono. Registrare anche ciò che manca. Sottoporre ad Alessandro i cambiamenti che alterano il significato dei rami.
4. Se esiste già una pianta locale, esportarla prima di importare il JSON aggiornato: la copia del browser prevale sulla base della repository. Confrontare e conservare le personalizzazioni. Promuovere su main soltanto le idee riutilizzabili dopo una decisione separata.

**Traccia delle fonti.** Decisioni e casi guida provengono dalla conversazione Informatica sulle viste alternative e dalla discussione “Ricostruire la richiesta”. La proposta V2 e i vincoli R4/R5/R6, G, placeholder e orizzonte M3/M4 provengono da “Pianifica macroobiettivi futuri”. Il codice del branch è la fonte per le funzioni di Atlas. Questa consegna non sostituisce l’analisi accurata di serveria1 prevista da Alessandro.
