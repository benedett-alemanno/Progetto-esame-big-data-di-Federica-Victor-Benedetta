# Progetto-esame-big-data-di-Federica-Victor-Benedetta
Progetto esame di big data degli studenti Federica, Victor e Benedetta

# Progetti di Basi di Dati

Raccolta di tre script Python per la gestione di basi di dati con paradigmi diversi (relazionale, a grafo, documentale/full-text), sviluppati con dati di fantasia a scopo didattico/universitario.

## Contenuto del repository

| File | Tecnologia | Dominio |
|---|---|---|
| `scuolaguida.py` | SQLite | Gestione di un'autoscuola |
| `federazionesportiva.py` | Neo4j (grafo) | Federazione sportiva |
| `valutazioni_ds.py` | Elasticsearch | Valutazioni studenti su insegnamenti universitari |

---

## 1. `scuolaguida.py` — Database relazionale (SQLite)

Modella la gestione di un'autoscuola: tipologie di patente, candidati, istruttori, veicoli, lezioni ed esami.

**Schema:**
- `Tipologia_Patente` — categorie di patente (AM, A1, A2, A, B, BE, C, C+E, D, D+E) con età minima
- `Candidato` — anagrafica candidati, collegati alla tipologia di patente richiesta
- `Istruttore` — anagrafica istruttori
- `Veicolo` — parco veicoli (targa, modello, categoria, anno)
- `Lezione` — prenotazioni di guida (istruttore, candidato, veicolo, data/ora/durata)
- `Esame` — esiti degli esami (teorico/pratico), con punteggio solo per il teorico

Include vincoli di integrità referenziale (FOREIGN KEY) e controlli sui dati (CHECK su età minima, orari, durata lezione, punteggio).

**Dataset:** 10 tipologie patente, 30 candidati, 10 istruttori, 15 veicoli, 100 lezioni, 50 esami.

**Query incluse:**
1. Lezioni di un candidato con relativo istruttore e veicolo
2. Numero di esami superati per categoria di patente
3. Voto medio per una specifica sessione d'esame

**Esecuzione:**
```bash
pip install --break-system-packages sqlite3  # incluso nella libreria standard di Python
python scuolaguida.py
```
Lo script crea in automatico il file `autoscuola.db` nella cartella corrente.

---

## 2. `federazionesportiva.py` — Database a grafo (Neo4j)

Modella una federazione sportiva con città, competizioni, squadre, atleti e allenatori, mettendo in evidenza le relazioni dirette e indirette tra le entità.

**Modello dati:**
```
(Squadra)-[:HA_SEDE]->(Citta)
(Competizione)-[:SI_SVOLGE_A]->(Citta)
(Atleta)-[:APPARTIENE_A {dal, al}]->(Squadra)
(Atleta)-[:PARTECIPA]->(Competizione)
(Allenatore)-[:ALLENA {dal, al}]->(Squadra)
```

Le relazioni `APPARTIENE_A` e `ALLENA` sono temporalizzate (proprietà `dal`/`al`), per consentire query filtrate per periodo e per rappresentare allenatori che seguono più squadre nel corso della carriera.

**Dataset:** 100 nodi totali — 8 città, 10 competizioni, 12 squadre, 62 atleti, 8 allenatori — con distribuzione non uniforme delle partecipazioni alle competizioni per un dataset più realistico.

**Query incluse:**
1. Atleti collegati per partecipazione alle stesse competizioni
2. Città più centrali nel grafo delle competizioni (per numero di eventi ospitati)
3. Allenatori connessi indirettamente tramite atleti/competizioni
4. Relazioni indirette tra allenatori e città sportive (distinte dalla sede della squadra)
5. Percorsi tra squadre e competizioni, derivati dalla partecipazione dei singoli atleti

**Esecuzione:**
```bash
pip install --break-system-packages neo4j
```
Richiede un'istanza Neo4j attiva su `bolt://localhost:7687` (credenziali di default nello script: `neo4j`/`12345678`, da adattare al proprio ambiente). Lo script svuota il database a ogni esecuzione prima di ripopolarlo.
```bash
python federazionesportiva.py
```

---

## 3. `valutazioni_ds.py` — Ricerca full-text e analytics (Elasticsearch)

Indicizza le schede di valutazione compilate dagli studenti di un corso di data science al termine di ogni esame, ed esegue query rappresentative delle funzionalità di ricerca testuale e di aggregazione di Elasticsearch.

**Dataset:** 100 documenti (20 studenti, 10 esami/insegnamenti, fino a 10 schede per esame), ciascuno con voto di interesse, valutazione del docente, valutazione del materiale didattico e un commento libero testuale.

**Funzionalità dimostrate:**
1. Relevance scoring (BM25) su ricerca testuale nei commenti
2. Fuzzy matching (tolleranza a errori di battitura, distanza di Levenshtein)
3. Ricerca con più parole chiave, con operatore AND (co-occorrenza) e operatore OR (sinonimi, combinato con fuzzy matching)
4. Highlighting dei termini di ricerca nei risultati
5. Significant text — parole più caratteristiche di un sottoinsieme di documenti
6. Match phrase — ricerca di una frase esatta
7. Filtro strutturato per intervallo di date
8. Filtro strutturato per intervallo numerico (valutazione docente)
9. Aggregazione numerica — media dell'interesse per insegnamento

**Esecuzione:**
```bash
pip install --break-system-packages elasticsearch
```
Richiede un'istanza Elasticsearch attiva su `http://localhost:9200`. Lo script elimina e ricrea l'indice `valutazioni_ds` a ogni esecuzione.
```bash
python valutazioni_ds.py
```

---

## Note generali

- Tutti i dati (anagrafiche, città, squadre, commenti) sono fittizi e generati a scopo illustrativo.
- Ogni script è autonomo e pensato per essere eseguito singolarmente dopo aver avviato il relativo database.
- Il codice privilegia la leggibilità e l'esplicitezza (dati inseriti in modo diretto, query commentate) rispetto ad astrazioni più concise, per facilitarne la comprensione e la revisione.
