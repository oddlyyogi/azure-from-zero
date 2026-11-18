#!/usr/bin/env bash
# price.sh FILTER [REGION]: retail prices from the public Azure Retail Prices API
set -euo pipefail
region=${2-swedencentral}
filter=$(printf "%s" "armRegionName eq '$region' and $1" | sed 's/ /%20/g')
url="https://prices.azure.com/api/retail/prices?\$filter=$filter"
curl -s --retry 5 --retry-all-errors -f "$url" |
  python3 -c 'import json,sys
for i in json.load(sys.stdin)["Items"]:
    print(i["productName"], "|", i["meterName"], "|", i["retailPrice"], i["unitOfMeasure"])'
