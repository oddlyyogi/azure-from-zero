"""Photo Notes API for Static Web Apps: a health check and a greeting from app settings."""
import datetime
import json
import os

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="health")
def health(req: func.HttpRequest) -> func.HttpResponse:
    now = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")
    body = {"status": "ok", "time": now}
    return func.HttpResponse(json.dumps(body), mimetype="application/json")


@app.route(route="hello")
def hello(req: func.HttpRequest) -> func.HttpResponse:
    greeting = os.environ.get("GREETING", "Hello")
    name = req.params.get("name", "visitor")
    return func.HttpResponse(f"{greeting}, {name}!")
