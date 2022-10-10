#!/bin/bash

if [ $# -lt 3 ]; then
    echo "Usage: $0 <rengine_url> <rengine_username> <rengine_password>"
    exit 1
fi

echo "INFO: Getting CSRF token ..."
curl -s "$1/login/" -c cookiejar --insecure -o /dev/null && \
csrf=$(cat cookiejar | grep csrftoken | rev | cut -d$'\t' -f1 | rev) && \
echo "DEBUG: csrftoken=$csrf" && \
echo "INFO: Logging in ..." && \
curl -s -d "username=$2&password=$3&csrfmiddlewaretoken=$csrf" "$1/login/" -X POST -b cookiejar -c cookiejar --insecure > /dev/null && \
sessionid=$(cat cookiejar | grep sessionid | rev | cut -d$'\t' -f1 | rev) && \
[[ $sessionid != "" ]] && echo "INFO: Got sessionid" && echo "DEBUG: sessionid = $sessionid" && exit 0
echo "ERROR: Couldn't get sessionid" && exit -1