# Origine red-blue-team

## Scopo

La directory `red-blue-team` e' lo spazio di incubazione da cui e' emerso `spectra-method`. Non e' il pacchetto pubblico, non e' la sorgente canonica installabile, e non va trattata come runtime stabile. E' un corpus di analisi, prototipi, prove di architettura e materiale di riferimento usato per definire il modello SPECTRA.

Il suo valore principale e' storico e progettuale:

- conserva le prime decisioni su agenti, workflow, moduli e stile operativo;
- mostra come i pattern BMAD sono stati studiati e riadattati;
- contiene esempi utili per capire perche' SPECTRA separa Red, Blue, IRT, GRC e Core;
- fornisce confronto quando si valuta se una feature nuova rispetta l'intento originale.

## Relazione con BMAD

SPECTRA nasce riusando concetti di orchestrazione multi-agente gia' presenti in BMAD, non copiando il dominio BMAD. Dal lato BMAD sono stati presi soprattutto pattern strutturali:

- agenti con identita', ruolo, principi e capacita' dichiarate;
- workflow a step con caricamento progressivo;
- Party Mode come conversazione multi-prospettiva;
- manifest e registri per rendere agenti e skill scopribili;
- separazione tra coordinamento, esecuzione, output e validazione.

SPECTRA adatta questi pattern a operazioni cybersecurity autorizzate. La trasformazione principale e' il passaggio da orchestrazione generica a orchestrazione vincolata da engagement, scope, RoE, evidenza e responsabilita' operativa.

In SPECTRA Red, Blue, IRT e GRC non sono personaggi decorativi. Sono domini di lavoro distinti:

- Red valuta percorsi di attacco entro scope e RoE;
- Blue analizza telemetria, controlli, detection e mitigazioni;
- IRT gestisce triage, contenimento, forensics, malware e recovery;
- GRC traduce rischio tecnico in governance, audit, policy e decisioni business;
- Core mantiene engagement, evidence chain, reportistica e coordinamento.

## Relazione con spectra-method

`spectra-method` e' la versione productized del lavoro nato in `red-blue-team`. E' il pacchetto npm/GitHub versionato, installabile e validato. Deve essere considerato la fonte di verita' per:

- struttura distributiva del framework;
- CLI e installazione;
- manifest e configurazione pubblica;
- workflow e skill da installare nei progetti consumer;
- runtime di supporto come Party Mode, Duel Mode e Blue Live Adapter;
- test, validazione e compatibilita' del pacchetto.

`red-blue-team` resta una reference corpus. Puo' spiegare l'intento, ma non deve sovrascrivere cio' che `spectra-method` ha gia' consolidato in package, test e CLI. Quando c'e' divergenza, il comportamento del pacchetto versionato vince; il corpus originario serve per capire se la divergenza e' voluta o se indica debito progettuale.

## Relazione con spectra-playground

`spectra-playground` e' un esempio consumer e testbed. Rappresenta una installazione che usa SPECTRA in un contesto pratico, con engagement, guide operative e dati di prova. Non e' la sorgente di verita' del framework.

Usarlo per:

- verificare ergonomia di installazione e uso;
- provare flussi end-to-end;
- osservare come un progetto consumer struttura engagement e output;
- raccogliere feedback su documentazione e CLI.

Non usarlo per:

- definire API canoniche;
- cambiare contratti di manifest;
- decidere policy safety globali;
- sostituire test o validazione del pacchetto.

## Concetti architetturali correnti

### Party Mode

Party Mode e' il planner multi-agente. Produce piani deterministici per far lavorare agenti SPECTRA in parallelo o in confronto controllato. Non esegue automaticamente azioni offensive: assegna lane, contratti di task, output attesi, profili modello e safety gate.

La funzione principale e' trasformare una domanda complessa in lavoro coordinato tra prospettive Red, Blue e Purple. Ogni piano deve restare legato a engagement, autorizzazione, scope e RoE.

### Duel Mode

Duel Mode modella esercizi Red/Blue distribuiti. Red, Blue e Referee hanno viste separate e ledger locali. Red registra intenzioni, azioni pianificate, osservazioni e handoff. Blue registra osservazioni, detection, mitigazioni, miss e handoff. Referee correla i ledger e produce scorecard.

Il punto chiave e' la separazione: Red e Blue non condividono tutto lo stato. Il Referee ha il compito di correlare evidenze e misurare se Blue ha rilevato o mitigato attivita' Red entro tempi e copertura accettabili.

### Blue Live e Blue Tail

Blue Live Adapter importa telemetria difensiva in modo read-only e la normalizza in eventi Blue. Blue Tail usa checkpoint per leggere solo nuovi byte dai log gia' visti, evitando duplicati nelle run successive.

Questi componenti non modificano log, servizi, firewall, host o configurazioni. Sono strumenti di ingestione e normalizzazione per alimentare il ledger Blue.

### Separazione ledger-only

Duel Mode e Blue Live sono ledger-only. Il framework registra eventi e correlazioni, non fornisce procedure per alterare artefatti, cancellare tracce o manipolare controlli. La separazione Red/Blue vive nei ledger e nei contratti di visibilita', non in tecniche anti-forensi.

### Scorecard

Le scorecard misurano l'esercizio. Metriche tipiche:

- latenza di detection;
- copertura per severita';
- miss per tecnica;
- mitigazioni osservate;
- grado finale dell'esito.

La scorecard non e' un giudizio narrativo libero. Deve derivare da eventi ledger, timestamp, tecnica, target, severita', confidenza e correlazioni esplicite.

### Scope guardrails

Ogni operazione SPECTRA parte da engagement e scope. Red non deve agire fuori RoE. Blue e IRT devono distinguere sistemi in scope, sistemi correlati e sistemi esclusi. GRC deve evitare policy o audit fuori perimetro.

I guardrail non sono burocrazia: sono il confine che rende l'operazione autorizzata, ripetibile e difendibile.

## Confine safety

SPECTRA deve modellare comportamento Red come misurazione di OPSEC, rumore e footprint, non come anti-forensics distruttiva.

Vietato:

- cancellazione o alterazione di log;
- manomissione di audit trail;
- cleanup distruttivo;
- disabilitazione di EDR, SIEM, auditd, Sysmon, Defender o logging;
- persistenza non autorizzata;
- istruzioni per nascondere evidenza a Blue o IRT.

Ammesso entro engagement autorizzato:

- pianificazione low-and-slow entro RoE;
- misura del footprint generato;
- budget di rumore;
- challenge di attribuzione;
- analisi di telemetria difensiva;
- detection engineering;
- mitigazioni e raccomandazioni Blue;
- correlazione Referee e scorecard.

Il principio e' semplice: Red puo' produrre segnali misurabili; Blue deve poterli osservare, rilevare o mitigare; il Referee deve poterli correlare. Nessuna parte del framework deve normalizzare cancellazione di prove o indebolimento dei controlli di sicurezza.

