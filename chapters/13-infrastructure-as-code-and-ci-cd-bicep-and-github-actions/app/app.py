"""Photo Notes: a tiny notes web app, the one-server version."""
import logging
import os
import sqlite3
from html import escape
from pathlib import Path

if os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    from azure.monitor.opentelemetry import configure_azure_monitor
    configure_azure_monitor()
from flask import Flask, redirect, request  # after telemetry starts

DB = Path(os.environ.get("PHOTO_NOTES_DB", Path(__file__).with_name("notes.db")))
app = Flask(__name__)


def db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS notes "
                "(id INTEGER PRIMARY KEY, title TEXT, body TEXT)")
    return con


@app.get("/")
def index():
    rows = db().execute("SELECT title, body FROM notes ORDER BY id DESC").fetchall()
    items = "".join(f"<li><b>{escape(t)}</b> {escape(b)}</li>" for t, b in rows)
    return f"<h1>Photo Notes</h1><ul>{items}</ul>"


@app.post("/notes")
def add_note():
    with db() as con:
        con.execute("INSERT INTO notes (title, body) VALUES (?, ?)",
                    (request.form["title"], request.form["body"]))
    logging.getLogger("photo_notes").warning("note saved: %s", request.form["title"])
    return redirect("/", code=303)


@app.get("/health")
def health():
    count = db().execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    return {"status": "ok", "notes": count}


@app.get("/photos")
def photos():
    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import ContainerClient
    account = os.environ["PHOTOS_ACCOUNT"]
    client = ContainerClient(f"https://{account}.blob.core.windows.net", "photos",
                             credential=DefaultAzureCredential())
    return {"photos": sorted(b.name for b in client.list_blobs())}


@app.get("/version")
def version():
    import socket
    return {"version": os.environ.get("APP_VERSION", "1"),
            "host": socket.gethostname()}


@app.get("/config")
def config():
    token = os.environ.get("PHOTO_SERVICE_TOKEN", "")
    return {"photo_service_token_set": bool(token), "length": len(token)}


@app.get("/boom")
def boom():
    raise RuntimeError("boom: a test failure for monitoring")
