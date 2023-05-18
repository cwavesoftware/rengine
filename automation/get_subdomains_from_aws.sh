#!/usr/bin/bash

aws route53 list-hosted-zones | jq '.HostedZones[].Id' | tr -d '"' | cut -d '/' -f3 > zones.lst
rm subdomains.txt
while read line; do echo "[+] getting zone id $line" && aws route53 list-resource-record-sets --hosted-zone-id $line | jq '.ResourceRecordSets[] | if (.Type=="A") then .Name else empty end' | grep $(echo $1 | sed 's/\./\\./g') | tr -d '"' | sed 's/\.$//g' >> subdomains.txt; done < zones.lst
