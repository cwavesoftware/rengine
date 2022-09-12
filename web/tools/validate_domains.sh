#!/bin/bash

while read -r domain
do
  nslookup $domain 1>/dev/null 2>&1 && [[ $(nslookup $domain | grep 'canonical name') == "" ]] && echo $domain
done < $1
