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

#returns Ligaspiele: SpielID, Erg1, Team1, T1Tref, T2Tref, T2, Erg2
def getLigaSpiele(unterwb, spieltag):
    return query_db("SELECT Spiel.SpielID, \
 (SELECT CASE WHEN T1Tref = 6 THEN CASE WHEN T2Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T1Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg1, \
(SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID) AS T1, \
T1Tref, T2Tref, \
(SELECT Name From Team WHERE Team.TeamID = Spiel.Team2ID) AS T2, \
(SELECT CASE WHEN T2Tref = 6 THEN CASE WHEN T1Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T2Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg2 \
FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spieltag = ? AND UnterwbID = ? ", [spieltag, unterwb])

#returns LigaTeamtabelle: Team, Spiele, Treffer, Kassiert, Diff, G, V, OTS, OTN, Punkte
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

#returns Spielertabelle: Nickname, Treffer, Spiele, Diff
def getSpielertabelle(unterwb, spieltag):
    cur = g.db.execute("SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = ls.SpielerID), \
SUM(treffer) AS Treffer, \
COUNT(*) AS Spiele \
FROM (Ligaspieler ls LEFT JOIN Spiel s ON ls.SpielID = s.SpielID) LEFT JOIN Ligaspiel lsp ON lsp.SpielID = s.SpielID \
WHERE s.UnterwbID = ? AND lsp.Spieltag <= ? \
GROUP BY ls.SpielerID ORDER BY treffer DESC, Spiele ASC", [unterwb, spieltag])
    return [dict(name=row[0], treffer=row[1], spiele=row[2], schnitt=round(float(row[1])/row[2], 2)) for row in cur.fetchall()]



def getPassword(nickname):
    return query_db("SELECT Passwort FROM Spieler WHERE Nickname = ?", [nickname], one=True)

def setPassword(nickname, password):
    g.db.execute("UPDATE Spieler SET Passwort = ? WHERE Nickname = ?", [password, nickname])
    g.db.commit()
    return
