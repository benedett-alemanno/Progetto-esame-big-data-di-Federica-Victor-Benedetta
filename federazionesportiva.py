"""
Gestione di un database a grafo (Neo4j) per una federazione sportiva
(dati di fantasia).

Modello dati:
    (:Citta {name})
    (:Competizione {name, date})
    (:Squadra {name, cat})
    (:Atleta {name})
    (:Allenatore {name})

Relazioni:
    (Squadra)-[:HA_SEDE]->(Citta)
    (Competizione)-[:SI_SVOLGE_A]->(Citta)
    (Atleta)-[:APPARTIENE_A {dal, al}]->(Squadra)
    (Atleta)-[:PARTECIPA]->(Competizione)
    (Allenatore)-[:ALLENA {dal, al}]->(Squadra)

Note sul modello:
- La citta' e' sempre un nodo proprio, mai una stringa annidata:
    le squadre vi sono collegate tramite HA_SEDE, le competizioni
    tramite SI_SVOLGE_A.
- ALLENA ha temporalita' (dal, al) come APPARTIENE_A: un allenatore
    puo' aver guidato piu' squadre in periodi diversi della carriera.
    Con 8 allenatori per 12 squadre, alcuni allenatori coprono piu'
    squadre nel tempo cosi' che tutte le squadre risultino allenate.
- APPARTIENE_A: anche questa relazione ha proprietà {dal, al} per r
    egistrare il periodo di appartenenza dell'atleta alla squadra.
    Nel dataset attuale ogni atleta è legato a una sola squadra
    (la traccia non richiede cambi di squadra per gli atleti),
    ma la temporalità è comunque modellata per coerenza con
    ALLENA e per consentire query filtrate per anno.
- La distribuzione di PARTECIPA e' non uniforme (4 atleti su 62 non
    hanno competizioni, la maggioranza ne ha 1-2, pochi arrivano a 3)
    per un dataset piu' realistico.

Dataset: 100 nodi totali
    8 Citta + 10 Competizioni + 12 Squadre + 62 Atleti + 8 Allenatori

Queries:
    1. atleti collegati per partecipazione alle stesse competizioni
    2. citta' piu' centrali nel grafo delle competizioni
    3. allenatori connessi indirettamente tramite atleti/competizioni
    4. relazioni indirette tra allenatori e citta' sportive
    5. percorsi tra squadre e competizioni (derivati dagli atleti)

Nota su Query 4 (allenatori e città): la query segue il percorso
indiretto Allenatore → Squadra → Atleta → Competizione → Città,
restituendo le città sportive raggiunte tramite le competizioni
dei propri atleti. Questo è distinto dal percorso diretto
Allenatore → Squadra → HA_SEDE → Città (sede della squadra),
che rappresenta una relazione diretta e non indiretta. La Query 4
copre intenzionalmente solo il secondo caso, in linea con il
requisito della traccia ("relazioni indirette tra allenatori e città sportive").

La connessione al driver viene aperta una sola volta in main(); ogni
funzione apre la propria sessione con "with driver.session(...) as
session:" cosi' la sessione si chiude automaticamente senza dover
gestire manualmente session.close().
"""

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "12345678")
DATABASE = "neo4j"


# ---------------------------------------------------------------------------
# CREAZIONE NODI
# ---------------------------------------------------------------------------
def crea_nodi(driver):
    """Crea tutti i nodi del grafo: Citta, Competizione, Squadra, Atleta, Allenatore."""

    citta = [
        "Roma", "Milano", "Torino",
        "Napoli", "Bologna", "Firenze",
        "Genova", "Bari",
    ]

    competizioni = [
        {"name": "Campionato Nazionale", "date": "2026-05-10"},
        {"name": "Coppa Regionale",      "date": "2026-06-01"},
        {"name": "Coppa Italia",          "date": "2026-07-01"},
        {"name": "Torneo Primavera",      "date": "2026-03-15"},
        {"name": "Trofeo Estivo",         "date": "2026-07-20"},
        {"name": "Challenge City",        "date": "2026-04-12"},
        {"name": "Supercoppa",            "date": "2026-08-10"},
        {"name": "Memorial Bianchi",      "date": "2026-02-20"},
        {"name": "Coppa Disciplina",      "date": "2025-11-15"},
        {"name": "Torneo Citta",          "date": "2026-09-05"},
    ]

    # cat = categoria (livello agonistico)
    squadre = [
        {"name": "Lions",    "cat": "Senior"},
        {"name": "Tigers",   "cat": "Junior"},
        {"name": "Sharks",   "cat": "Senior"},
        {"name": "Eagles",   "cat": "Junior"},
        {"name": "Wolves",   "cat": "Senior"},
        {"name": "Panthers", "cat": "Junior"},
        {"name": "Falcons",  "cat": "Senior"},
        {"name": "Bears",    "cat": "Junior"},
        {"name": "Hawks",    "cat": "Senior"},
        {"name": "Cobras",   "cat": "Junior"},
        {"name": "Bulls",    "cat": "Senior"},
        {"name": "Foxes",    "cat": "Junior"},
    ]

    # 62 atleti con nomi italiani comuni
    atleti = [
        "Pietro Moretti",    "Sofia Verdi",       "Elisa Fontana",
        "Davide Santoro",    "Aurora Rossi",      "Matteo Longo",
        "Federica Longo",    "Sofia Romano",      "Matteo Colombo",
        "Nicola Barbieri",   "Valentina Martini", "Camilla Romano",
        "Silvia Santini",    "Matteo Conti",      "Edoardo Martini",
        "Nicola Martini",    "Matteo Greco",      "Valentina Romano",
        "Sofia Rinaldi",     "Luca Ferrara",      "Camilla Gallo",
        "Giorgia Martini",   "Laura Bianchi",     "Laura Moretti",
        "Sofia Bianchi",     "Martina Lombardi",  "Beatrice Greco",
        "Edoardo Ferrara",   "Gabriele Rossi",    "Silvia Longo",
        "Simone Galli",      "Elena Esposito",    "Marco Caruso",
        "Luca Greco",        "Silvia Costa",      "Nicola Conti",
        "Giorgia Costa",     "Sara Costa",        "Chiara Colombo",
        "Matteo Santoro",    "Riccardo Lombardi", "Aurora Lombardi",
        "Anna Lombardi",     "Riccardo Marino",   "Riccardo Galli",
        "Elisa Romano",      "Andrea Mancini",    "Laura Longo",
        "Giorgia Leone",     "Gabriele Longo",    "Davide Ferrara",
        "Simone Ricci",      "Francesco Gallo",   "Federica Santoro",
        "Edoardo Esposito",  "Edoardo Galli",     "Nicola Costa",
        "Simone Lombardi",   "Giorgia Galli",     "Martina Moretti",
        "Pietro Martini",    "Gabriele Esposito",
    ]

    allenatori = [
        "Giorgio Colombo", "Roberto Romano",  "Giuseppe Greco",
        "Stefano Ricci",   "Fabio Rossi",     "Paolo Ferrari",
        "Vittorio Marino", "Massimo Bianchi",
    ]

    with driver.session(database=DATABASE) as session:
        for nome in citta:
            session.run("CREATE (:Citta {name: $name})", name=nome)

        for comp in competizioni:
            session.run(
                "CREATE (:Competizione {name: $name, date: $date})",
                name=comp["name"], date=comp["date"]
            )

        for sq in squadre:
            session.run(
                "CREATE (:Squadra {name: $name, cat: $cat})",
                name=sq["name"], cat=sq["cat"]
            )

        for nome in atleti:
            session.run("CREATE (:Atleta {name: $name})", name=nome)

        for nome in allenatori:
            session.run("CREATE (:Allenatore {name: $name})", name=nome)

    print(f"Creati: {len(citta)} Citta, {len(competizioni)} Competizione, "
          f"{len(squadre)} Squadra, {len(atleti)} Atleta, {len(allenatori)} Allenatore")
    print(f"Totale nodi: {len(citta)+len(competizioni)+len(squadre)+len(atleti)+len(allenatori)}")


# ---------------------------------------------------------------------------
# CREAZIONE RELAZIONI
# ---------------------------------------------------------------------------
def crea_relazioni(driver):
    """Crea tutte le relazioni: HA_SEDE, SI_SVOLGE_A, APPARTIENE_A, PARTECIPA, ALLENA."""

    ha_sede = [
        # (squadra, citta) — due citta' ospitano due squadre ciascuna
        ("Lions",    "Roma"),    ("Tigers",   "Milano"),
        ("Sharks",   "Napoli"),  ("Eagles",   "Torino"),
        ("Wolves",   "Bologna"), ("Panthers", "Firenze"),
        ("Falcons",  "Genova"),  ("Bears",    "Bari"),
        ("Hawks",    "Roma"),    ("Cobras",   "Milano"),
        ("Bulls",    "Napoli"),  ("Foxes",    "Torino"),
    ]

    si_svolge_a = [
        # Roma e' la citta' piu' centrale (3 competizioni)
        ("Campionato Nazionale", "Roma"),
        ("Challenge City",       "Roma"),
        ("Supercoppa",           "Roma"),
        # Milano: 3 competizioni
        ("Coppa Regionale",      "Milano"),
        ("Coppa Italia",         "Milano"),
        ("Memorial Bianchi",     "Milano"),
        # Altre citta'
        ("Torneo Primavera",     "Torino"),
        ("Trofeo Estivo",        "Napoli"),
        ("Campionato Nazionale", "Napoli"),   # multi-sede
        ("Memorial Bianchi",     "Bologna"),  # multi-sede
        ("Coppa Disciplina",     "Firenze"),
        ("Torneo Citta",         "Bari"),
        ("Torneo Citta",         "Genova"),
    ]

    appartiene_a = [
        # (atleta, squadra, dal, al)
        # Lions (7 atleti)
        ("Pietro Moretti",    "Lions",    2023, 2026),
        ("Sofia Verdi",       "Lions",    2021, 2026),
        ("Elisa Fontana",     "Lions",    2022, 2026),
        ("Davide Santoro",    "Lions",    2022, 2026),
        ("Aurora Rossi",      "Lions",    2022, 2026),
        ("Matteo Longo",      "Lions",    2021, 2026),
        ("Federica Longo",    "Lions",    2020, 2026),
        # Tigers (4 atleti)
        ("Sofia Romano",      "Tigers",   2019, 2026),
        ("Matteo Colombo",    "Tigers",   2021, 2026),
        ("Nicola Barbieri",   "Tigers",   2022, 2026),
        ("Valentina Martini", "Tigers",   2019, 2026),
        # Sharks (6 atleti)
        ("Camilla Romano",    "Sharks",   2019, 2026),
        ("Silvia Santini",    "Sharks",   2022, 2026),
        ("Matteo Conti",      "Sharks",   2022, 2026),
        ("Edoardo Martini",   "Sharks",   2019, 2026),
        ("Nicola Martini",    "Sharks",   2023, 2026),
        ("Matteo Greco",      "Sharks",   2024, 2026),
        # Eagles (5 atleti)
        ("Valentina Romano",  "Eagles",   2024, 2026),
        ("Sofia Rinaldi",     "Eagles",   2019, 2026),
        ("Luca Ferrara",      "Eagles",   2020, 2026),
        ("Camilla Gallo",     "Eagles",   2020, 2026),
        ("Giorgia Martini",   "Eagles",   2023, 2026),
        # Wolves (4 atleti)
        ("Laura Bianchi",     "Wolves",   2021, 2026),
        ("Laura Moretti",     "Wolves",   2019, 2026),
        ("Sofia Bianchi",     "Wolves",   2020, 2026),
        ("Martina Lombardi",  "Wolves",   2019, 2026),
        # Panthers (6 atleti)
        ("Beatrice Greco",    "Panthers", 2023, 2026),
        ("Edoardo Ferrara",   "Panthers", 2022, 2026),
        ("Gabriele Rossi",    "Panthers", 2023, 2026),
        ("Silvia Longo",      "Panthers", 2023, 2026),
        ("Simone Galli",      "Panthers", 2023, 2026),
        ("Elena Esposito",    "Panthers", 2020, 2026),
        # Falcons (3 atleti)
        ("Marco Caruso",      "Falcons",  2023, 2026),
        ("Luca Greco",        "Falcons",  2022, 2026),
        ("Silvia Costa",      "Falcons",  2022, 2026),
        # Bears (5 atleti)
        ("Nicola Conti",      "Bears",    2022, 2026),
        ("Giorgia Costa",     "Bears",    2021, 2026),
        ("Sara Costa",        "Bears",    2023, 2026),
        ("Chiara Colombo",    "Bears",    2022, 2026),
        ("Matteo Santoro",    "Bears",    2021, 2026),
        # Hawks (6 atleti)
        ("Riccardo Lombardi", "Hawks",    2023, 2026),
        ("Aurora Lombardi",   "Hawks",    2023, 2026),
        ("Anna Lombardi",     "Hawks",    2019, 2026),
        ("Riccardo Marino",   "Hawks",    2023, 2026),
        ("Riccardo Galli",    "Hawks",    2024, 2026),
        ("Elisa Romano",      "Hawks",    2019, 2026),
        # Cobras (4 atleti)
        ("Andrea Mancini",    "Cobras",   2020, 2026),
        ("Laura Longo",       "Cobras",   2024, 2026),
        ("Giorgia Leone",     "Cobras",   2020, 2026),
        ("Gabriele Longo",    "Cobras",   2021, 2026),
        # Bulls (7 atleti)
        ("Davide Ferrara",    "Bulls",    2024, 2026),
        ("Simone Ricci",      "Bulls",    2019, 2026),
        ("Francesco Gallo",   "Bulls",    2020, 2026),
        ("Federica Santoro",  "Bulls",    2020, 2026),
        ("Edoardo Esposito",  "Bulls",    2020, 2026),
        ("Edoardo Galli",     "Bulls",    2023, 2026),
        ("Nicola Costa",      "Bulls",    2019, 2026),
        # Foxes (5 atleti)
        ("Simone Lombardi",   "Foxes",    2020, 2026),
        ("Giorgia Galli",     "Foxes",    2019, 2026),
        ("Martina Moretti",   "Foxes",    2022, 2026),
        ("Pietro Martini",    "Foxes",    2022, 2026),
        ("Gabriele Esposito", "Foxes",    2024, 2026),
    ]

    partecipa = [
        # (atleta, competizione) — distribuzione non uniforme:
        # 4 atleti senza competizioni (Silvia Santini, Edoardo Martini,
        # Giorgia Costa, Riccardo Marino), la maggioranza con 1-2,
        # pochi con 3, per un dataset piu' realistico.
        ("Pietro Moretti",    "Trofeo Estivo"),
        ("Pietro Moretti",    "Campionato Nazionale"),
        ("Sofia Verdi",       "Trofeo Estivo"),
        ("Elisa Fontana",     "Memorial Bianchi"),
        ("Elisa Fontana",     "Coppa Regionale"),
        ("Davide Santoro",    "Trofeo Estivo"),
        ("Davide Santoro",    "Torneo Primavera"),
        ("Aurora Rossi",      "Coppa Disciplina"),
        ("Matteo Longo",      "Coppa Italia"),
        ("Federica Longo",    "Coppa Italia"),
        ("Federica Longo",    "Coppa Regionale"),
        ("Federica Longo",    "Campionato Nazionale"),
        ("Sofia Romano",      "Trofeo Estivo"),
        ("Matteo Colombo",    "Torneo Citta"),
        ("Matteo Colombo",    "Trofeo Estivo"),
        ("Nicola Barbieri",   "Memorial Bianchi"),
        ("Valentina Martini", "Supercoppa"),
        ("Valentina Martini", "Trofeo Estivo"),
        ("Camilla Romano",    "Memorial Bianchi"),
        ("Camilla Romano",    "Torneo Citta"),
        ("Edoardo Martini",   "Challenge City"),
        ("Nicola Martini",    "Campionato Nazionale"),
        ("Nicola Martini",    "Coppa Regionale"),
        ("Matteo Greco",      "Torneo Citta"),
        ("Valentina Romano",  "Campionato Nazionale"),
        ("Valentina Romano",  "Trofeo Estivo"),
        ("Sofia Rinaldi",     "Coppa Italia"),
        ("Sofia Rinaldi",     "Memorial Bianchi"),
        ("Luca Ferrara",      "Memorial Bianchi"),
        ("Luca Ferrara",      "Trofeo Estivo"),
        ("Camilla Gallo",     "Torneo Citta"),
        ("Giorgia Martini",   "Memorial Bianchi"),
        ("Laura Bianchi",     "Memorial Bianchi"),
        ("Laura Bianchi",     "Challenge City"),
        ("Laura Bianchi",     "Supercoppa"),
        ("Laura Moretti",     "Coppa Regionale"),
        ("Sofia Bianchi",     "Challenge City"),
        ("Sofia Bianchi",     "Supercoppa"),
        ("Sofia Bianchi",     "Memorial Bianchi"),
        ("Martina Lombardi",  "Supercoppa"),
        ("Beatrice Greco",    "Coppa Disciplina"),
        ("Beatrice Greco",    "Campionato Nazionale"),
        ("Edoardo Ferrara",   "Challenge City"),
        ("Gabriele Rossi",    "Coppa Regionale"),
        ("Silvia Longo",      "Supercoppa"),
        ("Silvia Longo",      "Coppa Disciplina"),
        ("Silvia Longo",      "Campionato Nazionale"),
        ("Simone Galli",      "Coppa Disciplina"),
        ("Simone Galli",      "Memorial Bianchi"),
        ("Elena Esposito",    "Torneo Primavera"),
        ("Marco Caruso",      "Torneo Citta"),
        ("Marco Caruso",      "Memorial Bianchi"),
        ("Luca Greco",        "Campionato Nazionale"),
        ("Luca Greco",        "Torneo Primavera"),
        ("Silvia Costa",      "Coppa Italia"),
        ("Nicola Conti",      "Memorial Bianchi"),
        ("Nicola Conti",      "Torneo Citta"),
        ("Nicola Conti",      "Coppa Regionale"),
        ("Sara Costa",        "Torneo Primavera"),
        ("Sara Costa",        "Coppa Italia"),
        ("Chiara Colombo",    "Campionato Nazionale"),
        ("Matteo Santoro",    "Coppa Regionale"),
        ("Matteo Santoro",    "Torneo Primavera"),
        ("Riccardo Lombardi", "Coppa Regionale"),
        ("Riccardo Lombardi", "Memorial Bianchi"),
        ("Riccardo Lombardi", "Torneo Citta"),
        ("Aurora Lombardi",   "Coppa Italia"),
        ("Aurora Lombardi",   "Memorial Bianchi"),
        ("Anna Lombardi",     "Trofeo Estivo"),
        ("Anna Lombardi",     "Coppa Disciplina"),
        ("Anna Lombardi",     "Torneo Citta"),
        ("Riccardo Galli",    "Torneo Primavera"),
        ("Riccardo Galli",    "Memorial Bianchi"),
        ("Riccardo Galli",    "Coppa Italia"),
        ("Elisa Romano",      "Torneo Citta"),
        ("Andrea Mancini",    "Coppa Italia"),
        ("Andrea Mancini",    "Coppa Regionale"),
        ("Laura Longo",       "Supercoppa"),
        ("Giorgia Leone",     "Coppa Disciplina"),
        ("Gabriele Longo",    "Campionato Nazionale"),
        ("Davide Ferrara",    "Trofeo Estivo"),
        ("Simone Ricci",      "Torneo Citta"),
        ("Simone Ricci",      "Memorial Bianchi"),
        ("Francesco Gallo",   "Memorial Bianchi"),
        ("Francesco Gallo",   "Coppa Disciplina"),
        ("Francesco Gallo",   "Torneo Citta"),
        ("Federica Santoro",  "Coppa Disciplina"),
        ("Edoardo Esposito",  "Supercoppa"),
        ("Edoardo Esposito",  "Memorial Bianchi"),
        ("Edoardo Galli",     "Torneo Primavera"),
        ("Edoardo Galli",     "Torneo Citta"),
        ("Edoardo Galli",     "Supercoppa"),
        ("Nicola Costa",      "Supercoppa"),
        ("Giorgia Galli",     "Supercoppa"),
        ("Giorgia Galli",     "Torneo Citta"),
        ("Martina Moretti",   "Coppa Italia"),
        ("Martina Moretti",   "Memorial Bianchi"),
        ("Martina Moretti",   "Campionato Nazionale"),
        ("Pietro Martini",    "Torneo Citta"),
        ("Gabriele Esposito", "Coppa Regionale"),
    ]

    allena = [
        # (allenatore, squadra, dal, al)
        # Giorgio Colombo ha allenato prima Foxes, poi Lions
        ("Giorgio Colombo",  "Foxes",    2018, 2020),
        ("Giorgio Colombo",  "Lions",    2020, 2026),
        # Roberto Romano ha allenato Tigers, poi Sharks
        ("Roberto Romano",   "Tigers",   2021, 2023),
        ("Roberto Romano",   "Sharks",   2023, 2026),
        ("Giuseppe Greco",   "Eagles",   2022, 2026),
        ("Stefano Ricci",    "Wolves",   2021, 2026),
        # Fabio Rossi ha allenato Panthers, poi Falcons
        ("Fabio Rossi",      "Panthers", 2019, 2024),
        ("Fabio Rossi",      "Falcons",  2024, 2026),
        ("Paolo Ferrari",    "Bears",    2022, 2026),
        ("Vittorio Marino",  "Hawks",    2020, 2026),
        # Massimo Bianchi allena Cobras e ha assunto anche Bulls di recente
        ("Massimo Bianchi",  "Cobras",   2021, 2026),
        ("Massimo Bianchi",  "Bulls",    2026, 2026),
    ]

    with driver.session(database=DATABASE) as session:
        for squadra_name, citta_name in ha_sede:
            session.run(
                """
                MATCH (s:Squadra {name: $squadra_name})
                MATCH (c:Citta {name: $citta_name})
                CREATE (s)-[:HA_SEDE]->(c)
                """,
                squadra_name=squadra_name, citta_name=citta_name
            )

        for comp_name, citta_name in si_svolge_a:
            session.run(
                """
                MATCH (comp:Competizione {name: $comp_name})
                MATCH (c:Citta {name: $citta_name})
                CREATE (comp)-[:SI_SVOLGE_A]->(c)
                """,
                comp_name=comp_name, citta_name=citta_name
            )

        for atleta_name, squadra_name, dal, al in appartiene_a:
            session.run(
                """
                MATCH (a:Atleta {name: $atleta_name})
                MATCH (s:Squadra {name: $squadra_name})
                CREATE (a)-[:APPARTIENE_A {dal: $dal, al: $al}]->(s)
                """,
                atleta_name=atleta_name, squadra_name=squadra_name, dal=dal, al=al
            )

        for atleta_name, comp_name in partecipa:
            session.run(
                """
                MATCH (a:Atleta {name: $atleta_name})
                MATCH (c:Competizione {name: $comp_name})
                CREATE (a)-[:PARTECIPA]->(c)
                """,
                atleta_name=atleta_name, comp_name=comp_name
            )

        for allenatore_name, squadra_name, dal, al in allena:
            session.run(
                """
                MATCH (al:Allenatore {name: $allenatore_name})
                MATCH (s:Squadra {name: $squadra_name})
                CREATE (al)-[:ALLENA {dal: $dal, al: $al}]->(s)
                """,
                allenatore_name=allenatore_name, squadra_name=squadra_name, dal=dal, al=al
            )

    print(f"Create: {len(ha_sede)} HA_SEDE, {len(si_svolge_a)} SI_SVOLGE_A, "
          f"{len(appartiene_a)} APPARTIENE_A, {len(partecipa)} PARTECIPA, "
          f"{len(allena)} ALLENA")


# ---------------------------------------------------------------------------
# QUERY 1: atleti collegati tra loro per partecipazione alle stesse competizioni
# ---------------------------------------------------------------------------
def query_atleti_stesse_competizioni(driver):
    """
    Trova tutti gli atleti collegati tra loro per partecipazione
    alle stesse competizioni.
    WHERE a1.name < a2.name evita duplicati invertiti e auto-coppie.
    """
    with driver.session(database=DATABASE) as session:
        result = session.run(
            """
            MATCH (a1:Atleta)-[:PARTECIPA]->(c:Competizione)<-[:PARTECIPA]-(a2:Atleta)
            WHERE a1.name < a2.name
            RETURN a1.name AS atleta_1, a2.name AS atleta_2, c.name AS competizione
            ORDER BY competizione, atleta_1, atleta_2
            """
        )
        righe = [dict(record) for record in result]

    print("\n--- Query 1: Atleti collegati per partecipazione alle stesse competizioni ---")
    if not righe:
        print("Nessun risultato.")
    for r in righe:
        print(f"{r['atleta_1']:<22} - {r['atleta_2']:<22} -> {r['competizione']}")

    return righe


# ---------------------------------------------------------------------------
# QUERY 2: citta' piu' centrali nel grafo delle competizioni sportive
# ---------------------------------------------------------------------------
def query_citta_piu_centrali(driver):
    """
    Individua quali citta' risultano piu' centrali nel grafo delle
    competizioni sportive, calcolando il grado come numero di relazioni
    entranti di tipo SI_SVOLGE_A.
    """
    with driver.session(database=DATABASE) as session:
        result = session.run(
            """
            MATCH (c:Citta)<-[:SI_SVOLGE_A]-(comp:Competizione)
            RETURN c.name AS citta, count(comp) AS grado
            ORDER BY grado DESC
            """
        )
        righe = [dict(record) for record in result]

    print("\n--- Query 2: Citta' piu' centrali (grado nel grafo delle competizioni) ---")
    if not righe:
        print("Nessun risultato.")
    for r in righe:
        print(f"{r['citta']:<15} grado = {r['grado']}")

    return righe


# ---------------------------------------------------------------------------
# QUERY 3: allenatori connessi indirettamente tramite atleti/competizioni
# ---------------------------------------------------------------------------
def query_allenatori_connessi_indirettamente(driver):
    """
    Individua gli allenatori che hanno seguito atleti partecipanti
    alle stesse competizioni, evidenziando le connessioni indirette
    tra squadre diverse.
    - s1 <> s2: filtra solo connessioni tra squadre diverse
    - DISTINCT: deduplicato per (allenatore_1, squadra_1, allenatore_2,
      squadra_2, competizione), indipendentemente da quante coppie di
      atleti generano la stessa connessione
    """
    with driver.session(database=DATABASE) as session:
        result = session.run(
            """
            MATCH (a1:Allenatore)-[:ALLENA]->(s1:Squadra)<-[:APPARTIENE_A]-(at1:Atleta)
            MATCH (at1)-[:PARTECIPA]->(c:Competizione)<-[:PARTECIPA]-(at2:Atleta)
            MATCH (at2)-[:APPARTIENE_A]->(s2:Squadra)<-[:ALLENA]-(a2:Allenatore)
            WHERE elementId(a1) < elementId(a2) AND s1 <> s2
            RETURN DISTINCT
                a1.name AS allenatore_1,
                s1.name AS squadra_1,
                a2.name AS allenatore_2,
                s2.name AS squadra_2,
                c.name  AS competizione
            ORDER BY allenatore_1, allenatore_2, competizione
            """
        )
        righe = [dict(record) for record in result]

    print("\n--- Query 3: Allenatori connessi indirettamente tramite atleti/competizioni ---")
    if not righe:
        print("Nessun risultato.")
    for r in righe:
        print(f"{r['allenatore_1']:<18} ({r['squadra_1']:<8}) - "
              f"{r['allenatore_2']:<18} ({r['squadra_2']:<8}) -> {r['competizione']}")

    return righe


# ---------------------------------------------------------------------------
# QUERY 4: relazioni indirette tra allenatori e citta' sportive
# ---------------------------------------------------------------------------
def query_allenatori_citta_sportive(driver):
    """
    Individua le relazioni indirette tra allenatori e citta' sportive,
    seguendo il percorso:
        Allenatore -[:ALLENA]-> Squadra <-[:APPARTIENE_A]- Atleta
                  -[:PARTECIPA]-> Competizione -[:SI_SVOLGE_A]-> Citta

    Nota: questo percorso e' diverso da Allenatore->Squadra->HA_SEDE->Citta
    (sede della squadra). I due percorsi rispondono a domande diverse:
    la sede e' fissa, mentre le citta' sportive dipendono dalle
    competizioni a cui gli atleti dell'allenatore hanno partecipato.

    DISTINCT deduplicato per (allenatore, squadra, competizione, citta).
    """
    with driver.session(database=DATABASE) as session:
        result = session.run(
            """
            MATCH (al:Allenatore)-[:ALLENA]->(s:Squadra)<-[:APPARTIENE_A]-(at:Atleta)
            MATCH (at)-[:PARTECIPA]->(c:Competizione)-[:SI_SVOLGE_A]->(ci:Citta)
            RETURN DISTINCT
                al.name AS allenatore,
                s.name  AS squadra,
                c.name  AS competizione,
                ci.name AS citta
            ORDER BY allenatore, citta, competizione
            """
        )
        righe = [dict(record) for record in result]

    print("\n--- Query 4: Relazioni indirette tra allenatori e citta' sportive ---")
    if not righe:
        print("Nessun risultato.")
    for r in righe:
        print(f"{r['allenatore']:<18} ({r['squadra']:<8}) -> "
              f"{r['citta']:<10} [{r['competizione']}]")

    return righe


# ---------------------------------------------------------------------------
# QUERY 5: percorsi tra squadre e competizioni (derivati dagli atleti)
# ---------------------------------------------------------------------------
def query_squadre_competizioni(driver):
    """
    Individua a quali competizioni ha partecipato ciascuna squadra,
    seguendo il percorso:
        Squadra <-[:APPARTIENE_A]- Atleta -[:PARTECIPA]-> Competizione

    La partecipazione e' attribuita all'Atleta (come da traccia), non alla
    Squadra: una squadra "partecipa" se almeno uno dei suoi atleti vi
    partecipa. Questa query rende esplicito quel percorso derivato.
    Riporta anche il conteggio degli atleti coinvolti per ogni coppia.
    """
    with driver.session(database=DATABASE) as session:
        result = session.run(
            """
            MATCH (s:Squadra)<-[:APPARTIENE_A]-(at:Atleta)-[:PARTECIPA]->(c:Competizione)
            RETURN DISTINCT
                s.name AS squadra,
                c.name AS competizione,
                count(DISTINCT at) AS atleti_coinvolti
            ORDER BY squadra, competizione
            """
        )
        righe = [dict(record) for record in result]

    print("\n--- Query 5: Percorsi tra squadre e competizioni (derivati dagli atleti) ---")
    if not righe:
        print("Nessun risultato.")
    for r in righe:
        print(f"{r['squadra']:<10} -> {r['competizione']:<25} "
              f"({r['atleti_coinvolti']} atleti)")

    return righe


# ---------------------------------------------------------------------------
# UTILITY: pulizia completa del database
# ---------------------------------------------------------------------------
def pulisci_database(driver):
    """Elimina tutti i nodi e le relazioni presenti nel database."""
    with driver.session(database=DATABASE) as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("Database svuotato.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    driver = GraphDatabase.driver(URI, auth=AUTH)

    try:
        driver.verify_connectivity()

        # Pulisce il database prima di ripopolarlo, per evitare nodi/relazioni
        # duplicate se lo script viene eseguito piu' volte. Commentare questa
        # riga solo se si vuole aggiungere dati a un database gia' popolato.
        pulisci_database(driver)

        crea_nodi(driver)
        crea_relazioni(driver)

        query_atleti_stesse_competizioni(driver)
        query_citta_piu_centrali(driver)
        query_allenatori_connessi_indirettamente(driver)
        query_allenatori_citta_sportive(driver)
        query_squadre_competizioni(driver)

    finally:
        driver.close()


if __name__ == "__main__":
    main()
