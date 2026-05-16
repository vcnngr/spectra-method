# Distributed Red/Blue Duel

## Scopo

Distributed Red/Blue Duel descrive come SPECTRA supporta esercizi Red/Blue su macchine, sessioni o operatori separati. Il modello serve a misurare detection, mitigation e coordinamento senza confondere i ruoli e senza trasformare l'esercizio in anti-forensics.

Il design e' volutamente ledger-first:

- Red registra attivita' e intenzioni nel proprio ledger;
- Blue registra telemetria, detection, mitigazioni e miss nel proprio ledger;
- Referee importa entrambi i ledger, correla eventi e produce scorecard;
- nessun ruolo modifica retroattivamente il ledger dell'altro.

## Ruoli

### Red

Red opera come emulatore di avversario autorizzato. Deve lavorare entro engagement, scope e RoE. In Duel Mode Red non riceve una licenza a cancellare tracce o disabilitare difese: modella OPSEC come riduzione del rumore, controllo del footprint e scelta di timing o tecnica misurabile.

Eventi tipici:

- `planned_action`: azione prevista o ipotesi operativa;
- `action`: azione eseguita entro scope;
- `observation`: risultato osservato da Red;
- `handoff`: informazione consegnata a Referee o fase successiva.

### Blue

Blue opera come difensore. Osserva telemetria, valida detection, propone mitigazioni e registra miss quando un segnale non viene rilevato. Blue Live Adapter puo' alimentare il ledger da log locali in modalita' read-only.

Eventi tipici:

- `observation`: segnale o contesto osservato;
- `detection`: rilevamento con tecnica, target, fonte e confidenza;
- `mitigation`: controllo o risposta applicata;
- `miss`: attivita' Red non rilevata o rilevata tardi;
- `handoff`: passaggio verso IRT, GRC o Referee.

### Referee

Referee mantiene la vista di correlazione. Non sostituisce Red o Blue, ma confronta eventi, timestamp, target e tecniche per produrre uno scorecard.

Eventi tipici:

- `checkpoint`: stato dell'esercizio;
- `correlation`: mapping tra evento Red ed evento Blue;
- `decision`: scelta di scoring o interpretazione;
- `score`: risultato intermedio o finale.

## Visibilita' separata

La separazione e' parte del modello. Red vede il proprio piano, le proprie azioni e lo scope condiviso. Blue vede telemetria, alert, controlli e proprie detection. Referee puo' leggere entrambi per scoring.

Questa separazione evita due errori:

- Blue che rileva per conoscenza artificiale del piano Red;
- Red che ottimizza contro dettagli Blue non disponibili in un esercizio reale.

Il formato ledger-only rende la separazione semplice da ispezionare: ogni evento ha ruolo, tipo, summary, timestamp, target, tecnica, fonte, confidenza, severita' e artefatti.

## Flusso operativo

1. Creare o verificare un engagement autorizzato.
2. Inizializzare sessione Duel per Red, Blue e Referee con lo stesso `session_id`.
3. Generare un piano Party Mode v2 con lane esplicite quando il lavoro richiede piu' prospettive:

```bash
spectra party plan --topic "distributed duel readiness" --mode purple --lanes red,blue,irt,grc,core
```

4. Far registrare a Red attivita' pianificate o osservate entro RoE.
5. Far registrare a Blue osservazioni, detection, mitigazioni e miss.
6. Usare Blue Live/Blue Tail, se utile, per ingest read-only di log difensivi.
7. Esportare i ledger locali con Red/Blue Broker quando i ruoli girano su macchine diverse.
8. Importare i bundle nel workspace Referee.
9. Far produrre al Referee correlazioni e scorecard.
10. Trasferire risultati verso report, backlog di detection, piano di mitigazione o follow-up IRT/GRC.

Party Mode v2 non esegue azioni. Produce contratti di lavoro per sub-agent: input richiesti, output obbligatori, criteri di completamento, quality gate e merge contract. Questo rende esplicito cosa deve consegnare ogni lane prima che il Referee o Chronicle producano sintesi e report.

## Blue Live e Blue Tail

Blue Live Adapter legge sorgenti difensive locali e normalizza eventi Blue. Le sorgenti supportate dal runtime corrente includono log tipo `auth`, `nginx_access`, `nginx_error`, `postfix`, `dovecot`, `fail2ban`, `suricata_eve`, `wazuh`, `zeek_conn`, `zeek_dns` e `zeek_http`.

Blue Tail aggiunge checkpoint. Quando viene eseguito in modalita' tail, legge solo la parte nuova dei file gia' processati. Questo permette run ripetute senza duplicare detection vecchie. Le righe finali incomplete restano in sospeso fino all'arrivo di una newline, cosi' il ledger non contiene detection troncate.

Vincolo importante: Blue Live e Blue Tail sono read-only. Non cancellano, ruotano, riscrivono o correggono log. Non applicano firewall rule, non riavviano servizi, non modificano host.

## Red/Blue Broker

Red/Blue Broker consente lo scambio offline dei ledger tra macchine separate. Ogni ruolo esporta un bundle JSON dal proprio ledger locale:

```bash
spectra broker export --session ENG-2026-001 --role red --bundle red-bundle.json
spectra broker export --session ENG-2026-001 --role blue --bundle blue-bundle.json
```

Il Referee importa i bundle nel proprio workspace:

```bash
spectra broker import --session ENG-2026-001 --role red --bundle red-bundle.json
spectra broker import --session ENG-2026-001 --role blue --bundle blue-bundle.json
spectra duel score --session ENG-2026-001 --output scorecard.md
```

Ogni bundle contiene tipo, versione schema bundle, versione schema evento, sessione, ruolo, timestamp di export, eventi e checksum SHA256 del payload eventi. L'import verifica checksum, event count, sessione, ruolo, schema bundle, schema evento e campi minimi. I campi evento non riconosciuti vengono scartati prima di scrivere il ledger, poi gli eventi gia' presenti vengono deduplicati.

Il broker non apre socket, non esegue listener, non installa agenti remoti e non controlla host. E' un meccanismo esplicito di scambio file, adatto a Red e Blue realmente separati.

## Scorecard

La scorecard deve restare spiegabile. Ogni punteggio deve poter essere ricondotto a eventi ledger.

Metriche raccomandate:

- detection latency: tempo tra azione Red e detection Blue correlata;
- severity coverage: quota di eventi Red rilevati per severita';
- technique misses: tecniche non rilevate o rilevate con bassa confidenza;
- mitigation coverage: eventi con risposta o controllo applicato;
- outcome grade: sintesi finale derivata dalle metriche, non da impressioni.

Quando manca una correlazione, Referee deve distinguere tra:

- nessuna telemetria disponibile;
- telemetria disponibile ma non analizzata;
- detection assente;
- detection presente ma non collegata alla tecnica corretta;
- mitigazione presente ma tardiva o incompleta.

## Guardrail di scope

Duel Mode non indebolisce i controlli SPECTRA. Ogni evento Red deve restare dentro scope e RoE. Ogni evento Blue deve indicare fonte e target osservato. Referee deve segnalare qualunque mismatch tra ledger e scope.

Esempi di violazione:

- Red registra azione su target escluso;
- Red propone tecnica non autorizzata dalle RoE;
- Blue importa log di sistemi non autorizzati senza contesto;
- Referee assegna score senza evento correlabile.

## Confine safety

Il modello ammette OPSEC come misura, non come cancellazione di evidenza.

Comportamenti vietati:

- cancellare, alterare o nascondere log;
- manomettere audit trail;
- disabilitare EDR, SIEM, auditd, Sysmon, Defender o logging;
- fare cleanup distruttivo;
- rimuovere artefatti per impedire detection;
- creare persistenza non autorizzata.

Comportamenti ammessi entro autorizzazione:

- pianificare attivita' low-and-slow;
- misurare quanto rumore produce una tecnica;
- confrontare tecniche per detection coverage;
- registrare footprint e sorgenti di telemetria;
- validare regole di detection;
- proporre mitigazioni;
- produrre scorecard e backlog di miglioramento.

Il risultato atteso non e' "Red invisibile". Il risultato atteso e' una misura onesta: quali segnali sono stati prodotti, quali Blue ha visto, quali sono mancati, quali controlli hanno funzionato e quali vanno migliorati.
