#!/bin/bash

if [ $# -lt 3 ]; then
    echo "Usage: $0 <rengine_url> <rengine_username> <rengine_password>"
    exit 1
fi

sh ../automation/login.sh $1 $2 $3
running_scans=$(curl -k -b cookiejar -s $1/api/listScanHistory/ | jq '.scan_histories[] | .scan_status' | grep -e "^1$")
echo $running_scans
[[ $running_scans != "" ]] && echo "Scans are still running" && exit -1

pending_scans=$(curl -k -b cookiejar -s $1/api/listScanHistory/ | jq '.scan_histories[] | .scan_status' | grep -e "^-1$")
echo $pending_scans
[[ $pending_scans != "" ]] && echo "Scans are still pending" && exit -1

cd ..
out=$(git pull)
[[ $out == "Already up to date." ]] && echo $out && exit -2
echo "New code pulled from github"

sudo docker-compose down && sudo docker-compose up -d --build