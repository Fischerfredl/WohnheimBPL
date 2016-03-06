from app import g

def getSpieler():
    cur = g.db.execute("select SpielerID, Nickname, Vorname, Name from Spieler")
    return [dict(ID=row[0], Nickname=row[1], Vorname=row[2], Nachname=row[3]) for row in cur.fetchall()]

def getTeams():
    cur = g.db.execute("select TeamID, Name from Team")
    return [dict(ID=row[0], Name=row[1]) for row in cur.fetchall()]

def getSpieltag(unterwb, spieltag):
    cur = g.db.execute(" \
 SELECT (SELECT CASE WHEN T1Tref = 6 THEN CASE WHEN T2Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T1Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg1, \
(SELECT Name FROM Team WHERE Team.TeamID = Spiel.Team1ID) AS T1, \
T1Tref, T2Tref, \
(SELECT Name From Team WHERE Team.TeamID = Spiel.Team2ID) AS T2, \
(SELECT CASE WHEN T2Tref = 6 THEN CASE WHEN T1Tref = 5 THEN 'OTS' ELSE 'G' END ELSE CASE WHEN T2Tref = 5 THEN 'OTN' ELSE 'V' END END) AS Erg2 \
FROM Ligaspiel Inner Join Spiel ON Ligaspiel.SpielID = Spiel.SpielID WHERE Spieltag = ? AND UnterwbID = ? ", [spieltag, unterwb])
    return [dict(Erg1=row[0], T1=row[1], T1tref=row[2], T2tref=row[3], T2=row[4], Erg2=row[5]) for row in cur.fetchall()]

def getTeamtabelle(unterwb, spieltag):
    cur = g.db.execute("SELECT (SELECT Name FROM Team WHERE Team.TeamID = t2.TeamID) As Team, \
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
    return [dict(team=row[0], spiele=row[1], treffer=row[2], kassiert=row[3], diff=row[4], g=row[5], v=row[6], ots=row[7], otn=row[8], punkte=row[9])for row in cur.fetchall()]

def getSpielertabelle(unterwb, spieltag):
    cur = g.db.execute("SELECT (SELECT Nickname FROM Spieler WHERE Spieler.SpielerID = ls.SpielerID), \
SUM(treffer) AS Treffer, \
COUNT(*) AS Spiele \
FROM (Ligaspieler ls LEFT JOIN Spiel s ON ls.SpielID = s.SpielID) LEFT JOIN Ligaspiel lsp ON lsp.SpielID = s.SpielID \
WHERE s.UnterwbID = ? AND lsp.Spieltag <= ? \
GROUP BY ls.SpielerID ORDER BY treffer DESC, Spiele ASC", [unterwb, spieltag])
    return [dict(name=row[0], treffer=row[1], spiele=row[2], schnitt=round(float(row[1])/row[2], 2)) for row in cur.fetchall()]

def getPassword(nickname):
    return g.db.execute("SELECT Passwort FROM Spieler WHERE Nickname = ?", [nickname])