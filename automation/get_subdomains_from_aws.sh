#!/usr/bin/bash
echo $#
aws route53 list-hosted-zones | jq '.HostedZones[].Id' | tr -d '"' | cut -d '/' -f3 >zones.lst
rm subdomains.txt
rm tmp
while read line; do
	echo "[+] getting zone id $line" &&
		aws route53 list-resource-record-sets --hosted-zone-id $line |
		jq '.ResourceRecordSets[] | if (.Type=="A") then .Name else empty end' |
			tr -d '"' | sed 's/\.$//g' >>tmp
done <zones.lst

[[ $# > 0 ]] && cat tmp | grep $(echo $1 | sed 's/\./\\./g') >>subdomains.txt
[[ $# = 0 ]] && mv tmp subdomains.txt
