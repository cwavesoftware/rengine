#!/bin/bash

if [ ! $# -eq 5 ]; then
    echo "Usage: $0 <rengine_url> <rengine_username> <rengine_password> <target_name> <h1_handle>"
    exit 1
fi

bash login.sh $1 $2 $3
[[ ! $? -eq 0 ]] && exit -1

echo "INFO: Getting CSRF token ..."
csrf=$(curl -s $1/target/add/target -b cookiejar -c cookiejar --insecure | sed -n "s/^.*name=\"csrfmiddlewaretoken\" value=\"\(.*\)\".*$/\1/p" | head -n 1)
echo "DEBUG: csrftoken=$csrf"

echo "INFO: Creating target $4 ..."
res=$(curl  --write-out '%{http_code}' -s $1/target/add/target -b cookiejar --insecure -o /dev/null -d "csrfmiddlewaretoken=$csrf&name=$4&description=created%20via%20automation%20script&h1_team_handle=$5&add-target=submit")
if [ $res -eq 302 ]; then
    echo "INFO: Creating target $4: SUCCESS"
else    
    echo "INFO: Creating target $4: FAIL"
    exit -1
fi
echo "INFO: $0 Done"