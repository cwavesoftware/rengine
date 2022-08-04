#!/bin/bash

if [ $# -lt 6 ]; then
    echo "Usage: $0 <rengine_url> <target_domain> <rengine_username> <rengine_password> <scan_engine> <included_subdomains_file> [--wait]"
    exit 1
fi

bash login.sh $1 $3 $4L

targets=""
get_targets () {
    targets=$(curl -s -b cookiejar "$1/api/queryTargets/" --insecure)
}

get_target_id () {
    target_id=$(echo $targets | jq ".domains[] | if (.name == \"$1\") then .id else empty end")
}

get_engine_id () {
    echo "INFO: Looking for engine $2"
    engine_id=$(curl -s -b cookiejar "$1/api/listEngines/" --insecure | jq ".engines[] | if (.engine_name==\"$2\") then .id else empty end")
}

trigger () {
    echo "INFO: Getting CSRF token ..."
    csrf=$(curl -s $1/scan/start/$2 -b cookiejar -c cookiejar --insecure | sed -n "s/^.*name=\"csrfmiddlewaretoken\" value=\"\(.*\)\".*$/\1/p")
    # echo "csrf=$csrf"

    echo "INFO: Triggering scan ..."
    included_subdomains_file=$4
    touch $included_subdomains_file && \
    curl -s $1/scan/start/$2 -b cookiejar --insecure -o /dev/null -d "csrfmiddlewaretoken=$csrf&scan_mode=$3&importSubdomainTextArea=$(cat $included_subdomains_file)&outOfScopeSubdomainTextarea="

}

wait () {
    last_scan_id=$(curl -k -b cookiejar -s $1/api/listScanHistory/ | jq '.scan_histories[0].id')
    last_scan_celery_id=$(curl -k -b cookiejar -s $1/api/listScanHistory/ | jq '.scan_histories[0].celery_id')
    echo "Scan ID = $last_scan_id, Celery ID = $last_scan_celery_id"
    scan_status=-1
    sleepTime=60  # seconds
    while [ ! $scan_status -eq 2 ]
    do
        sleep $sleepTime
        scan_status=$(curl -k -s -b cookiejar $1/api/scan/status/$last_scan_id | jq '.scanStatus')
        echo "Scan status = $scan_status"
        [ $scan_status -eq 0 ] && echo "Scan failed" && exit -1
    done
}

get_targets $1
get_target_id $2
echo "DEBUG: Target ID: $target_id"
if [[ $target_id == "" ]] || [ ! $target_id -eq $target_id ];
   then echo "ERROR: Could not get Target ID" >&2; exit 1 
fi

get_engine_id $1 "$5"
echo "DEBUG: Engine ID: $engine_id"
if [[ $engine_id == "" ]] || [ ! $engine_id -eq $engine_id ];
   then echo "ERROR: Could not get Engine ID" >&2; exit 1 
fi

trigger $1 $target_id $engine_id $6

if [ $7 = "--wait" ]; then
    wait $1
fi
rm cookiejar

echo "INFO: Done"
