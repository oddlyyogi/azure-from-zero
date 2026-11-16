#!/usr/bin/env bash
# rg-report.sh: every resource group with its region and resource count
set -euo pipefail
printf "%-28s %-16s %s\n" "GROUP" "REGION" "RESOURCES"
az group list --query '[].[name, location]' -o tsv |
while read -r name region; do
  count=$(az resource list -g "$name" --query "length(@)" -o tsv)
  printf "%-28s %-16s %s\n" "$name" "$region" "$count"
done
