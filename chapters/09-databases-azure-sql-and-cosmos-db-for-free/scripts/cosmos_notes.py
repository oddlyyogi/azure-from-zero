"""Write, read and query Photo Notes in Cosmos DB over REST with an Entra ID token."""
import datetime
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

account, db, coll = sys.argv[1:4]
base = f"https://{account}.documents.azure.com"
token = subprocess.run(["az", "account", "get-access-token", "--resource", base,
                        "--query", "accessToken", "-o", "tsv"],
                       capture_output=True, text=True, check=True).stdout.strip()


def call(method, path, body=None, **extra):
    auth = urllib.parse.quote(f"type=aad&ver=1.0&sig={token}", safe="")
    now = datetime.datetime.now(datetime.UTC).strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers = {"Authorization": auth, "x-ms-version": "2018-12-31",
               "Content-Type": "application/json", "x-ms-date": now}
    headers.update(extra)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{base}/{path}", data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read() or b"{}"
            charge = resp.headers["x-ms-request-charge"]
            return resp.status, charge, json.loads(raw)
    except urllib.error.HTTPError as err:
        return err.code, err.headers.get("x-ms-request-charge"), json.load(err)


docs = f"dbs/{db}/colls/{coll}/docs"
notes = [("ana", "n1", "Harbour"), ("ana", "n2", "Market"), ("ben", "n3", "Beach")]
for user, nid, title in notes:
    status, ru, _ = call("POST", docs, {"id": nid, "userId": user, "title": title},
                         **{"x-ms-documentdb-partitionkey": json.dumps([user])})
    print("write", nid, status, ru, "RU")
status, ru, item = call("GET", f"{docs}/n1", **{"x-ms-documentdb-partitionkey": '["ana"]'})
print("point read", item["title"], status, ru, "RU")
status, ru, _ = call("GET", f"{docs}/n9", **{"x-ms-documentdb-partitionkey": '["ana"]'})
print("missing read", status, ru, "RU")
query = {"query": "SELECT c.title FROM c WHERE c.userId = 'ana'"}
status, ru, res = call("POST", docs, query, **{"x-ms-documentdb-isquery": "true",
                       "Content-Type": "application/query+json",
                       "x-ms-documentdb-partitionkey": '["ana"]'})
print("query one user", [d["title"] for d in res["Documents"]], status, ru, "RU")
status, ru, err = call("POST", docs, {"id": "n1", "userId": "ana", "title": "Again"},
                      **{"x-ms-documentdb-partitionkey": '["ana"]'})
print("duplicate id", status, err.get("code"))
everyone = {"query": "SELECT c.userId, c.title FROM c"}
status, ru, res = call("POST", docs, everyone, **{
    "x-ms-documentdb-isquery": "true", "Content-Type": "application/query+json",
    "x-ms-documentdb-query-enablecrosspartition": "true"})
print("query all users", len(res["Documents"]), status, ru, "RU")
status, ru, _ = call("PUT", f"{docs}/n2", {"id": "n2", "userId": "ana",
                     "title": "Market, figs"},
                     **{"x-ms-documentdb-partitionkey": '["ana"]'})
print("replace n2", status, ru, "RU")
status, ru, _ = call("DELETE", f"{docs}/n3",
                     **{"x-ms-documentdb-partitionkey": '["ben"]'})
print("delete n3", status, ru, "RU")
