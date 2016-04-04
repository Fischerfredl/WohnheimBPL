from app import g

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0][0] if rv else None) if one else rv

def getSpieler():
    d = query_db("select * from Spieler")
    return d

def getTeams():
    cur = g.db.execute("select TeamID, Name from Team")
    return [dict(ID=row[0], Name=row[1]) for row in cur.fetchall()]

# returns SpielErgebnis depending on type:
# Ligaspiel - tuple: (SpielID, Erg1, Team1, T1Tref, T2Tref, T2, Erg2, Spieltag, spielerlist[] {list with tuples (spieler, treffer)})
# Turnierspiel - tuple: (SpielID, Team1, Team2, Sieger, Becherueber)
# KOSpiel - tuple: (SpielID, Team1, Erg1, Erg2, Team2)
def getSpielErgebnis(gameid):
    modus = query_db('SELECT (SELECT Modus FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = Spiel.UnterwbID) FROM Spiel Where SpielID = ?', [gameid], one=True)
    if modus == 'liga':
        tuple =  query_db("SELECT Spiel.SpielID, \
                        (SELECT CASE WHEN T1Tref = 6 THEN CASE WHEN T2Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T1Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg1, \
                        (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID) AS T1, \
                        T1Tref, T2Tref, \
                        (SELECT Name From Team WHERE Team.TeamID = Spiel.Team2ID) AS T2, \
                        (SELECT CASE WHEN T2Tref = 6 THEN CASE WHEN T1Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T2Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg2, \
                         Ligaspiel.Spieltag \
                        FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spiel.SpielID = ? ", [gameid])[0]
        spielerlist = []
        for spieler in query_db('SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Ligaspieler.SpielerID), Treffer FROM Ligaspieler WHERE SpielID = ? ', [gameid]):
            spielerlist.append(spieler)
        tuple = tuple + (spielerlist,)
        return tuple
    elif modus == 'turnier':
        return query_db('SELECT Spiel.SpielID, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID), \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team2ID), \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.SiegerID), \
                    Becherueber \
                    FROM Spiel Inner Join Turnierspiel ON Spiel.SpielID = Turnierspiel.SpielID \
                    WHERE Spiel.SpielID = ?', [gameid])[0]
    else:  # modus =='ko'
        return query_db('SELECT Spiel.SpielID, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID), \
                    T1Erg, \
                    T2Erg, \
                    (SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team2ID) \
                    FROM Spiel Inner Join KOspiel ON Spiel.SpielID = KOspiel.SpielID \
                    WHERE Spiel.SpielID = ?', [gameid])[0]

# returns Spieldata - tuple: (SpielID, UnterwbID, Unterwbname, Datum, Gewertet)
def getSpieldata(gameid):
    return query_db('SELECT Spiel.SpielID, UnterwbID, (SELECT Name FROM Unterwettbewerb WHERE Unterwettbewerb.UnterwbID = Spiel.UnterwbID), Datum, Gewertet FROM Spiel WHERE SpielID = ?', [gameid])[0]

# returns LigaTeamtabelle - List with tuples: Team, Spiele, Treffer, Kassiert, Diff, G, V, OTS, OTN, Punkte
def getLigaTeamtabelle(unterwb, spieltag):
    return query_db("SELECT (SELECT Name FROM Team WHERE Team.TeamID = t2.TeamID) As Team, \
SUM(CASE WHEN t2.TeamID = t1.TeamID THEN 1 ELSE 0 END) Spiele, \
SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer END) Treffer, \
SUM(CASE WHEN Kassiert IS NULL THEN 0 ELSE Kassiert END) Kassiert, \
SUM(CASE WHEN Treffer IS NULL THEN 0 ELSE Treffer-Kassiert END) AS Differenz, \
SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 1 ELSE 0 END) AS G,\
SUM(CASE WHEN Treffer < 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS V, \
SUM(CASE WHEN Treffer = 6 AND Kassiert = 5 THEN 1 ELSE 0 END) AS OTS, \
SUM(CASE WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS OTN, \
SUM(CASE WHEN Treffer = 6 AND Kassiert < 5 THEN 3 WHEN Treffer = 6 AND Kassiert = 5 THEN 2 WHEN Treffer = 5 AND Kassiert = 6 THEN 1 ELSE 0 END) AS Punkte \
FROM \
(SELECT DISTINCT TeamID FROM Teilgenommen WHERE Teilgenommen.UnterwbID = ?) AS t2 Left Join \
(SELECT Spiel.SpielID, Team1ID TeamID, T1Tref Treffer, T2Tref Kassiert, Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 AND Spiel.UnterwbID = ? AND Spieltag <= ? UNION SELECT Spiel.SpielID, Team2ID TeamID, T2Tref Treffer, T1Tref Kassiert, Spiel.UnterwbID, Spiel.SiegerID, Ligaspiel.Spieltag, Spiel.Gewertet FROM Ligaspiel INNER JOIN Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spiel.SiegerID IS NOT NULL AND Spiel.Gewertet = 1 AND Spiel.UnterwbID = ? AND Spieltag <= ?) AS t1 \
ON t2.TeamID = t1.TeamID \
GROUP BY t2.TeamID \
ORDER BY Punkte DESC, Differenz DESC, Treffer DESC, Team ASC;", [unterwb, unterwb, spieltag, unterwb, spieltag])

#returns Spielertabelle - List with tuples: Nickname, Treffer, Spiele, Diff
def getSpielertabelle(unterwb, spieltag):
    cur = g.db.execute("SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = ls.SpielerID), \
SUM(treffer) AS Treffer, \
COUNT(*) AS Spiele \
FROM (Ligaspieler ls LEFT JOIN Spiel s ON ls.SpielID = s.SpielID) LEFT JOIN Ligaspiel lsp ON lsp.SpielID = s.SpielID \
WHERE s.UnterwbID = ? AND lsp.Spieltag <= ? \
GROUP BY ls.SpielerID ORDER BY treffer DESC, Spiele ASC", [unterwb, spieltag])
    return [dict(name=row[0], treffer=row[1], spiele=row[2], schnitt=round(float(row[1])/row[2], 2)) for row in cur.fetchall()]

def getMaxSpieltag(unterwb):
    return query_db('SELECT MAX(Spieltag) \
                    FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID \
                    WHERE UnterwbID = ?', [unterwb], one=True)

def getCurrentSpieltag(unterwb):
    max = getMaxSpieltag(unterwb)
    while max != 1:
        if query_db('SELECT SiegerID \
FROM Spiel Inner Join Ligaspiel ON Spiel.SpielID = Ligaspiel.SpielID \
WHERE Spieltag = ? AND UnterwbID = ? AND SiegerID not null', [max, unterwb], one=True):
            return max
        max -= max
    return 1

def getLigaplatzierung(unterwb, team):
    i = 1
    for item in getLigaTeamtabelle(unterwb, getCurrentSpieltag(unterwb)):
        if item[0] == team:
            return i
        i += 1
    return 0

# returns Teaminfo - List with tuples: (UnterwbID, Unterwbname, Platzierung, (Spieler,))
def getTeaminfo(team):
    list = []
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE TeamID = (SELECT TeamID FROM Team WHERE name = ?)', [team]):
        unterwbid = row[0]
        unterwbname = row[2]
        if row[1] == 'liga':
            platz = getLigaplatzierung(unterwbid, team)
        else:
            # row[1] == 'ko'
            platz = 'Platzierung fuer KO nicht implementiert'
        spieler = query_db('SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = Teilgenommen.SpielerID) \
                           FROM Teilgenommen \
                           WHERE UnterwbID = ? AND \
                           (SELECT name FROM Team WHERE Team.TeamID = Teilgenommen.TeamID) = ?', [unterwbid, team])
        platzierung = (unterwbid, unterwbname, platz, spieler)
        list.append(platzierung)
    return list

# returns Spielerinfo - List with tuples: (UnterwbID, Unterwbname, Platzierung, Team)
def getSpielerinfo(spieler):
    list=[]
    for row in query_db('SELECT DISTINCT uwb.UnterwbID, Modus, uwb.Name, (SELECT Name FROM Team WHERE Team.TeamID = tg.TeamID) \
                        FROM Teilgenommen tg Inner Join Unterwettbewerb uwb ON tg.UnterwbID = uwb.UnterwbID \
                        WHERE SpielerID = (SELECT SpielerID FROM Spieler WHERE nickname = ?)', [spieler]):
        unterwbid = row[0]
        unterwbname = row[2]
        team = row[3]
        if row[1] == 'liga':
            platz = getLigaplatzierung(unterwbid, team)
        else:
            # row[1] == 'ko'
            platz = 'Platzierung fuer KO nicht implementiert'
        platzierung = (unterwbid, unterwbname, platz, team)
        list.append(platzierung)
    return list

def getPassword(nickname):
    return query_db("SELECT Passwort FROM Spieler WHERE Nickname = ?", [nickname], one=True)

def setPassword(nickname, password):
    g.db.execute("UPDATE Spieler SET Passwort = ? WHERE Nickname = ?", [password, nickname])
    g.db.commit()
    return