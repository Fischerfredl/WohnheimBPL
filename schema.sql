DROP TABLE IF EXISTS Teilgenommen;
DROP TABLE IF EXISTS KOSpiel;
DROP TABLE IF EXISTS Ligaspiel;
DROP TABLE IF EXISTS Turnierspiel;
DROP TABLE IF EXISTS Spiel;
DROP TABLE IF EXISTS Unterwettbewerb;
DROP TABLE IF EXISTS Wettbewerb;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Spieler;

CREATE TABLE Spieler (
	SpielerID int NOT NULL PRIMARY KEY,
	Name varchar(20),
	Vorname varchar(20) NOT NULL,
	Nickname varchar(20) UNIQUE
);

CREATE TABLE Team (
	TeamID int NOT NULL PRIMARY KEY,
	Name varchar(40) NOT NULL UNIQUE
);

CREATE TABLE Wettbewerb (
	WbID int NOT NULL PRIMARY KEY,
	Name varchar(40) NOT NULL UNIQUE
);

CREATE TABLE Unterwettbewerb (
	UnterwbID int NOT NULL PRIMARY KEY,
	WbID int NOT NULL,
	Name varchar(40) UNIQUE,
	Modus varchar(7) NOT NULL CHECK (Modus = 'turnier' OR Modus = 'liga' OR Modus = 'ko'),
	OTN varchar(3) NOT NULL CHECK (OTN = 'ein' OR OTN = 'aus'),
	Start date NOT NULL,
	Ende date,
  	CONSTRAINT fk_WbUnterwb FOREIGN KEY (WbID) REFERENCES  Wettbewerb(WbID)
);

CREATE TABLE Spiel (
	SpielID int NOT NULL PRIMARY KEY,
	UnterwbID int NOT NULL,
	Team1ID int,
	Team2ID int,
	SiegerID int,
	Gewertet int NOT NULL DEFAULT 1,
	Datum date,
    CONSTRAINT fk_SpielUnterwb FOREIGN KEY (UnterwbID) REFERENCES Unterwettbewerb(UnterwbID),
    CONSTRAINT fk_SpielTeam1 FOREIGN KEY (Team1ID) REFERENCES Team(TeamID),
    CONSTRAINT fk_SpielTeam2 FOREIGN KEY (Team2ID) REFERENCES Team(TeamID),
    CONSTRAINT fk_SpielSieger FOREIGN KEY (SiegerID) REFERENCES Team(TeamID),
    CONSTRAINT chk_Gewertet CHECK(Gewertet = 0 OR Gewertet = 1)
);

CREATE TABLE Turnierspiel (
	SpielID int NOT NULL,
	Becherueber int CHECK (Becherueber <= 6),
    CONSTRAINT fk_Turnierspiel FOREIGN KEY (SpielID) REFERENCES Spiel(SpielID)
);

CREATE TABLE Ligaspiel (
	SpielID int NOT NULL,
	Spieltag int,
	Spieler1ID int,
	Spieler2ID int,
	Spieler3ID int,
	Spieler4ID int,
	Sp1tref int CHECK (Sp1tref <= 6),
	Sp2tref int CHECK (Sp2tref <= 6),
	Sp3tref int CHECK (Sp3tref <= 6),
	Sp4tref int CHECK (Sp4tref <= 6),
	T1tref int CHECK (T1tref <= 6),
	T2tref int CHECK (T2tref <= 6),
	T1Strafe int CHECK (T1Strafe <= 6),
	T2Strafe int CHECK (T2Strafe <= 6),
    CONSTRAINT fk_Ligaspiel FOREIGN KEY (SpielID) REFERENCES Spiel(SpielID),
    CONSTRAINT fk_LigaSpieler1 FOREIGN KEY (Spieler1ID) REFERENCES Spieler(SpielerID),
    CONSTRAINT fk_LigaSpieler2 FOREIGN KEY (Spieler2ID) REFERENCES Spieler(SpielerID),
    CONSTRAINT fk_LigaSpieler3 FOREIGN KEY (Spieler3ID) REFERENCES Spieler(SpielerID),
    CONSTRAINT fk_LigaSpieler4 FOREIGN KEY (Spieler4ID) REFERENCES Spieler(SpielerID)    
);

CREATE TABLE KOspiel (
	SpielID int NOT NULL,
	NFWinnerID int,
	NFLoserID int,
	Bestofwhat int DEFAULT 1,
	T1Erg int,
	T2Erg int,
    CONSTRAINT fk_KOspiel FOREIGN KEY (SpielID) REFERENCES Spiel(SpielID),
    CONSTRAINT fk_NWwin FOREIGN KEY (NFWinnerID) REFERENCES Spiel(SpielID),
    CONSTRAINT fk_NFLos FOREIGN KEY (NFLoserID) REFERENCES Spiel(SpielID)
);

CREATE TABLE Teilgenommen (
	UnterwbID int NOT NULL,
	TeamID int NOT NULL,
	SpielerID int NOT NULL, 
    CONSTRAINT fk_TGUnterwb FOREIGN KEY (UnterwbID) REFERENCES Unterwettbewerb(UnterwbID),
    CONSTRAINT fk_TGTeam FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
	CONSTRAINT fk_TGSpieler FOREIGN KEY (SpielerID) REFERENCES Spieler(SpielerID)
);                                      

INSERT INTO TEAM(TeamID, Name) VALUES (1, 'Fuckin Schnitzel');
INSERT INTO TEAM(TeamID, Name) VALUES (2, 'Bauernpower');
INSERT INTO TEAM(TeamID, Name) VALUES (3, 'The Beer Pong Theory');
INSERT INTO TEAM(TeamID, Name) VALUES (4, 'Party Palmen');
INSERT INTO TEAM(TeamID, Name) VALUES (5, 'Die drei Moustachiere');
INSERT INTO TEAM(TeamID, Name) VALUES (6, '3 guys 6 cups');
INSERT INTO TEAM(TeamID, Name) VALUES (7, 'Geil, geiler, Toaster');
INSERT INTO TEAM(TeamID, Name) VALUES (8, 'Drinky and the Brain');
INSERT INTO TEAM(TeamID, Name) VALUES (9, 'Die Jägermeister');
INSERT INTO TEAM(TeamID, Name) VALUES (10, 'Mahatma GönnDir');
INSERT INTO TEAM(TeamID, Name) VALUES (11, 'The Beer Pong Theory 2.0');
INSERT INTO TEAM(TeamID, Name) VALUES (12, 'The Walking Drunk');
INSERT INTO TEAM(TeamID, Name) VALUES (13, 'Here for Beer');
INSERT INTO TEAM(TeamID, Name) VALUES (14, 'Die Busfahrer');
INSERT INTO TEAM(TeamID, Name) VALUES (15, 'Cartofel');
INSERT INTO TEAM(TeamID, Name) VALUES (16, 'Drink 182');
INSERT INTO TEAM(TeamID, Name) VALUES (17, 'Sir, Cup & Cupper');
INSERT INTO TEAM(TeamID, Name) VALUES (18, '3.2.1...meins');
INSERT INTO TEAM(TeamID, Name) VALUES (19, 'Pong Fu Pandas');
INSERT INTO TEAM(TeamID, Name) VALUES (20, 'Boom Chicka Beer Pong');
INSERT INTO TEAM(TeamID, Name) VALUES (21, 'Benjamin Bierchen');
INSERT INTO TEAM(TeamID, Name) VALUES (22, 'Sir Hit-a-lot');
INSERT INTO TEAM(TeamID, Name) VALUES (23, 'Long John Beerpong');
INSERT INTO TEAM(TeamID, Name) VALUES (24, 'Die ExBeerTen');
INSERT INTO TEAM(TeamID, Name) VALUES (25, '(Schöne Scheiße)3');
INSERT INTO TEAM(TeamID, Name) VALUES (26, 'Gut und aussehend');
INSERT INTO TEAM(TeamID, Name) VALUES (27, 'Attack on Beer');
INSERT INTO TEAM(TeamID, Name) VALUES (28, 'Cup & Cupper');
INSERT INTO TEAM(TeamID, Name) VALUES (29, 'Pong Lenis');
INSERT INTO TEAM(TeamID, Name) VALUES (30, 'Die Bierpongbärchenbande');
INSERT INTO TEAM(TeamID, Name) VALUES (31, 'El Machado');
INSERT INTO TEAM(TeamID, Name) VALUES (32, 'Fuckin Nugget');

INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (1, 'Mack', 'Tobias', 'Tibo');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (2, 'Bickl', 'Matthias', 'Schnitzel');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (3, 'Pflugrad', 'Peter', 'Peter');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (4, 'Wolf', 'Julian', 'Jule');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (5, 'Schön', 'Stefan', 'Schön');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (6, 'Andraschko', 'Christian', 'Bri');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (7, 'Ellinger', 'Tobias', 'Elli');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (8, 'Wagner', 'Vanessa', 'Vanessa');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (9, 'Eichhoff', 'Robert', 'Robert E.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (10, 'Lacherstorfer', 'Jessica', 'Jessi');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (11, 'Baramidze', 'Nino', 'Nino');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (12, 'Reiche', 'Robert', 'Robert R.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (13, 'Kriwan', 'Martin', 'Kriwan');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (14, 'Benischke', 'Florian', 'Flo');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (15, 'Martin', 'Thomas', 'Thomas M.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (16, 'Aigner', 'Matthias', 'Matthias A.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (17, 'Seidel', 'Susi', 'Susi');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (18, 'Rausch', 'Britta', 'Britta');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (19, 'Petzak', 'Tobias', 'Petzi');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (20, 'Melch', 'Alfred', 'Alfred');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (21, 'Muschiol', 'Maya', 'Maya');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (22, 'Kayaci', 'Esra', 'Esra');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (23, 'Häusler', 'Katharina', 'Kathi');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (24, 'Schmöger', 'Stefan', 'Schmögi');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (25, 'Kulot', 'David', 'David');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (26, 'Kempka', 'Martin', 'Martin Ke.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (27, 'Nolde', 'Anna', 'Anna N.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (28, 'Lipfert', 'Salome', 'Salome');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (29, 'Mantaj', 'Julian', 'Julian');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (30, null, 'Lena', 'Lena');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (31, null, 'Sebastian', 'Sebastian');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (32, 'Seemüller', 'Martin', 'Martin S.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (33, 'Vesenberg', 'Dennis', 'Sir');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (34, 'Gassmann', 'Daniel', 'Gassi');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (35, null, 'Mario', 'Mario');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (36, 'Mayer', 'Phillip', 'PM');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (37, 'Huber', 'Jessi', 'Jessi H.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (38, null, 'Philip', 'Philip');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (39, 'Mayer', 'Chris', 'CM');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (40, 'Meckes', 'Caro', 'Caro');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (41, 'Herre', 'Alexander', 'Toaster');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (42, 'Bittracher', 'Martin', 'Magic');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (43, 'Herrmann', 'Steffen', 'Steffen');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (44, 'Wagner', 'Sandro', 'Sandro');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (45, 'Rieder', 'Manuel', 'Manu');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (46, 'Frosch', 'Dennis', 'Frog');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (47, null, 'Natalie', 'Natalie');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (48, 'Otte', 'Felix', 'Felix');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (49, 'Wohllaib', 'Jacqueline', 'Shacky');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (50, 'Herbinger', 'Martin', 'Hoerby');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (51, null, 'Marcel', 'Marcel');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (52, null, 'Patrick', 'Patrick');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (53, 'Olschewski', 'Patrick', 'Paddy');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (54, null, 'Michael', 'Michael');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (55, 'Wassermann', 'Manuel', 'Manu W.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (56, 'Hahn', 'Michael', 'Michi H.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (57, 'Kerstiens', 'Franziska', 'Franzi');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (58, 'Eberle', 'Anna', 'Anna E.');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (59, 'J', 'Jannik', 'Jannik J');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (60, 'G', 'Johannes', 'Johannes G');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (61, null, 'Hana', 'Hana');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (62, 'G', 'Chris', 'Chris G');
INSERT INTO Spieler(SpielerID, Name, Vorname, Nickname) VALUES (63, null, 'Chris', 'Chris');

INSERT INTO  Wettbewerb(WbID, Name) VALUES (1, 'WS 14/15');
INSERT INTO  Wettbewerb(WbID, Name) VALUES (2, 'SS 15');
INSERT INTO  Wettbewerb(WbID, Name) VALUES (3, 'WS 15/16');

INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name, Modus, OTN, Start, Ende) VALUES (1, 1, '14/15 liga', 'liga', 'ein', '2014-11-30', '2015-02-01');
INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name, Modus, OTN, Start, Ende) VALUES (2, 2, '15 liga', 'liga', 'ein', '2015-04-30', '2015-07-14');
INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name, Modus, OTN, Start, Ende) VALUES (3, 3, '15/16 REL', 'liga', 'ein', '2015-11-01', '2015-12-22');
INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name, Modus, OTN, Start, Ende) VALUES (4, 3, '15/16 TSL', 'liga', 'ein', '2015-11-01', '2015-12-22');
INSERT INTO Unterwettbewerb(UnterwbID, WbID, Name, Modus, OTN, Start, Ende) VALUES (5, 3, '15/16 Play-Offs', 'ko', 'ein', '2016-01-10', '2016-01-26');

INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 1, 1);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 1, 2);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 2, 3);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 2, 4);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 3, 5);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 3, 6);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 3, 39);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 4, 7);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 4, 8);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 4, 9);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 5, 10);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 5, 11);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 5, 12);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 6, 13);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 6, 14);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 6, 15);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 7, 16);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 7, 41);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 7, 58);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 8, 17);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 8, 18);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 8, 19);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 9, 20);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 9, 21);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 9, 22);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 9, 23);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 10, 24);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (1, 10, 25);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 2, 3);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 2, 4);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 11, 5);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 11, 39);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 11, 54);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 12, 25);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 12, 21);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 13, 10);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 13, 11);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 13, 55);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 14, 45);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 14, 46);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 1, 1);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 1, 2);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 15, 40);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 15, 41);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 15, 48);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 16, 56);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 16, 18);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 16, 19);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 6, 13);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 6, 14);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 6, 15);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 17, 16);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 17, 33);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 17, 58);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 4, 7);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 4, 8);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 4, 9);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 18, 20);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 18, 57);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (2, 18, 49);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 19, 26);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 19, 27);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 19, 10);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 20, 21);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 20, 25);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 20, 28);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 2, 3);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 2, 4);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 2, 29);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 21, 30);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 21, 31);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 22, 32);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 22, 33);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 22, 34);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 16, 17);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 16, 18);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 16, 19);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 23, 35);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 23, 36);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 23, 37);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 24, 59);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 24, 60);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 24, 61);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 25, 5);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 25, 38);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (3, 25, 39);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 26, 40);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 26, 41);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 27, 42);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 27, 43);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 27, 44);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 6, 13);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 6, 14);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 6, 15);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 28, 58);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 28, 16);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 29, 45);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 29, 46);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 29, 47);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 32, 1);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 32, 48);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 32, 62);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 30, 49);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 30, 53);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 30, 20);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 4, 7);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 4, 9);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 4, 50);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 31, 51);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 31, 52);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (4, 31, 63);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 19, 26);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 19, 27);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 19, 10);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 2, 3);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 2, 4);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 2, 29);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 22, 32);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 22, 33);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 22, 34);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 16, 17);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 16, 18);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 16, 19);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 26, 40);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 26, 41);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 29, 45);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 29, 46);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 29, 47);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 4, 7);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 4, 9);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 4, 50);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 31, 51);
INSERT INTO Teilgenommen(UnterwbID, TeamID, SpielerID) VALUES (5, 31, 52);

INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (1, 1, 10, 6, 10, 1, '2014-12-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (2, 1, 7, 8, 7, 1, '2014-12-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (3, 1, 9, 3, 3, 1, '2014-12-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (4, 1, 5, 1, 1, 1, '2014-12-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (5, 1, 4, 2, 4, 1, '2014-12-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (6, 1, 4, 9, 9, 1, '2014-12-08');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (7, 1, 1, 10, 1, 1, '2014-12-08');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (8, 1, 2, 5, 2, 1, '2014-12-08');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (9, 1, 8, 6, 6, 1, '2014-12-08');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (10, 1, 3, 7, 3, 1, '2014-12-08');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (11, 1, 7, 1, 1, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (12, 1, 5, 3, 5, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (13, 1, 9, 8, 8, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (14, 1, 6, 2, 2, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (15, 1, 10, 4, 10, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (16, 1, 4, 5, 4, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (17, 1, 9, 6, 6, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (18, 1, 8, 10, 8, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (19, 1, 2, 7, 2, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (20, 1, 3, 1, 1, 1, '2014-12-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (21, 1, 1, 9, 9, 1, '2015-01-12');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (22, 1, 10, 3, 10, 1, '2015-01-12');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (23, 1, 2, 8, 8, 1, '2015-01-12');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (24, 1, 7, 4, 4, 1, '2015-01-12');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (25, 1, 6, 5, 6, 1, '2015-01-12');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (26, 1, 5, 9, 5, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (27, 1, 8, 1, 8, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (28, 1, 6, 7, 7, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (29, 1, 3, 4, 4, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (30, 1, 10, 2, 2, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (31, 1, 2, 3, 3, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (32, 1, 7, 9, 9, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (33, 1, 1, 6, 6, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (34, 1, 4, 8, 4, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (35, 1, 5, 10, 5, 1, '2015-01-19');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (36, 1, 6, 4, 6, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (37, 1, 3, 8, null, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (38, 1, 1, 2, 1, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (39, 1, 9, 10, null, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (40, 1, 7, 5, 7, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (41, 1, 1, 4, 1, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (42, 1, 10, 7, 7, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (43, 1, 6, 3, 3, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (44, 1, 8, 5, null, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (45, 1, 9, 2, 2, 1, '2015-01-26');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (46, 2, 1, 17, 1, 1, '2015-05-04');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (47, 2, 15, 13, 13, 1, '2015-05-04');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (48, 2, 12, 11, 12, 1, '2015-05-04');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (49, 2, 6, 2, 2, 1, '2015-05-04');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (50, 2, 18, 4, 4, 1, '2015-05-04');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (51, 2, 14, 16, 14, 1, '2015-05-04');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (52, 2, 16, 1, 16, 1, '2015-05-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (53, 2, 4, 14, 14, 1, '2015-05-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (54, 2, 2, 18, 2, 1, '2015-05-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (55, 2, 11, 6, 11, 1, '2015-05-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (56, 2, 13, 12, 12, 1, '2015-05-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (57, 2, 17, 15, 15, 1, '2015-05-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (58, 2, 1, 15, 15, 1, '2015-05-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (59, 2, 12, 17, 12, 1, '2015-05-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (60, 2, 6, 13, 13, 1, '2015-05-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (61, 2, 18, 11, 11, 1, '2015-05-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (62, 2, 14, 2, 14, 1, '2015-05-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (63, 2, 16, 4, 16, 1, '2015-05-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (64, 2, 4, 1, 1, 1, '2015-06-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (65, 2, 2, 16, 2, 1, '2015-06-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (66, 2, 11, 14, 11, 1, '2015-06-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (67, 2, 13, 18, 13, 1, '2015-06-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (68, 2, 17, 6, 6, 1, '2015-06-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (69, 2, 15, 12, 12, 1, '2015-06-01');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (70, 2, 1, 12, 12, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (71, 2, 6, 15, 15, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (72, 2, 18, 17, 17, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (73, 2, 14, 13, 14, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (74, 2, 16, 11, 11, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (75, 2, 4, 2, 2, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (76, 2, 2, 1, 1, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (77, 2, 11, 4, 11, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (78, 2, 13, 16, 13, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (79, 2, 17, 14, 17, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (80, 2, 15, 18, 15, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (81, 2, 12, 6, 12, 1, '2015-06-15');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (82, 2, 1, 6, 1, 1, '2015-06-22');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (83, 2, 18, 12, 12, 1, '2015-06-22');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (84, 2, 14, 15, 14, 1, '2015-06-22');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (85, 2, 16, 17, 16, 1, '2015-06-22');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (86, 2, 4, 13, 13, 1, '2015-06-22');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (87, 2, 2, 11, 2, 1, '2015-06-22');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (88, 2, 11, 1, 11, 1, '2015-06-29');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (89, 2, 13, 2, 2, 1, '2015-06-29');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (90, 2, 17, 4, 17, 1, '2015-06-29');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (91, 2, 15, 16, 16, 1, '2015-06-29');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (92, 2, 12, 14, 14, 1, '2015-06-29');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (93, 2, 6, 18, 6, 1, '2015-06-29');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (94, 2, 1, 18, 1, 1, '2015-07-06');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (95, 2, 14, 6, 14, 1, '2015-07-06');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (96, 2, 16, 12, 12, 1, '2015-07-06');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (97, 2, 4, 15, 4, 1, '2015-07-06');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (98, 2, 2, 17, 2, 1, '2015-07-06');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (99, 2, 11, 13, 13, 1, '2015-07-06');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (100, 2, 13, 1, 13, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (101, 2, 17, 11, 11, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (102, 2, 15, 2, 2, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (103, 2, 12, 4, 12, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (104, 2, 6, 16, 6, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (105, 2, 18, 14, 14, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (106, 2, 1, 14, 1, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (107, 2, 16, 18, 16, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (108, 2, 4, 6, 6, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (109, 2, 2, 12, 2, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (110, 2, 11, 15, 11, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (111, 2, 13, 17, 13, 1, '2015-07-13');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (112, 3, 16, 20, 20, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (113, 3, 24, 23, 24, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (114, 3, 25, 21, 25, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (115, 3, 19, 2, 19, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (116, 3, 19, 23, 19, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (117, 3, 25, 2, 25, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (118, 3, 20, 24, 20, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (119, 3, 16, 22, 16, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (120, 3, 25, 23, 25, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (121, 3, 24, 19, 19, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (122, 3, 20, 22, 20, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (123, 3, 16, 21, 16, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (124, 3, 25, 19, 19, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (125, 3, 16, 2, 2, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (126, 3, 22, 24, 22, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (127, 3, 20, 21, 20, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (128, 3, 16, 23, 16, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (129, 3, 20, 2, 2, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (130, 3, 24, 25, 24, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (131, 3, 22, 21, 22, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (132, 3, 23, 20, 23, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (133, 3, 16, 19, 16, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (134, 3, 21, 24, 21, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (135, 3, 22, 2, 22, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (136, 3, 21, 2, 2, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (137, 3, 23, 22, 22, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (138, 3, 19, 20, 19, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (139, 3, 16, 25, 25, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (140, 3, 19, 22, 19, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (141, 3, 2, 24, 2, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (142, 3, 25, 20, 25, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (143, 3, 23, 21, 21, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (144, 3, 25, 22, 22, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (145, 3, 23, 2, 2, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (146, 3, 24, 16, 16, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (147, 3, 19, 21, 21, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (148, 4, 30, 27, 27, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (149, 4, 31, 4, 4, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (150, 4, 32, 29, 29, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (151, 4, 26, 6, 26, 1, '2015-11-02');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (152, 4, 26, 4, 26, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (153, 4, 32, 28, 32, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (154, 4, 27, 31, 31, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (155, 4, 30, 29, 30, 1, '2015-11-09');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (156, 4, 32, 6, 32, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (157, 4, 31, 26, 26, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (158, 4, 27, 29, 27, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (159, 4, 30, 28, 28, 1, '2015-11-16');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (160, 4, 32, 4, 4, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (161, 4, 30, 6, 6, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (162, 4, 29, 31, 29, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (163, 4, 27, 28, 27, 1, '2015-11-23');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (164, 4, 32, 26, 32, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (165, 4, 30, 4, 4, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (166, 4, 27, 6, 27, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (167, 4, 29, 28, 29, 1, '2015-11-30');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (168, 4, 4, 27, 4, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (169, 4, 30, 26, 26, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (170, 4, 28, 31, 28, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (171, 4, 29, 6, 29, 1, '2015-12-07');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (172, 4, 28, 6, 6, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (173, 4, 4, 29, 29, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (174, 4, 26, 27, 26, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (175, 4, 31, 32, 32, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (176, 4, 26, 29, 29, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (177, 4, 6, 31, 6, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (178, 4, 30, 32, 30, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (179, 4, 4, 28, 28, 1, '2015-12-14');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (180, 4, 4, 6, 4, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (181, 4, 31, 30, 31, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (182, 4, 32, 27, 27, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (183, 4, 26, 28, 26, 1, '2015-12-21');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (184, 5, 32, 22, 22, 1, '2016-01-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (185, 5, 19, 29, 19, 1, '2016-01-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (186, 5, 26, 16, 26, 1, '2016-01-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (187, 5, 2, 4, 2, 1, '2016-01-11');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (188, 5, 2, 22, 22, 1, '2016-01-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (189, 5, 19, 26, 19, 1, '2016-01-18');
INSERT INTO Spiel(SpielID, UnterwbID, Team1ID, Team2ID, SiegerID, Gewertet, Datum) VALUES (190, 5, 22, 19, 22, 1, '2016-01-25');

INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (1, 1, 24, 25, 14, 15, 3, 3, 0, 1, 6, 1, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (2, 1, 58, 16, 17, 18, 3, 3, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (3, 1, 20, 22, 5, 6, 1, 3, 5, 1, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (4, 1, 11, 10, 2, 1, 2, 3, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (5, 1, 8, 9, 4, 3, 4, 2, 0, 0, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (6, 2, 9, 8, 21, 22, 0, 2, 2, 4, 2, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (7, 2, 1, 2, 24, 25, 4, 2, 5, 0, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (8, 2, 3, 4, 12, 10, 4, 2, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (9, 2, 18, 19, 14, 13, 4, 1, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (10, 2, 39, 6, 58, 41, 3, 3, 2, 1, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (11, 3, 41, 58, 1, 2, 2, 1, 4, 2, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (12, 3, 11, 12, 5, 6, 4, 2, 2, 2, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (13, 3, 20, 21, 17, 19, 3, 2, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (14, 3, 14, 13, 3, 4, 1, 2, 3, 3, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (15, 3, 25, 24, 8, 9, 3, 3, 1, 4, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (16, 4, 7, 9, 12, 10, 3, 3, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (17, 4, 20, 21, 15, 13, 4, 1, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (18, 4, 18, 17, 24, 25, 6, 0, 5, 0, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (19, 4, 3, 4, 58, 41, 2, 4, 2, 0, 6, 2, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (20, 4, 39, 5, 1, 2, 2, 3, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (21, 5, 2, 1, 20, 21, 3, 2, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (22, 5, 24, 25, 39, 6, 4, 2, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (23, 5, 3, 4, 18, 17, 2, 3, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (24, 5, 58, 16, 7, 9, 0, 5, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (25, 5, 14, 15, 10, 11, 4, 2, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (26, 6, 12, 11, 23, 21, 3, 3, 0, 5, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (27, 6, 17, 18, 1, 2, 1, 5, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (28, 6, 13, 15, 58, 16, 3, 2, 5, 1, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (29, 6, 39, 5, 7, 8, 2, 3, 5, 1, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (30, 6, 24, 25, 3, 4, 0, 3, 2, 4, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (31, 7, 3, 4, 5, 6, 4, 1, 4, 1, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (32, 7, 58, 16, 20, 21, 2, 3, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (33, 7, 1, 2, 13, 14, 2, 2, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (34, 7, 8, 9, 17, 18, 1, 5, 1, 3, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (35, 7, 12, 11, 24, 25, 0, 6, 2, 1, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (36, 8, null, null, null, null, null, null, null, null, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (37, 8, null, null, null, null, null, null, null, null, null, null, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (38, 8, null, null, null, null, null, null, null, null, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (39, 8, null, null, null, null, null, null, null, null, null, null, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (40, 8, null, null, null, null, null, null, null, null, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (41, 9, null, null, null, null, null, null, null, null, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (42, 9, null, null, null, null, null, null, null, null, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (43, 9, null, null, null, null, null, null, null, null, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (44, 9, null, null, null, null, null, null, null, null, null, null, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (45, 9, null, null, null, null, null, null, null, null, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (46, 1, 1, 2, 33, 58, 2, 4, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (47, 1, 40, 41, 10, 55, 1, 2, 4, 2, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (48, 1, 21, 25, 5, 54, 5, 1, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (49, 1, 13, 15, 3, 4, 3, 2, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (50, 1, 57, 20, 9, 8, 2, 3, 5, 1, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (51, 1, 46, 45, 18, 19, 5, 1, 5, 0, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (52, 2, 18, 19, 1, 2, 3, 3, 1, 4, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (53, 2, 7, 8, 46, 45, 5, 0, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (54, 2, 4, 3, 49, 20, 2, 4, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (55, 2, 39, 54, 14, 13, 3, 3, 3, 0, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (56, 2, 11, 55, 21, 25, 5, 0, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (57, 2, 17, 58, 40, 41, 4, 0, 4, 2, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (58, 3, 1, 2, 40, 41, 3, 2, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (59, 3, 21, 25, 33, 17, 2, 4, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (60, 3, 14, 15, 11, 10, 4, 1, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (61, 3, 49, 57, 39, 5, 2, 1, 2, 4, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (62, 3, 46, 45, 3, 4, 3, 3, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (63, 3, 19, 18, 7, 8, 5, 1, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (64, 4, 7, 8, 1, 2, 1, 4, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (65, 4, 3, 4, 19, 18, 4, 2, 2, 1, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (66, 4, 5, 54, 46, 45, 5, 1, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (67, 4, 11, 10, 49, 57, 3, 3, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (68, 4, 33, 58, 14, 13, 2, 2, 2, 4, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (69, 4, 40, 41, 21, 25, 2, 3, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (70, 5, 1, 2, 21, 25, 3, 1, 4, 2, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (71, 5, 14, 15, 40, 41, 3, 1, 3, 3, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (72, 5, 57, 20, 17, 58, 0, 3, 4, 2, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (73, 5, 46, 45, 11, 55, 5, 1, 1, 4, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (74, 5, 19, 18, 39, 54, 1, 0, 4, 2, 1, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (75, 5, 9, 8, 3, 4, 1, 2, 3, 3, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (76, 6, 3, 4, 1, 2, 2, 2, 5, 1, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (77, 6, 39, 5, 9, 8, 2, 4, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (78, 6, 10, 55, 19, 18, 2, 4, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (79, 6, 33, 17, 46, 45, 3, 3, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (80, 6, 41, 40, 57, 20, 3, 3, 2, 1, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (81, 6, 21, 25, 13, 15, 3, 3, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (82, 7, 1, 2, 14, 13, 2, 4, 1, 3, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (83, 7, 49, 20, 21, 25, 1, 4, 5, 1, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (84, 7, 46, 45, 40, 41, 2, 4, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (85, 7, 18, 56, 17, 58, 3, 3, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (86, 7, 7, 8, 11, 10, 2, 2, 4, 2, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (87, 7, 3, 4, 39, 5, 6, 0, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (88, 8, 39, 5, 1, 2, 3, 3, 3, 0, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (89, 8, 10, 55, 3, 4, 3, 2, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (90, 8, 33, 58, 9, 8, 5, 1, 0, 2, 6, 2, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (91, 8, 40, 41, 18, 19, 2, 3, 3, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (92, 8, 21, 25, 46, 45, 1, 4, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (93, 8, 14, 15, 49, 20, 4, 2, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (94, 9, 1, 2, 49, 57, 5, 1, 1, 0, 6, 1, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (95, 9, 46, 45, 14, 15, 4, 2, 1, 3, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (96, 9, 19, 18, 21, 25, 1, 4, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (97, 9, 9, 7, 40, 41, 5, 1, 1, 4, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (98, 9, 3, 4, 33, 17, 3, 3, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (99, 9, 39, 54, 11, 55, 2, 3, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (100, 10, 11, 55, 1, 2, 4, 2, 5, 0, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (101, 10, 33, 58, 5, 54, 2, 2, 3, 3, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (102, 10, 40, 41, 3, 4, 2, 2, 3, 3, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (103, 10, 21, 25, 9, null, 3, 3, 2, null, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (104, 10, 13, 15, 19, 18, 4, 2, 1, 4, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (105, 10, 49, 20, 46, 45, 2, 2, 4, 2, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (106, 11, 1, 2, 46, 45, 3, 3, 2, 2, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (107, 11, 19, 18, 49, 20, 2, 4, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (108, 11, 9, null, 14, 13, 4, null, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (109, 11, 3, 4, 25, 21, 2, 4, 1, 3, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (110, 11, 5, 54, 40, 41, 5, 1, 1, 4, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (111, 11, 11, 10, 33, 58, 5, 1, 2, 2, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (112, 1, 17, 18, 28, 21, 0, 4, 5, 1, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (113, 1, 60, 59, 35, 36, 0, 6, 4, 0, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (114, 1, 5, 38, 30, 31, 4, 2, 0, 1, 6, 1, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (115, 1, 26, 27, 3, 4, 2, 4, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (116, 2, 10, 26, 35, 37, 3, 3, 2, 1, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (117, 2, 5, 39, 3, 4, 3, 3, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (118, 2, 25, 21, 60, 59, 2, 4, 0, 5, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (119, 2, 19, 18, 32, 34, 3, 3, 1, 3, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (120, 3, 38, 39, 35, 36, 3, 3, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (121, 3, 60, 59, 10, 27, 1, 2, 3, 3, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (122, 3, 25, 21, 33, 34, 3, 3, 1, 1, 6, 2, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (123, 3, 17, 18, 30, 31, 2, 4, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (124, 4, 5, 38, 26, 27, 2, 2, 4, 2, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (125, 4, 17, 18, 3, 29, 0, 5, 5, 1, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (126, 4, 32, 34, 60, 59, 3, 3, 2, 2, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (127, 4, 28, 25, 30, 31, 4, 2, 1, 1, 6, 2, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (128, 5, 17, 19, 35, 37, 3, 3, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (129, 5, 28, 21, 3, 29, 2, 1, 4, 2, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (130, 5, 60, 59, 5, 39, 2, 4, 5, 0, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (131, 5, 32, 33, 30, 31, 4, 2, 1, 4, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (132, 6, 35, 36, 28, 21, 5, 1, 2, 2, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (133, 6, 19, 18, 10, 26, 3, 3, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (134, 6, 30, 31, 60, 59, 2, 4, 2, 2, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (135, 6, 33, 34, 4, 29, 1, 5, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (136, 7, 30, 31, 3, 29, 1, 4, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (137, 7, 35, 36, 32, 33, 3, 1, 4, 2, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (138, 7, 10, 27, 28, 25, 4, 2, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (139, 7, 19, 18, 38, 39, 3, 2, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (140, 8, 26, 27, 33, 34, 4, 2, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (141, 8, 3, 29, 60, 59, 2, 4, 0, 5, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (142, 8, 5, 38, 25, 21, 4, 2, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (143, 8, 35, 36, 30, 31, 3, 2, 3, 3, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (144, 9, 5, 39, 32, 34, 1, 2, 0, 6, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (145, 9, 35, 36, 3, 4, 1, 1, 3, 3, 2, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (146, 9, 60, 61, 19, 18, 1, 2, 1, 5, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (147, 9, 10, 26, 30, 31, 2, 3, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (148, 1, 20, 49, 42, 44, 1, 2, 3, 3, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (149, 1, 51, 63, 50, 9, 0, 3, 4, 2, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (150, 1, 1, 48, 45, 46, 1, 5, 2, 1, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (151, 1, 40, 41, 14, 13, 2, 4, 1, 3, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (152, 2, 40, 41, 50, 9, 3, 3, 2, 2, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (153, 2, 48, 62, 58, 16, 2, 4, 3, 0, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (154, 2, 42, 43, 52, 63, 2, 3, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (155, 2, 20, 49, 46, 47, 2, 4, 2, 1, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (156, 3, 1, 48, 15, 13, 4, 2, 0, 1, 6, 1, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (157, 3, 51, 63, 40, 41, 3, 2, 1, 5, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (158, 3, 42, 44, 45, 46, 3, 3, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (159, 3, 20, 49, 58, 16, 2, 0, 5, 1, 2, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (160, 4, 1, 48, 7, 50, 4, 1, 1, 5, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (161, 4, 20, 49, 14, 15, 1, 3, 3, 3, 4, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (162, 4, 45, 46, 51, 52, 3, 3, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (163, 4, 43, 44, 58, 16, 3, 3, 4, 1, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (164, 5, 1, 48, 40, 41, 2, 4, 1, 0, 6, 1, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (165, 5, 20, 53, 7, 50, 1, 4, 5, 1, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (166, 5, 42, 44, 15, 13, 4, 2, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (167, 5, 45, 46, 58, 16, 2, 4, 3, 2, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (168, 6, 50, 9, 42, 43, 1, 4, 2, 2, 6, 4, 1, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (169, 6, 20, 53, 40, 41, 2, 1, 4, 2, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (170, 6, 58, 16, 51, 52, 3, 3, 2, 3, 6, 5, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (171, 6, 45, 46, 15, 13, 3, 3, 3, 1, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (172, 7, 58, 16, 14, 13, 2, 1, 3, 3, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (173, 7, 7, 50, 45, 46, 2, 1, 2, 4, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (174, 7, 40, 41, 42, 44, 2, 4, 1, 2, 6, 3, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (175, 7, 52, 63, 1, 48, 2, 1, 4, 2, 3, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (176, 8, 40, 41, 45, 46, 2, 3, 2, 4, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (177, 8, 15, 13, 51, 52, 2, 4, 3, 1, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (178, 8, 20, 53, 1, 48, 2, 3, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (179, 8, 7, 50, 58, 16, 4, 1, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (180, 9, 50, 9, 15, 13, 3, 3, 3, 1, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (181, 9, 51, 63, 20, 49, 2, 4, 1, 3, 6, 4, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (182, 9, 1, 48, 43, 44, 4, 1, 4, 2, 5, 6, 0, 0);
INSERT INTO Ligaspiel(SpielID, Spieltag, Spieler1ID, Spieler2ID, Spieler3ID, Spieler4ID, Sp1tref, Sp2tref, Sp3tref, Sp4tref, T1tref, T2tref, T1Strafe, T2Strafe) VALUES (183, 9, 40, 41, 58, 16, 4, 2, 0, 2, 6, 2, 0, 0);

INSERT INTO Kospiel(SpielID, NFWinnerID, NFLoserID, Bestofwhat, T1Erg, T2Erg) VALUES (184, 188, null, 3, 0, 2);
INSERT INTO Kospiel(SpielID, NFWinnerID, NFLoserID, Bestofwhat, T1Erg, T2Erg) VALUES (185, 189, null, 3, 2, 0);
INSERT INTO Kospiel(SpielID, NFWinnerID, NFLoserID, Bestofwhat, T1Erg, T2Erg) VALUES (186, 189, null, 3, 2, 0);
INSERT INTO Kospiel(SpielID, NFWinnerID, NFLoserID, Bestofwhat, T1Erg, T2Erg) VALUES (187, 188, null, 3, 2, 0);
INSERT INTO Kospiel(SpielID, NFWinnerID, NFLoserID, Bestofwhat, T1Erg, T2Erg) VALUES (188, 190, null, 3, 1, 2);
INSERT INTO Kospiel(SpielID, NFWinnerID, NFLoserID, Bestofwhat, T1Erg, T2Erg) VALUES (189, 190, null, 3, 2, 0);
INSERT INTO Kospiel(SpielID, NFWinnerID, NFLoserID, Bestofwhat, T1Erg, T2Erg) VALUES (190, null, null, 5, 3, 0);