#!/usr/bin/env bash
# kql.sh WORKSPACE QUERY: run a KQL query in a Log Analytics workspace (no extension)
set -euo pipefail
ws=$(az monitor log-analytics workspace show -g "$G" -n "$1" --query customerId -o tsv)
body=$(python3 -c 'import json,sys; print(json.dumps({"query": sys.argv[1]}))' "$2")
az rest --method post --resource https://api.loganalytics.io \
  --url "https://api.loganalytics.io/v1/workspaces/$ws/query" --body "$body" \
  --query "tables[0].rows" -o tsv
