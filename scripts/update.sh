#!/bin/bash

if [ $# -lt 4 ]; then
    echo "Usage: $0 <rengine_url> <rengine_username> <rengine_password> <dev|prod>"
    exit 1
fi

set -x

bash ./automation/login.sh $1 $2 $3 && \
running_scans=$(curl -k -b cookiejar -s $1/api/listScanHistory/ | jq '.scan_histories[] | .scan_status' | grep -e "^1$") && \
echo $running_scans && \
[[ $running_scans != "" ]] && echo "Scans are still running" && exit -1

pending_scans=$(curl -k -b cookiejar -s $1/api/listScanHistory/ | jq '.scan_histories[] | .scan_status' | grep -e "^-1$") && \
echo $pending_scans && \
[[ $pending_scans != "" ]] && echo "Scans are still pending" && exit -1

git config --global --add safe.directory $(pwd)
git stash
out=$(git pull)
git stash apply
[[ ! $? -eq 0 ]] && exit -1
echo $out && \
[[ $out == "Already up to date." ]] && exit -1
echo "New code pulled from github"

[[ $4 == "dev" ]] && f=docker-compose.dev.yml
[[ $4 == "prod" ]] && f=docker-compose.yml
docker-compose -f $f down
docker-compose -f $f up -d --build
