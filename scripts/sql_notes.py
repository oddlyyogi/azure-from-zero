"""Create, fill and query the Photo Notes table in Azure SQL with Entra ID sign-in."""
import sys

import mssql_python

server = sys.argv[1]
conn = mssql_python.connect(
    f"Server=tcp:{server}.database.windows.net,1433;Database=photonotes;"
    "Authentication=ActiveDirectoryDefault;Encrypt=yes;")
cur = conn.cursor()
cur.execute("IF OBJECT_ID('dbo.notes') IS NULL CREATE TABLE dbo.notes ("
            "id INT IDENTITY PRIMARY KEY, title NVARCHAR(100) NOT NULL, body NVARCHAR(400))")
for title, body in [("Harbour", "Boats at sunrise"), ("Market", "Fresh figs")]:
    cur.execute("INSERT INTO dbo.notes (title, body) VALUES (?, ?)", (title, body))
conn.commit()
for row in cur.execute("SELECT id, title, body FROM dbo.notes ORDER BY id").fetchall():
    print(tuple(row))
print("signed in as:", cur.execute("SELECT SUSER_SNAME()").fetchone()[0])
size = "SELECT DATABASEPROPERTYEX(DB_NAME(), 'ServiceObjective')"
print("service objective:", cur.execute(size).fetchone()[0])

cur.execute("IF OBJECT_ID('dbo.tags') IS NULL CREATE TABLE dbo.tags ("
            "note_id INT NOT NULL REFERENCES dbo.notes(id), "
            "tag NVARCHAR(30) NOT NULL)")
cur.execute("INSERT INTO dbo.tags (note_id, tag) "
            "SELECT id, 'sea' FROM dbo.notes WHERE title = 'Harbour'")
conn.commit()
rows = cur.execute("SELECT n.title, t.tag FROM dbo.notes AS n "
                   "JOIN dbo.tags AS t ON t.note_id = n.id").fetchall()
print("joined:", [tuple(r) for r in rows])
try:
    cur.execute("INSERT INTO dbo.tags (note_id, tag) VALUES (999, 'ghost')")
except Exception as err:
    print("rejected:", "FOREIGN KEY" in str(err))
conn.close()
