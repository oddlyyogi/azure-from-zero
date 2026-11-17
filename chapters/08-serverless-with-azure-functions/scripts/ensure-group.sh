#!/usr/bin/env bash
# ensure-group.sh NAME [REGION]: create the resource group only if it does not exist
set -euo pipefail
name=$1
region=${2:-swedencentral}
if [ "$(az group exists --name "$name")" = "true" ]; then
  echo "$name already exists"
  exit 0
fi
az group create --name "$name" --location "$region" --tags project=photo-notes -o none
echo "$name created in $region"
