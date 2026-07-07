import sqlite3

# ─────────────────────────────────────────
# CONNESSIONE
# ─────────────────────────────────────────

conn = sqlite3.connect("autoscuola.db")
conn.execute("PRAGMA foreign_keys = ON")   # abilita i vincoli FK in SQLite
cursor = conn.cursor()


# ─────────────────────────────────────────
# CREAZIONE TABELLE
# ─────────────────────────────────────────

cursor.executescript("""
CREATE TABLE IF NOT EXISTS Tipologia_Patente (
    Id_TP       INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome        TEXT    NOT NULL,
    Descrizione TEXT,
    Eta_min     INTEGER NOT NULL CHECK (Eta_min >= 14)
);

CREATE TABLE IF NOT EXISTS Candidato (
    Id_C    INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome    TEXT    NOT NULL,
    Cognome TEXT    NOT NULL,
    Data_N  TEXT    NOT NULL,
    Id_TP   INTEGER NOT NULL,
    FOREIGN KEY (Id_TP) REFERENCES Tipologia_Patente(Id_TP)
);

CREATE TABLE IF NOT EXISTS Istruttore (
    Id_I            INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome            TEXT NOT NULL,
    Cognome         TEXT NOT NULL,
    Nr_Abilitazione TEXT NOT NULL UNIQUE,
    Telefono        TEXT
);

CREATE TABLE IF NOT EXISTS Veicolo (
    Targa                   TEXT PRIMARY KEY,
    Modello                 TEXT    NOT NULL,
    Categoria               TEXT    NOT NULL,
    Anno_immatricolazione   INTEGER NOT NULL CHECK (Anno_immatricolazione < 2026)
);

CREATE TABLE IF NOT EXISTS Lezione (
    Id_Prenotazione INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_I            INTEGER NOT NULL,
    Id_C            INTEGER NOT NULL,
    Targa           TEXT    NOT NULL,
    Data            TEXT    NOT NULL,
    Ora             TEXT    NOT NULL CHECK (Ora >= '08:00' AND Ora <= '20:00'),
    Durata          INTEGER NOT NULL CHECK (Durata > 0 AND Durata <= 180),
    FOREIGN KEY (Id_I)  REFERENCES Istruttore(Id_I),
    FOREIGN KEY (Id_C)  REFERENCES Candidato(Id_C),
    FOREIGN KEY (Targa) REFERENCES Veicolo(Targa)
);

CREATE TABLE IF NOT EXISTS Tipologia_Esame (
    Id_TE       INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome        TEXT    NOT NULL,
    Max_posti   INTEGER NOT NULL CHECK (Max_posti > 0)
);

CREATE TABLE IF NOT EXISTS Esame (
    Id_E        INTEGER PRIMARY KEY AUTOINCREMENT,
    Id_C        INTEGER NOT NULL,
    Id_TE       INTEGER NOT NULL,
    Data        TEXT    NOT NULL,
    Esito       TEXT    NOT NULL CHECK (Esito IN ('Superato', 'Non Superato')),
    Punteggio   INTEGER          CHECK (Punteggio >= 0 AND Punteggio <= 30),
    FOREIGN KEY (Id_C)  REFERENCES Candidato(Id_C),
    FOREIGN KEY (Id_TE) REFERENCES Tipologia_Esame(Id_TE)
);
""")

conn.commit()
print("Tabelle create correttamente.\n")


# ─────────────────────────────────────────
# INSERIMENTO DATI
# ─────────────────────────────────────────

# Tipologia_Patente (10)
cursor.executemany(
    "INSERT OR IGNORE INTO Tipologia_Patente (Id_TP, Nome, Descrizione, Eta_min) VALUES (?, ?, ?, ?)",
    [
        (1,  'AM',  'Ciclomotori',                       14),
        (2,  'A1',  'Motocicli leggeri',                 16),
        (3,  'A2',  'Motocicli medi',                    18),
        (4,  'A',   'Motocicli senza limiti di potenza',  20),
        (5,  'B',   'Autoveicoli',                       18),
        (6,  'BE',  'Autoveicoli con rimorchio',         18),
        (7,  'C',   'Autocarri',                         21),
        (8,  'C+E', 'Autocarri con rimorchio',           21),
        (9,  'D',   'Autobus',                           24),
        (10, 'D+E', 'Autobus con rimorchio',             24),
    ]
)

# Candidato (30)
cursor.executemany(
    "INSERT OR IGNORE INTO Candidato (Id_C, Nome, Cognome, Data_N, Id_TP) VALUES (?, ?, ?, ?, ?)",
    [
        (1,  'Luca',      'Rossi',     '2005-03-12', 1),
        (2,  'Giulia',    'Bianchi',   '2006-07-21', 2),
        (3,  'Marco',     'Verdi',     '2007-11-02', 3),
        (4,  'Sara',      'Ferrari',   '2004-01-15', 4),
        (5,  'Alessio',   'Russo',     '2003-05-22', 5),
        (6,  'Martina',   'Romano',    '2002-09-10', 6),
        (7,  'Davide',    'Colombo',   '2001-12-30', 7),
        (8,  'Elisa',     'Ricci',     '2000-04-18', 8),
        (9,  'Simone',    'Marino',    '1999-08-07', 9),
        (10, 'Chiara',    'Greco',     '1998-02-25', 10),
        (11, 'Matteo',    'Bruno',     '2005-06-14', 1),
        (12, 'Francesca', 'Gallo',     '2006-10-03', 2),
        (13, 'Andrea',    'Conti',     '2007-01-29', 3),
        (14, 'Valentina', 'De Luca',   '2004-03-11', 4),
        (15, 'Riccardo',  'Mancini',   '2003-07-19', 5),
        (16, 'Laura',     'Costa',     '2002-11-05', 6),
        (17, 'Stefano',   'Giordano',  '2001-02-14', 7),
        (18, 'Giorgia',   'Rizzo',     '2000-06-23', 8),
        (19, 'Lorenzo',   'Lombardi',  '1999-09-30', 9),
        (20, 'Beatrice',  'Moretti',   '1998-12-08', 10),
        (21, 'Nicola',    'Barbieri',  '2005-04-17', 1),
        (22, 'Camilla',   'Fontana',   '2006-08-26', 2),
        (23, 'Filippo',   'Santoro',   '2007-12-04', 3),
        (24, 'Alice',     'Mariani',   '2004-02-12', 4),
        (25, 'Tommaso',   'Rinaldi',   '2003-05-21', 5),
        (26, 'Sofia',     'Caruso',    '2002-09-29', 6),
        (27, 'Gabriele',  'Ferrara',   '2001-01-07', 7),
        (28, 'Aurora',    'Galli',     '2000-04-16', 8),
        (29, 'Pietro',    'Martini',   '1999-08-24', 9),
        (30, 'Noemi',     'Leone',     '1998-11-02', 10),
    ]
)

# Istruttore (10)
cursor.executemany(
    "INSERT OR IGNORE INTO Istruttore (Id_I, Nome, Cognome, Nr_Abilitazione, Telefono) VALUES (?, ?, ?, ?, ?)",
    [
        (1,  'Paolo',     'Neri',     'AB12345', '3331112222'),
        (2,  'Andrea',    'Gallo',    'AB54321', '3333334444'),
        (3,  'Elena',     'Costa',    'AB67890', '3335556666'),
        (4,  'Francesco', 'Romano',   'AB11223', '3337778888'),
        (5,  'Chiara',    'Mancini',  'AB44556', '3339990000'),
        (6,  'Davide',    'Ricci',    'AB77889', '3332223333'),
        (7,  'Valentina', 'Esposito', 'AB99001', '3334445555'),
        (8,  'Simone',    'Conti',    'AB22334', '3336667777'),
        (9,  'Federica',  'Greco',    'AB55667', '3338889999'),
        (10, 'Matteo',    'Bruno',    'AB88990', '3331113333'),
    ]
)

# Veicolo (15)
cursor.executemany(
    "INSERT OR IGNORE INTO Veicolo (Targa, Modello, Categoria, Anno_immatricolazione) VALUES (?, ?, ?, ?)",
    [
        ('AB123CD', 'Fiat Panda',        'B',   2018),
        ('EF456GH', 'Volkswagen Golf',   'B',   2020),
        ('IJ789KL', 'Yamaha MT-07',      'A2',  2021),
        ('MN012OP', 'Piaggio Liberty',   'AM',  2019),
        ('QR345ST', 'Fiat 500',          'B',   2022),
        ('UV678WX', 'Opel Corsa',        'B',   2017),
        ('YZ901AB', 'Honda CB500F',      'A2',  2020),
        ('CD234EF', 'Kawasaki Z900',     'A',   2023),
        ('GH567IJ', 'Iveco Daily',       'C',   2019),
        ('KL890MN', 'Mercedes Sprinter', 'C',   2021),
        ('OP123QR', 'Scania R450',       'C+E', 2018),
        ('ST456UV', 'Mercedes Tourismo', 'D',   2020),
        ('WX789YZ', 'Piaggio Beverly',   'A1',  2022),
        ('AB987CD', 'Fiat Ducato',       'BE',  2019),
        ('EF654GH', 'MAN TGX',           'C+E', 2017),
    ]
)

# Lezione (100)
# Pattern: si ripete un blocco fisso di 30 lezioni (istruttori 1-10 ripetuti 3 volte,
# candidati 1-30, veicoli 1-15 ripetuti 2 volte, orari e durate a rotazione),
# cambiano solo numero prenotazione e data (che avanza di un giorno ogni riga).
cursor.executemany(
    "INSERT OR IGNORE INTO Lezione (Id_Prenotazione, Id_I, Id_C, Targa, Data, Ora, Durata) VALUES (?, ?, ?, ?, ?, ?, ?)",
    [
        (1,1,1,'AB123CD','2026-01-05','08:00',60),
        (2,2,2,'EF456GH','2026-01-06','09:00',90),
        (3,3,3,'IJ789KL','2026-01-07','10:00',45),
        (4,4,4,'MN012OP','2026-01-08','11:00',120),
        (5,5,5,'QR345ST','2026-01-09','13:00',60),
        (6,6,6,'UV678WX','2026-01-10','14:00',30),
        (7,7,7,'YZ901AB','2026-01-11','15:00',90),
        (8,8,8,'CD234EF','2026-01-12','16:00',60),
        (9,9,9,'GH567IJ','2026-01-13','17:00',150),
        (10,10,10,'KL890MN','2026-01-14','18:00',60),
        (11,1,11,'OP123QR','2026-01-15','08:00',60),
        (12,2,12,'ST456UV','2026-01-16','09:00',90),
        (13,3,13,'WX789YZ','2026-01-17','10:00',45),
        (14,4,14,'AB987CD','2026-01-18','11:00',120),
        (15,5,15,'EF654GH','2026-01-19','13:00',60),
        (16,6,16,'AB123CD','2026-01-20','14:00',30),
        (17,7,17,'EF456GH','2026-01-21','15:00',90),
        (18,8,18,'IJ789KL','2026-01-22','16:00',60),
        (19,9,19,'MN012OP','2026-01-23','17:00',150),
        (20,10,20,'QR345ST','2026-01-24','18:00',60),
        (21,1,21,'UV678WX','2026-01-25','08:00',60),
        (22,2,22,'YZ901AB','2026-01-26','09:00',90),
        (23,3,23,'CD234EF','2026-01-27','10:00',45),
        (24,4,24,'GH567IJ','2026-01-28','11:00',120),
        (25,5,25,'KL890MN','2026-01-29','13:00',60),
        (26,6,26,'OP123QR','2026-01-30','14:00',30),
        (27,7,27,'ST456UV','2026-01-31','15:00',90),
        (28,8,28,'WX789YZ','2026-02-01','16:00',60),
        (29,9,29,'AB987CD','2026-02-02','17:00',150),
        (30,10,30,'EF654GH','2026-02-03','18:00',60),
        (31,1,1,'AB123CD','2026-02-04','08:00',60),
        (32,2,2,'EF456GH','2026-02-05','09:00',90),
        (33,3,3,'IJ789KL','2026-02-06','10:00',45),
        (34,4,4,'MN012OP','2026-02-07','11:00',120),
        (35,5,5,'QR345ST','2026-02-08','13:00',60),
        (36,6,6,'UV678WX','2026-02-09','14:00',30),
        (37,7,7,'YZ901AB','2026-02-10','15:00',90),
        (38,8,8,'CD234EF','2026-02-11','16:00',60),
        (39,9,9,'GH567IJ','2026-02-12','17:00',150),
        (40,10,10,'KL890MN','2026-02-13','18:00',60),
        (41,1,11,'OP123QR','2026-02-14','08:00',60),
        (42,2,12,'ST456UV','2026-02-15','09:00',90),
        (43,3,13,'WX789YZ','2026-02-16','10:00',45),
        (44,4,14,'AB987CD','2026-02-17','11:00',120),
        (45,5,15,'EF654GH','2026-02-18','13:00',60),
        (46,6,16,'AB123CD','2026-02-19','14:00',30),
        (47,7,17,'EF456GH','2026-02-20','15:00',90),
        (48,8,18,'IJ789KL','2026-02-21','16:00',60),
        (49,9,19,'MN012OP','2026-02-22','17:00',150),
        (50,10,20,'QR345ST','2026-02-23','18:00',60),
        (51,1,21,'UV678WX','2026-02-24','08:00',60),
        (52,2,22,'YZ901AB','2026-02-25','09:00',90),
        (53,3,23,'CD234EF','2026-02-26','10:00',45),
        (54,4,24,'GH567IJ','2026-02-27','11:00',120),
        (55,5,25,'KL890MN','2026-02-28','13:00',60),
        (56,6,26,'OP123QR','2026-03-01','14:00',30),
        (57,7,27,'ST456UV','2026-03-02','15:00',90),
        (58,8,28,'WX789YZ','2026-03-03','16:00',60),
        (59,9,29,'AB987CD','2026-03-04','17:00',150),
        (60,10,30,'EF654GH','2026-03-05','18:00',60),
        (61,1,1,'AB123CD','2026-03-06','08:00',60),
        (62,2,2,'EF456GH','2026-03-07','09:00',90),
        (63,3,3,'IJ789KL','2026-03-08','10:00',45),
        (64,4,4,'MN012OP','2026-03-09','11:00',120),
        (65,5,5,'QR345ST','2026-03-10','13:00',60),
        (66,6,6,'UV678WX','2026-03-11','14:00',30),
        (67,7,7,'YZ901AB','2026-03-12','15:00',90),
        (68,8,8,'CD234EF','2026-03-13','16:00',60),
        (69,9,9,'GH567IJ','2026-03-14','17:00',150),
        (70,10,10,'KL890MN','2026-03-15','18:00',60),
        (71,1,11,'OP123QR','2026-03-16','08:00',60),
        (72,2,12,'ST456UV','2026-03-17','09:00',90),
        (73,3,13,'WX789YZ','2026-03-18','10:00',45),
        (74,4,14,'AB987CD','2026-03-19','11:00',120),
        (75,5,15,'EF654GH','2026-03-20','13:00',60),
        (76,6,16,'AB123CD','2026-03-21','14:00',30),
        (77,7,17,'EF456GH','2026-03-22','15:00',90),
        (78,8,18,'IJ789KL','2026-03-23','16:00',60),
        (79,9,19,'MN012OP','2026-03-24','17:00',150),
        (80,10,20,'QR345ST','2026-03-25','18:00',60),
        (81,1,21,'UV678WX','2026-03-26','08:00',60),
        (82,2,22,'YZ901AB','2026-03-27','09:00',90),
        (83,3,23,'CD234EF','2026-03-28','10:00',45),
        (84,4,24,'GH567IJ','2026-03-29','11:00',120),
        (85,5,25,'KL890MN','2026-03-30','13:00',60),
        (86,6,26,'OP123QR','2026-03-31','14:00',30),
        (87,7,27,'ST456UV','2026-04-01','15:00',90),
        (88,8,28,'WX789YZ','2026-04-02','16:00',60),
        (89,9,29,'AB987CD','2026-04-03','17:00',150),
        (90,10,30,'EF654GH','2026-04-04','18:00',60),
        (91,1,1,'AB123CD','2026-04-05','08:00',60),
        (92,2,2,'EF456GH','2026-04-06','09:00',90),
        (93,3,3,'IJ789KL','2026-04-07','10:00',45),
        (94,4,4,'MN012OP','2026-04-08','11:00',120),
        (95,5,5,'QR345ST','2026-04-09','13:00',60),
        (96,6,6,'UV678WX','2026-04-10','14:00',30),
        (97,7,7,'YZ901AB','2026-04-11','15:00',90),
        (98,8,8,'CD234EF','2026-04-12','16:00',60),
        (99,9,9,'GH567IJ','2026-04-13','17:00',150),
        (100,10,10,'KL890MN','2026-04-14','18:00',60),
    ]
)

# Tipologia_Esame (2, già esistenti)
cursor.executemany(
    "INSERT OR IGNORE INTO Tipologia_Esame (Id_TE, Nome, Max_posti) VALUES (?, ?, ?)",
    [
        (1, 'Teorico', 30),
        (2, 'Pratico',   5),
    ]
)

# Esame (50 record)
# Punteggio è NULL per gli esami pratici.
cursor.executemany(
    "INSERT OR IGNORE INTO Esame (Id_E, Id_C, Data, Esito, Punteggio, Id_TE) VALUES (?, ?, ?, ?, ?, ?)",
    [
        (1,1,'2026-02-02','Superato',28,1),
        (2,2,'2026-02-04','Superato',24,1),
        (3,3,'2026-02-06','Non Superato',15,1),
        (4,4,'2026-02-08','Superato',None,2),
        (5,5,'2026-02-10','Non Superato',None,2),
        (6,6,'2026-02-12','Superato',30,1),
        (7,7,'2026-02-14','Superato',22,1),
        (8,8,'2026-02-16','Superato',None,2),
        (9,9,'2026-02-18','Non Superato',10,1),
        (10,10,'2026-02-20','Superato',None,2),
        (11,11,'2026-02-22','Superato',28,1),
        (12,12,'2026-02-24','Superato',24,1),
        (13,13,'2026-02-26','Non Superato',15,1),
        (14,14,'2026-02-28','Superato',None,2),
        (15,15,'2026-03-02','Non Superato',None,2),
        (16,16,'2026-03-04','Superato',30,1),
        (17,17,'2026-03-06','Superato',22,1),
        (18,18,'2026-03-08','Superato',None,2),
        (19,19,'2026-03-10','Non Superato',10,1),
        (20,20,'2026-03-12','Superato',None,2),
        (21,21,'2026-03-14','Superato',28,1),
        (22,22,'2026-03-16','Superato',24,1),
        (23,23,'2026-03-18','Non Superato',15,1),
        (24,24,'2026-03-20','Superato',None,2),
        (25,25,'2026-03-22','Non Superato',None,2),
        (26,26,'2026-03-24','Superato',30,1),
        (27,27,'2026-03-26','Superato',22,1),
        (28,28,'2026-03-28','Superato',None,2),
        (29,29,'2026-03-30','Non Superato',10,1),
        (30,30,'2026-04-01','Superato',None,2),
        (31,1,'2026-04-03','Superato',28,1),
        (32,2,'2026-04-05','Superato',24,1),
        (33,3,'2026-04-07','Non Superato',15,1),
        (34,4,'2026-04-09','Superato',None,2),
        (35,5,'2026-04-11','Non Superato',None,2),
        (36,6,'2026-04-13','Superato',30,1),
        (37,7,'2026-04-15','Superato',22,1),
        (38,8,'2026-04-17','Superato',None,2),
        (39,9,'2026-04-19','Non Superato',10,1),
        (40,10,'2026-04-21','Superato',None,2),
        (41,11,'2026-04-23','Superato',28,1),
        (42,12,'2026-04-25','Superato',24,1),
        (43,13,'2026-04-27','Non Superato',15,1),
        (44,14,'2026-04-29','Superato',None,2),
        (45,15,'2026-05-01','Non Superato',None,2),
        (46,16,'2026-05-03','Superato',30,1),
        (47,17,'2026-05-05','Superato',22,1),
        (48,18,'2026-05-07','Superato',None,2),
        (49,19,'2026-05-09','Non Superato',10,1),
        (50,20,'2026-05-11','Superato',None,2),
    ]
)

conn.commit()
print("Dati inseriti correttamente.\n")


# ─────────────────────────────────────────
# QUERY 1 — Lezioni di un candidato
#           con istruttore e veicolo
# ─────────────────────────────────────────

ID_CANDIDATO = 1   # ← modificare qui per cercare un candidato diverso

cursor.execute("""
    SELECT
        L.Data,
        L.Ora,
        L.Durata,
        I.Nome    AS Nome_Istruttore,
        I.Cognome AS Cognome_Istruttore,
        V.Targa,
        V.Modello
    FROM Lezione L
    JOIN Istruttore I ON L.Id_I  = I.Id_I
    JOIN Veicolo    V ON L.Targa = V.Targa
    WHERE L.Id_C = ?
    ORDER BY L.Data, L.Ora
""", (ID_CANDIDATO,))

rows = cursor.fetchall()
print(f"── Query 1: lezioni del candidato Id={ID_CANDIDATO} ──")
print(f"{'Data':<12} {'Ora':<6} {'Min':>4}  {'Istruttore':<20} {'Targa':<10} Veicolo")
print("-" * 70)
for r in rows:
    istruttore = f"{r[3]} {r[4]}"
    print(f"{r[0]:<12} {r[1]:<6} {r[2]:>4}  {istruttore:<20} {r[5]:<10} {r[6]}")
print()


# ─────────────────────────────────────────
# QUERY 2 — Esami superati per categoria
#           di patente
# ─────────────────────────────────────────

cursor.execute("""
    SELECT
        TP.Nome  AS Categoria_Patente,
        COUNT(*) AS Esami_Superati
    FROM Esame E
    JOIN Candidato        C  ON E.Id_C  = C.Id_C
    JOIN Tipologia_Patente TP ON C.Id_TP = TP.Id_TP
    WHERE E.Esito = 'Superato'
    GROUP BY TP.Id_TP, TP.Nome
    ORDER BY TP.Nome
""")

rows = cursor.fetchall()
print("── Query 2: esami superati per categoria di patente ──")
print(f"{'Categoria':<12} {'Esami superati':>14}")
print("-" * 28)
for r in rows:
    print(f"{r[0]:<12} {r[1]:>14}")
print()


# ─────────────────────────────────────────
# QUERY 3 — Voto medio per sessione d'esame
# ─────────────────────────────────────────

DATA_ESAME = '2026-06-10'   # ← modificare qui per una sessione diversa
ID_TIPO    = 1              # ← 1=Teorico, 2=Pratico

cursor.execute("""
    SELECT
        E.Data,
        T.Nome     AS Tipo_Esame,
        AVG(E.Punteggio) AS Voto_Medio
    FROM Esame E
    JOIN Tipologia_Esame T ON E.Id_TE = T.Id_TE
    WHERE E.Data  = ?
      AND E.Id_TE = ?
""", (DATA_ESAME, ID_TIPO))

row = cursor.fetchone()
print(f"── Query 3: voto medio della sessione {DATA_ESAME} (Id_TE={ID_TIPO}) ──")
if row and row[2] is not None:
    print(f"Data: {row[0]}  |  Tipo: {row[1]}  |  Voto medio: {row[2]:.2f}")
else:
    print("Nessun dato disponibile per questa sessione.")
print()


# ─────────────────────────────────────────
# CHIUSURA
# ─────────────────────────────────────────

conn.close()
print("Connessione chiusa.")
