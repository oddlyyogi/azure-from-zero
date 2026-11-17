"""Photo Notes functions: a notes API, a photo-jobs worker and a timer."""
import datetime
import json
import logging

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="notes", methods=["GET", "POST"])
@app.table_input(arg_name="rows", table_name="notes", partition_key="notes",
                 connection="AzureWebJobsStorage")
@app.table_output(arg_name="out", table_name="notes", connection="AzureWebJobsStorage")
def notes(req: func.HttpRequest, rows: str, out: func.Out[str]) -> func.HttpResponse:
    if req.method == "POST":
        note = req.get_json()
        key = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d%H%M%S%f")
        out.set(json.dumps({"PartitionKey": "notes", "RowKey": key,
                            "title": note["title"], "body": note["body"]}))
        return func.HttpResponse(status_code=201)
    notes = [{"title": r["title"], "body": r["body"]} for r in json.loads(rows)]
    return func.HttpResponse(json.dumps(notes), mimetype="application/json")


@app.queue_trigger(arg_name="msg", queue_name="photo-jobs", connection="AzureWebJobsStorage")
@app.table_output(arg_name="meta", table_name="photometa", connection="AzureWebJobsStorage")
def photo_job(msg: func.QueueMessage, meta: func.Out[str]) -> None:
    photo = msg.get_body().decode()
    if not photo.endswith(".png"):
        raise ValueError(f"not a photo: {photo}")
    logging.info("photo job for %s", photo)
    meta.set(json.dumps({"PartitionKey": "photos", "RowKey": photo,
                         "processed": datetime.datetime.now(datetime.UTC).isoformat()}))


@app.timer_trigger(arg_name="timer", schedule="0 */5 * * * *")
def heartbeat(timer: func.TimerRequest) -> None:
    logging.info("photo-notes heartbeat, past due: %s", timer.past_due)
