"""Upload one photo to blob storage with an Entra ID token (standard library only)."""
import subprocess
import sys
import urllib.request
from pathlib import Path

account, photo = sys.argv[1], Path(sys.argv[2])
token = subprocess.run(
    ["az", "account", "get-access-token", "--resource", "https://storage.azure.com/",
     "--query", "accessToken", "-o", "tsv"],
    capture_output=True, text=True, check=True).stdout.strip()

req = urllib.request.Request(
    f"https://{account}.blob.core.windows.net/photos/{photo.name}",
    data=photo.read_bytes(), method="PUT",
    headers={"Authorization": f"Bearer {token}", "x-ms-version": "2025-05-05",
             "x-ms-blob-type": "BlockBlob", "Content-Type": "image/png"})
with urllib.request.urlopen(req) as resp:
    print(photo.name, "->", resp.status)
