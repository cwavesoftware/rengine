#!/bin/bash

while read -r domain
do
  lookup=$(nslookup $domain); r=$?
  #echo $lookup
  #echo $r
  [[ $r -eq 0 ]] && [[ $(echo $lookup | grep -i 'no answer') == "" ]] && echo $domain
done < $1
