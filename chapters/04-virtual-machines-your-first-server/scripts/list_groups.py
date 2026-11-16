"""List resource groups by calling Azure Resource Manager directly."""
import json
import subprocess
import urllib.request

token = subprocess.run(
    ["az", "account", "get-access-token", "--query", "accessToken", "-o", "tsv"],
    capture_output=True, text=True, check=True).stdout.strip()
sub = subprocess.run(["az", "account", "show", "--query", "id", "-o", "tsv"],
                     capture_output=True, text=True, check=True).stdout.strip()

url = f"https://management.azure.com/subscriptions/{sub}/resourcegroups?api-version=2021-04-01"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
with urllib.request.urlopen(req) as resp:
    for group in json.load(resp)["value"]:
        print(group["name"], group["location"])
