from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# Elimina l'indice se esiste già, per poter rilanciare lo script senza errori
es.indices.delete(index="valutazioni_ds", ignore_unavailable=True)

# Lista dei 100 documenti (20 studenti, 10 esami, 10 schede per esame)
documenti = [
    {"Id_scheda_valutazione": "DS001_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS001", "Nome": "Marco", "Cognome": "Rossi", "Eta": 24, "Data_Esame": "2026-02-10", "Interesse_per_insegnamento": 9, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso molto interessante sui Big Data e Python per l'analisi dei dati."},
    {"Id_scheda_valutazione": "DS002_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS002", "Nome": "Anna", "Cognome": "Verdi", "Eta": 26, "Data_Esame": "2026-02-12", "Interesse_per_insegnamento": 8, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Docente preparato su database NoSQL e sistemi distribuiti."},
    {"Id_scheda_valutazione": "DS003_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS003", "Nome": "Luca", "Cognome": "Bianchi", "Eta": 23, "Data_Esame": "2026-02-15", "Interesse_per_insegnamento": 10, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Ottimo corso sui database distribuiti e NoSQL."},
    {"Id_scheda_valutazione": "DS006_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS006", "Nome": "Giulia", "Cognome": "Conti", "Eta": 24, "Data_Esame": "2026-02-16", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso interessante su Big Data e architetture distribuite."},
    {"Id_scheda_valutazione": "DS007_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS007", "Nome": "Davide", "Cognome": "Ferrari", "Eta": 26, "Data_Esame": "2026-02-17", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Big Data spiegato bene ma servono più esempi pratici."},
    {"Id_scheda_valutazione": "DS008_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS008", "Nome": "Elena", "Cognome": "Ricci", "Eta": 23, "Data_Esame": "2026-02-18", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Argomento molto utile per il lavoro con grandi moli di dati."},
    {"Id_scheda_valutazione": "DS009_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS009", "Nome": "Simone", "Cognome": "Marino", "Eta": 28, "Data_Esame": "2026-02-19", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Corso complesso ma interessante sui sistemi NoSQL."},
    {"Id_scheda_valutazione": "DS010_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS010", "Nome": "Chiara", "Cognome": "Greco", "Eta": 22, "Data_Esame": "2026-02-20", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima panoramica su Hadoop e Spark."},
    {"Id_scheda_valutazione": "DS011_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS011", "Nome": "Matteo", "Cognome": "Bruno", "Eta": 25, "Data_Esame": "2026-02-22", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante l'uso di Python per l'analisi Big Data."},
    {"Id_scheda_valutazione": "DS012_1", "Id_Esame": 1, "Insegnamento": "Big Data", "Id_studente": "DS012", "Nome": "Francesca", "Cognome": "Galli", "Eta": 24, "Data_Esame": "2026-02-25", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile ma richiede basi più solide di programmazione."},
    {"Id_scheda_valutazione": "DS001_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS001", "Nome": "Marco", "Cognome": "Rossi", "Eta": 24, "Data_Esame": "2026-03-01", "Interesse_per_insegnamento": 10, "Valutazione_docente": 10, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante il clustering e Python per l'analisi dei dati."},
    {"Id_scheda_valutazione": "DS004_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS004", "Nome": "Sara", "Cognome": "Esposito", "Eta": 25, "Data_Esame": "2026-03-02", "Interesse_per_insegnamento": 9, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima spiegazione degli algoritmi di clustering."},
    {"Id_scheda_valutazione": "DS005_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS005", "Nome": "Paolo", "Cognome": "Romano", "Eta": 27, "Data_Esame": "2026-03-05", "Interesse_per_insegnamento": 8, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Clustering interessante ma servono più esercitazioni."},
    {"Id_scheda_valutazione": "DS013_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS013", "Nome": "Alessandro", "Cognome": "Costa", "Eta": 27, "Data_Esame": "2026-03-06", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Data Mining interessante, in particolare il clustering."},
    {"Id_scheda_valutazione": "DS014_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS014", "Nome": "Valentina", "Cognome": "Fontana", "Eta": 23, "Data_Esame": "2026-03-08", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottimo approfondimento sugli algoritmi di classificazione."},
    {"Id_scheda_valutazione": "DS015_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS015", "Nome": "Riccardo", "Cognome": "Serra", "Eta": 26, "Data_Esame": "2026-03-10", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile ma un po' teorico, servirebbero più esercitazioni pratiche."},
    {"Id_scheda_valutazione": "DS016_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS016", "Nome": "Martina", "Cognome": "Pellegrini", "Eta": 25, "Data_Esame": "2026-03-12", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante il collegamento tra clustering e machine learning."},
    {"Id_scheda_valutazione": "DS017_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS017", "Nome": "Andrea", "Cognome": "Longo", "Eta": 24, "Data_Esame": "2026-03-15", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Corso utile ma impegnativo."},
    {"Id_scheda_valutazione": "DS018_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS018", "Nome": "Federica", "Cognome": "Gatti", "Eta": 22, "Data_Esame": "2026-03-17", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante l'applicazione del data mining al settore sanitario."},
    {"Id_scheda_valutazione": "DS019_2", "Id_Esame": 2, "Insegnamento": "Data Mining", "Id_studente": "DS019", "Nome": "Nicola", "Cognome": "Villa", "Eta": 28, "Data_Esame": "2026-03-20", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Buona spiegazione degli algoritmi di clustering gerarchico."},
    {"Id_scheda_valutazione": "DS002_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS002", "Nome": "Anna", "Cognome": "Verdi", "Eta": 26, "Data_Esame": "2026-04-10", "Interesse_per_insegnamento": 10, "Valutazione_docente": 10, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Reti neurali e machine learning spiegati con Python."},
    {"Id_scheda_valutazione": "DS003_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS003", "Nome": "Luca", "Cognome": "Bianchi", "Eta": 23, "Data_Esame": "2026-04-12", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottimo approccio alle reti neurali e machine learning."},
    {"Id_scheda_valutazione": "DS005_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS005", "Nome": "Paolo", "Cognome": "Romano", "Eta": 27, "Data_Esame": "2026-04-15", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Machine learning complesso ma utile per l'analisi dati."},
    {"Id_scheda_valutazione": "DS006_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS006", "Nome": "Giulia", "Cognome": "Conti", "Eta": 24, "Data_Esame": "2026-04-16", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante l'introduzione alle reti neurali."},
    {"Id_scheda_valutazione": "DS009_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS009", "Nome": "Simone", "Cognome": "Marino", "Eta": 28, "Data_Esame": "2026-04-18", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Machine learning utile ma richiede più matematica di base."},
    {"Id_scheda_valutazione": "DS012_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS012", "Nome": "Francesca", "Cognome": "Galli", "Eta": 24, "Data_Esame": "2026-04-20", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima spiegazione degli algoritmi supervisionati."},
    {"Id_scheda_valutazione": "DS015_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS015", "Nome": "Riccardo", "Cognome": "Serra", "Eta": 26, "Data_Esame": "2026-04-22", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Corso interessante su reti neurali e deep learning."},
    {"Id_scheda_valutazione": "DS018_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS018", "Nome": "Federica", "Cognome": "Gatti", "Eta": 22, "Data_Esame": "2026-04-24", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile per capire le applicazioni pratiche del machine learning."},
    {"Id_scheda_valutazione": "DS020_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS020", "Nome": "Ilaria", "Cognome": "Leone", "Eta": 23, "Data_Esame": "2026-04-27", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante ma servono più esempi di codice Python."},
    {"Id_scheda_valutazione": "DS013_3", "Id_Esame": 3, "Insegnamento": "Machine Learning", "Id_studente": "DS013", "Nome": "Alessandro", "Cognome": "Costa", "Eta": 27, "Data_Esame": "2026-04-29", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottimo corso, molto utile per l'analisi predittiva."},
    {"Id_scheda_valutazione": "DS001_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS001", "Nome": "Marco", "Cognome": "Rossi", "Eta": 24, "Data_Esame": "2026-05-10", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Statistica utile per l'analisi dei dati."},
    {"Id_scheda_valutazione": "DS004_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS004", "Nome": "Sara", "Cognome": "Esposito", "Eta": 25, "Data_Esame": "2026-05-12", "Interesse_per_insegnamento": 8, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Statistica spiegata bene con esempi pratici."},
    {"Id_scheda_valutazione": "DS003_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS003", "Nome": "Luca", "Cognome": "Bianchi", "Eta": 23, "Data_Esame": "2026-05-15", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso impegnativo ma utile per l'analisi dati."},
    {"Id_scheda_valutazione": "DS007_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS007", "Nome": "Davide", "Cognome": "Ferrari", "Eta": 26, "Data_Esame": "2026-05-16", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Statistica utile ma piuttosto impegnativa."},
    {"Id_scheda_valutazione": "DS010_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS010", "Nome": "Chiara", "Cognome": "Greco", "Eta": 22, "Data_Esame": "2026-05-18", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima base di matematica per la data science."},
    {"Id_scheda_valutazione": "DS014_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS014", "Nome": "Valentina", "Cognome": "Fontana", "Eta": 23, "Data_Esame": "2026-05-20", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante il collegamento tra statistica e probabilità."},
    {"Id_scheda_valutazione": "DS016_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS016", "Nome": "Martina", "Cognome": "Pellegrini", "Eta": 25, "Data_Esame": "2026-05-22", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Corso utile ma con troppa teoria."},
    {"Id_scheda_valutazione": "DS019_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS019", "Nome": "Nicola", "Cognome": "Villa", "Eta": 28, "Data_Esame": "2026-05-24", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante l'applicazione della statistica ai big data."},
    {"Id_scheda_valutazione": "DS002_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS002", "Nome": "Anna", "Cognome": "Verdi", "Eta": 26, "Data_Esame": "2026-05-26", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Ottimo corso, molto utile per l'analisi dei dati."},
    {"Id_scheda_valutazione": "DS017_4", "Id_Esame": 4, "Insegnamento": "Statistica e matematica per la data science", "Id_studente": "DS017", "Nome": "Andrea", "Cognome": "Longo", "Eta": 24, "Data_Esame": "2026-05-28", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Statistica interessante ma servono più esercitazioni."},
    {"Id_scheda_valutazione": "DS002_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS002", "Nome": "Anna", "Cognome": "Verdi", "Eta": 26, "Data_Esame": "2026-06-10", "Interesse_per_insegnamento": 8, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Data warehouse e modelli multidimensionali chiari."},
    {"Id_scheda_valutazione": "DS004_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS004", "Nome": "Sara", "Cognome": "Esposito", "Eta": 25, "Data_Esame": "2026-06-12", "Interesse_per_insegnamento": 9, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Ottimi esempi su data warehouse e schemi multidimensionali."},
    {"Id_scheda_valutazione": "DS005_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS005", "Nome": "Paolo", "Cognome": "Romano", "Eta": 27, "Data_Esame": "2026-06-15", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Approfondire schemi a stella e data warehouse."},
    {"Id_scheda_valutazione": "DS008_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS008", "Nome": "Elena", "Cognome": "Ricci", "Eta": 23, "Data_Esame": "2026-06-16", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante l'uso dei data warehouse nelle aziende."},
    {"Id_scheda_valutazione": "DS011_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS011", "Nome": "Matteo", "Cognome": "Bruno", "Eta": 25, "Data_Esame": "2026-06-18", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Ottima spiegazione degli schemi a stella e snowflake."},
    {"Id_scheda_valutazione": "DS013_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS013", "Nome": "Alessandro", "Cognome": "Costa", "Eta": 27, "Data_Esame": "2026-06-20", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso utile ma un po' ripetitivo."},
    {"Id_scheda_valutazione": "DS017_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS017", "Nome": "Andrea", "Cognome": "Longo", "Eta": 24, "Data_Esame": "2026-06-22", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante il processo di ETL."},
    {"Id_scheda_valutazione": "DS020_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS020", "Nome": "Ilaria", "Cognome": "Leone", "Eta": 23, "Data_Esame": "2026-06-24", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottimo corso sui modelli multidimensionali."},
    {"Id_scheda_valutazione": "DS006_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS006", "Nome": "Giulia", "Cognome": "Conti", "Eta": 24, "Data_Esame": "2026-06-26", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile per capire l'architettura dei data warehouse."},
    {"Id_scheda_valutazione": "DS009_5", "Id_Esame": 5, "Insegnamento": "Modelli multidimensionali per l'analisi dei dati", "Id_studente": "DS009", "Nome": "Simone", "Cognome": "Marino", "Eta": 28, "Data_Esame": "2026-06-28", "Interesse_per_insegnamento": 8, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante ma servono più casi di studio."},
    {"Id_scheda_valutazione": "DS001_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS001", "Nome": "Marco", "Cognome": "Rossi", "Eta": 24, "Data_Esame": "2026-07-06", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante l'introduzione al GDPR e alla privacy digitale."},
    {"Id_scheda_valutazione": "DS003_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS003", "Nome": "Luca", "Cognome": "Bianchi", "Eta": 23, "Data_Esame": "2026-07-07", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto utile per capire gli aspetti legali dell'informatica."},
    {"Id_scheda_valutazione": "DS005_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS005", "Nome": "Paolo", "Cognome": "Romano", "Eta": 27, "Data_Esame": "2026-07-08", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Corso interessante ma piuttosto teorico."},
    {"Id_scheda_valutazione": "DS007_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS007", "Nome": "Davide", "Cognome": "Ferrari", "Eta": 26, "Data_Esame": "2026-07-09", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima panoramica sul diritto d'autore nel software."},
    {"Id_scheda_valutazione": "DS009_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS009", "Nome": "Simone", "Cognome": "Marino", "Eta": 28, "Data_Esame": "2026-07-10", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile per comprendere le normative sulla protezione dei dati."},
    {"Id_scheda_valutazione": "DS011_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS011", "Nome": "Matteo", "Cognome": "Bruno", "Eta": 25, "Data_Esame": "2026-07-11", "Interesse_per_insegnamento": 8, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante il tema della responsabilità digitale."},
    {"Id_scheda_valutazione": "DS013_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS013", "Nome": "Alessandro", "Cognome": "Costa", "Eta": 27, "Data_Esame": "2026-07-13", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante l'analisi dei contratti informatici."},
    {"Id_scheda_valutazione": "DS015_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS015", "Nome": "Riccardo", "Cognome": "Serra", "Eta": 26, "Data_Esame": "2026-07-14", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso utile ma con troppi riferimenti normativi."},
    {"Id_scheda_valutazione": "DS017_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS017", "Nome": "Andrea", "Cognome": "Longo", "Eta": 24, "Data_Esame": "2026-07-15", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante il collegamento tra cybersicurezza e diritto."},
    {"Id_scheda_valutazione": "DS019_6", "Id_Esame": 6, "Insegnamento": "Informatica giuridica", "Id_studente": "DS019", "Nome": "Nicola", "Cognome": "Villa", "Eta": 28, "Data_Esame": "2026-07-16", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Utile ma richiede più esempi pratici."},
    {"Id_scheda_valutazione": "DS002_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS002", "Nome": "Anna", "Cognome": "Verdi", "Eta": 26, "Data_Esame": "2026-07-17", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante l'approfondimento sui modelli di regressione."},
    {"Id_scheda_valutazione": "DS004_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS004", "Nome": "Sara", "Cognome": "Esposito", "Eta": 25, "Data_Esame": "2026-07-18", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima spiegazione dei modelli statistici applicati ai dati reali."},
    {"Id_scheda_valutazione": "DS006_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS006", "Nome": "Giulia", "Cognome": "Conti", "Eta": 24, "Data_Esame": "2026-07-19", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso utile ma un po' complesso da seguire."},
    {"Id_scheda_valutazione": "DS008_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS008", "Nome": "Elena", "Cognome": "Ricci", "Eta": 23, "Data_Esame": "2026-07-20", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante il confronto tra modelli lineari e non lineari."},
    {"Id_scheda_valutazione": "DS010_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS010", "Nome": "Chiara", "Cognome": "Greco", "Eta": 22, "Data_Esame": "2026-07-21", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Utile ma servirebbero più esercizi pratici."},
    {"Id_scheda_valutazione": "DS012_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS012", "Nome": "Francesca", "Cognome": "Galli", "Eta": 24, "Data_Esame": "2026-07-22", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante l'uso dei modelli statistici predittivi."},
    {"Id_scheda_valutazione": "DS014_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS014", "Nome": "Valentina", "Cognome": "Fontana", "Eta": 23, "Data_Esame": "2026-07-23", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Ottimo corso, molto utile per l'analisi dei dati."},
    {"Id_scheda_valutazione": "DS016_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS016", "Nome": "Martina", "Cognome": "Pellegrini", "Eta": 25, "Data_Esame": "2026-07-24", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante ma un po' teorico."},
    {"Id_scheda_valutazione": "DS018_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS018", "Nome": "Federica", "Cognome": "Gatti", "Eta": 22, "Data_Esame": "2026-07-25", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile per comprendere meglio la statistica inferenziale."},
    {"Id_scheda_valutazione": "DS020_7", "Id_Esame": 7, "Insegnamento": "Modelli statistici", "Id_studente": "DS020", "Nome": "Ilaria", "Cognome": "Leone", "Eta": 23, "Data_Esame": "2026-07-27", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante il tema della validazione dei modelli."},
    {"Id_scheda_valutazione": "DS001_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS001", "Nome": "Marco", "Cognome": "Rossi", "Eta": 24, "Data_Esame": "2026-08-03", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante l'approccio Agile alla gestione dei progetti."},
    {"Id_scheda_valutazione": "DS004_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS004", "Nome": "Sara", "Cognome": "Esposito", "Eta": 25, "Data_Esame": "2026-08-04", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto utile per organizzare il lavoro di gruppo."},
    {"Id_scheda_valutazione": "DS007_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS007", "Nome": "Davide", "Cognome": "Ferrari", "Eta": 26, "Data_Esame": "2026-08-05", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso interessante ma servono più casi pratici."},
    {"Id_scheda_valutazione": "DS010_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS010", "Nome": "Chiara", "Cognome": "Greco", "Eta": 22, "Data_Esame": "2026-08-06", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima spiegazione delle metodologie Scrum e Kanban."},
    {"Id_scheda_valutazione": "DS013_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS013", "Nome": "Alessandro", "Cognome": "Costa", "Eta": 27, "Data_Esame": "2026-08-07", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Utile ma un po' ripetitivo nella seconda parte."},
    {"Id_scheda_valutazione": "DS016_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS016", "Nome": "Martina", "Cognome": "Pellegrini", "Eta": 25, "Data_Esame": "2026-08-08", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante la gestione dei rischi di progetto."},
    {"Id_scheda_valutazione": "DS019_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS019", "Nome": "Nicola", "Cognome": "Villa", "Eta": 28, "Data_Esame": "2026-08-10", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso utile per il lavoro in team."},
    {"Id_scheda_valutazione": "DS002_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS002", "Nome": "Anna", "Cognome": "Verdi", "Eta": 26, "Data_Esame": "2026-08-11", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante il collegamento tra project management e data science."},
    {"Id_scheda_valutazione": "DS005_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS005", "Nome": "Paolo", "Cognome": "Romano", "Eta": 27, "Data_Esame": "2026-08-12", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottimo corso, molto utile per la pianificazione dei progetti."},
    {"Id_scheda_valutazione": "DS008_8", "Id_Esame": 8, "Insegnamento": "Project Management", "Id_studente": "DS008", "Nome": "Elena", "Cognome": "Ricci", "Eta": 23, "Data_Esame": "2026-08-13", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile ma richiede più tempo per essere assimilato."},
    {"Id_scheda_valutazione": "DS011_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS011", "Nome": "Matteo", "Cognome": "Bruno", "Eta": 25, "Data_Esame": "2026-08-14", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante lo studio dei bias cognitivi nelle decisioni economiche."},
    {"Id_scheda_valutazione": "DS014_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS014", "Nome": "Valentina", "Cognome": "Fontana", "Eta": 23, "Data_Esame": "2026-08-15", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto utile per comprendere il comportamento dei consumatori."},
    {"Id_scheda_valutazione": "DS017_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS017", "Nome": "Andrea", "Cognome": "Longo", "Eta": 24, "Data_Esame": "2026-08-17", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso interessante ma piuttosto teorico."},
    {"Id_scheda_valutazione": "DS020_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS020", "Nome": "Ilaria", "Cognome": "Leone", "Eta": 23, "Data_Esame": "2026-08-18", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima spiegazione della teoria del prospetto."},
    {"Id_scheda_valutazione": "DS003_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS003", "Nome": "Luca", "Cognome": "Bianchi", "Eta": 23, "Data_Esame": "2026-08-19", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Utile ma richiede basi di psicologia."},
    {"Id_scheda_valutazione": "DS006_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS006", "Nome": "Giulia", "Cognome": "Conti", "Eta": 24, "Data_Esame": "2026-08-20", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante il tema delle euristiche decisionali."},
    {"Id_scheda_valutazione": "DS009_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS009", "Nome": "Simone", "Cognome": "Marino", "Eta": 28, "Data_Esame": "2026-08-21", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso utile per capire le decisioni economiche irrazionali."},
    {"Id_scheda_valutazione": "DS012_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS012", "Nome": "Francesca", "Cognome": "Galli", "Eta": 24, "Data_Esame": "2026-08-22", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante il collegamento con l'economia comportamentale."},
    {"Id_scheda_valutazione": "DS015_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS015", "Nome": "Riccardo", "Cognome": "Serra", "Eta": 26, "Data_Esame": "2026-08-24", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante e ben strutturato."},
    {"Id_scheda_valutazione": "DS018_9", "Id_Esame": 9, "Insegnamento": "Economia cognitiva", "Id_studente": "DS018", "Nome": "Federica", "Cognome": "Gatti", "Eta": 22, "Data_Esame": "2026-08-25", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Utile ma servono più esempi concreti."},
    {"Id_scheda_valutazione": "DS001_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS001", "Nome": "Marco", "Cognome": "Rossi", "Eta": 24, "Data_Esame": "2026-09-01", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante l'analisi del testo con Python e NLP."},
    {"Id_scheda_valutazione": "DS002_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS002", "Nome": "Anna", "Cognome": "Verdi", "Eta": 26, "Data_Esame": "2026-09-02", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Ottima spiegazione delle tecniche di text mining."},
    {"Id_scheda_valutazione": "DS003_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS003", "Nome": "Luca", "Cognome": "Bianchi", "Eta": 23, "Data_Esame": "2026-09-03", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso utile ma servono più esercitazioni pratiche."},
    {"Id_scheda_valutazione": "DS004_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS004", "Nome": "Sara", "Cognome": "Esposito", "Eta": 25, "Data_Esame": "2026-09-04", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 9, "Commenti_suggerimenti": "Molto interessante l'uso del sentiment analysis."},
    {"Id_scheda_valutazione": "DS005_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS005", "Nome": "Paolo", "Cognome": "Romano", "Eta": 27, "Data_Esame": "2026-09-05", "Interesse_per_insegnamento": 6, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 6, "Commenti_suggerimenti": "Utile ma un po' complesso senza basi di NLP."},
    {"Id_scheda_valutazione": "DS006_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS006", "Nome": "Giulia", "Cognome": "Conti", "Eta": 24, "Data_Esame": "2026-09-06", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Interessante il collegamento tra text mining e machine learning."},
    {"Id_scheda_valutazione": "DS007_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS007", "Nome": "Davide", "Cognome": "Ferrari", "Eta": 26, "Data_Esame": "2026-09-07", "Interesse_per_insegnamento": 7, "Valutazione_docente": 7, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Corso utile per l'analisi di grandi quantità di testo."},
    {"Id_scheda_valutazione": "DS008_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS008", "Nome": "Elena", "Cognome": "Ricci", "Eta": 23, "Data_Esame": "2026-09-08", "Interesse_per_insegnamento": 9, "Valutazione_docente": 9, "Valutazione_materiale_didattico": 8, "Commenti_suggerimenti": "Molto interessante l'applicazione del text mining ai social media."},
    {"Id_scheda_valutazione": "DS009_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS009", "Nome": "Simone", "Cognome": "Marino", "Eta": 28, "Data_Esame": "2026-09-09", "Interesse_per_insegnamento": 8, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Ottimo corso, utile per l'estrazione di informazioni dai testi."},
    {"Id_scheda_valutazione": "DS010_10", "Id_Esame": 10, "Insegnamento": "Text Mining", "Id_studente": "DS010", "Nome": "Chiara", "Cognome": "Greco", "Eta": 22, "Data_Esame": "2026-09-10", "Interesse_per_insegnamento": 7, "Valutazione_docente": 8, "Valutazione_materiale_didattico": 7, "Commenti_suggerimenti": "Interessante ma richiede più pratica con le librerie NLP."},
]

# Inserisce tutti i documenti nell'indice, uno alla volta
for doc in documenti:
    es.index(index="valutazioni_ds", document=doc)

# Forza il refresh dell'indice, altrimenti i documenti appena inseriti
# potrebbero non essere visibili subito nelle ricerche
es.indices.refresh(index="valutazioni_ds")

conteggio = es.count(index="valutazioni_ds")
print("Documenti totali nell'indice:", conteggio["count"])


# 1. RELEVANCE SCORING (BM25)
# Ogni risultato ha un punteggio di pertinenza (_score), non solo un match booleano.
print("\n--- 1. Relevance scoring ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "match": {
            "Commenti_suggerimenti": "corso interessante big data"
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_score"], hit["_id"], hit["_source"])


# 2. FUZZY MATCHING
# Tollera errori di battitura (distanza di Levenshtein): trova "ottimo"
# anche se scritto in modo leggermente diverso (ad esempio "ottima").
# In SQL servirebbe un motore esterno.
print("\n--- 2. Fuzzy matching ---")
result = es.search(
    index="valutazioni_ds",
    size=20,
    query={
        "match": {
            "Commenti_suggerimenti": {
                "query": "ottimo",
                "fuzziness": "AUTO"
            }
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_id"], hit["_source"])


# 3a. RICERCA CON DUE PAROLE CHIAVE (AND)
# Utile per cercare co-occorrenze significative.
print("\n--- 3a. Ricerca con due parole chiave (AND) ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "match": {
            "Commenti_suggerimenti": {
                "query": "utile statistica",
                "operator": "and"
            }
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_id"], hit["_source"])


# 3b. RICERCA CON DUE PAROLE CHIAVE (OR)
# Utile per la ricerca di sinonimi.
print("\n--- 3b. Ricerca con due parole chiave (OR) ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "match": {
            "Commenti_suggerimenti": {
                "query": "capire comprendere",
                "operator": "or",
                "fuzziness": "AUTO"
            }
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_id"], hit["_source"])


# 4. HIGHLIGHTING
# Restituisce i frammenti di testo con i termini di ricerca evidenziati.
print("\n--- 4. Highlighting ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "match": {
            "Commenti_suggerimenti": "python"
        }
    },
    highlight={
        "fields": {
            "Commenti_suggerimenti": {}
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_id"], hit["_source"])
    print("   highlight:", hit["highlight"]["Commenti_suggerimenti"])


# 5. SIGNIFICANT TEXT
# Trova le parole più caratteristiche di un sottoinsieme di documenti
# (qui: valutazioni con voto docente basso) rispetto al resto del corpus.
print("\n--- 5. Significant text ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "range": {
            "Valutazione_docente": {"lte": 7}
        }
    },
    aggs={
        "parole_caratteristiche": {
            "significant_text": {
                "field": "Commenti_suggerimenti"
            }
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for bucket in result["aggregations"]["parole_caratteristiche"]["buckets"]:
    print(bucket["key"], "- occorrenze:", bucket["doc_count"])


# 6. MATCH PHRASE
# Le parole devono comparire esattamente in quell'ordine e vicinanza.
print("\n--- 6. Match phrase ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "match_phrase": {
            "Commenti_suggerimenti": "l'analisi dei dati"
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_id"], hit["_source"])


# 7. FILTRO STRUTTURATO SU DATA (range query)
print("\n--- 7. Range su data esame ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "range": {
            "Data_Esame": {
                "gte": "2026-03-01",
                "lte": "2026-05-31"
            }
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_id"], hit["_source"])


# 8. FILTRO STRUTTURATO SU VALUTAZIONE DOCENTE (range query)
print("\n--- 8. Range su valutazione docente ---")
result = es.search(
    index="valutazioni_ds",
    query={
        "range": {
            "Valutazione_docente": {
                "gt": 9
            }
        }
    }
)
print("Risultati trovati:", result["hits"]["total"]["value"])
for hit in result["hits"]["hits"]:
    print(hit["_id"], hit["_source"])


# 9. AGGREGAZIONE NUMERICA: media interesse per insegnamento
print("\n--- 9. Media interesse per insegnamento ---")
result = es.search(
    index="valutazioni_ds",
    size=0,
    aggs={
        "insegnamenti": {
            "terms": {
                "field": "Insegnamento.keyword",
                "size": 20
            },
            "aggs": {
                "media_interesse": {
                    "avg": {
                        "field": "Interesse_per_insegnamento"
                    }
                }
            }
        }
    }
)
for bucket in result["aggregations"]["insegnamenti"]["buckets"]:
    print(bucket["key"], "- media interesse:", round(bucket["media_interesse"]["value"], 2))
