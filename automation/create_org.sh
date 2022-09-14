#!/bin/bash

if [ ! $# -eq 4 ]; then
    echo "Usage: $0 <rengine_url> <rengine_username> <rengine_password> <org_name>"
    exit 1
fi

bash login.sh $1 $2 $3
[[ ! $? -eq 0 ]] && exit -1

echo "INFO: Getting CSRF token ..."
csrf=$(curl -s $1/target/add/organization -b cookiejar -c cookiejar --insecure | sed -n "s/^.*name=\"csrfmiddlewaretoken\" value=\"\(.*\)\".*$/\1/p")
echo "DEBUG: csrftoken=$csrf"

echo "INFO: Creating organization $4 ..."
res=$(curl --write-out '%{http_code}' -s $1/target/add/organization -b cookiejar --insecure -o /dev/null -d "csrfmiddlewaretoken=$csrf&name=$4&descrption=created via automation from Hackerone")
if [ $res -eq 302 ]; then
    echo "INFO: Creating organization $4: SUCCESS"
else    
    echo "INFO: Creating organization $4: FAIL"
    exit -1
fi
echo "INFO: $0 Done"