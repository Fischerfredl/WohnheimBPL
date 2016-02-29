# WohnheimBPL
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
	Name varchar(40) NOT NULL UNIQUE,
	Start date
);

CREATE TABLE Unterwettbewerb (
	UnterwbID int NOT NULL PRIMARY KEY,
	WbID int NOT NULL FOREIGN KEY REFERENCES Wettbewerb(WbID),
	Name varchar(40) UNIQUE,
	Modus varchar(7) NOT NULL CHECK (Modus = 'turnier' OR Modus = 'liga' OR Modus = 'ko'),
	OTN varchar(3) NOT NULL CHECK (OTN = 'ein' OR OTN = 'aus'),
);

CREATE TABLE Spiel (
	SpielID int NOT NULL PRIMARY KEY,
	UnterwbID int NOT NULL FOREIGN KEY REFERENCES Unterwettbewerb(UnterwbID),
	Team1ID int FOREIGN KEY REFERENCES Team(TeamID),
	Team2ID int FOREIGN KEY REFERENCES Team(TeamID),
	SiegerID int FOREIGN KEY REFERENCES Team(TeamID),
	Gewertet int NOT NULL CHECK(Gewertet = 0 OR Gewertet = 1) DEFAULT 1,
);

CREATE TABLE Turnierspiel (
	SpielID int NOT NULL FOREIGN KEY REFERENCES Spiel(SpielID),
	Becherueber int CHECK (Becherueber <= 6)
);

CREATE TABLE Ligaspiel (
	SpielID int NOT NULL FOREIGN KEY REFERENCES Spiel(SpielID),
	Spieltag int,
	Spieler1ID int FOREIGN KEY REFERENCES Spieler(SpielerID),
	Spieler2ID int FOREIGN KEY REFERENCES Spieler(SpielerID),
	Spieler3ID int FOREIGN KEY REFERENCES Spieler(SpielerID),
	Spieler4ID int FOREIGN KEY REFERENCES Spieler(SpielerID),
	Sp1tref int CHECK (Sp1tref < = 6),
	Sp2tref int CHECK (Sp2tref < = 6),
	Sp3tref int CHECK (Sp3tref < = 6),
	Sp4tref int CHECK (Sp4tref < = 6),
	T1tref int CHECK (T1tref <= 6),
	T2tref int CHECK (T2tref <= 6),
	T1Strafe int CHECK (T1Strafe <= 6),
	T2Strafe int CHECK (T2Strafe <= 6)
);

CREATE TABLE KOspiel (
	SpielID int NOT NULL FOREIGN KEY REFERENCES Spiel(SpielID),
	NFWinnerID int FOREIGN KEY REFERENCES Spiel(SpielID),
	NFLoserID int FOREIGN KEY REFERENCES Spiel(SpielID),
	Bestofwhat int DEFAULT 1,
	T1Erg int,
	T2Erg int
);

CREATE TABLE Teilgenommen (
	UnterwbID int NOT NULL FOREIGN KEY REFERENCES Unterwettbewerb(UnterwbID),
	TeamID int NOT NULL FOREIGN KEY REFERENCES Team(TeamID),
	SpielerID int NOT NULL FOREIGN KEY REFERENCES Spieler(SpielerID)
);
