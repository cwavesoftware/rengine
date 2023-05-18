#!/usr/bin/bash

aws route53 list-hosted-zones --profile $1 | jq '.HostedZones[].Id' | tr -d '"' | cut -d '/' -f3 > zones.lst
rm subdomains.txt
while read line; do echo "[+] getting zone id $line" && aws route53 --profile $1 list-resource-record-sets --hosted-zone-id $line | jq '.ResourceRecordSets[] | if (.Type=="A") then .Name else empty end' | grep $2 | tr -d '"' | sed 's/\.$//g' >> subdomains.txt; done < zones.lst
