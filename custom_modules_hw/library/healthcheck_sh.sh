#!/bin/bash
# WANT_JSON

addr=$(cat $1 | grep -Po '(?<="addr": ")(.*?)(?=")')
tls=$(cat $1 | grep -Po '(?<="tls": )(.*?)(?=,)')
#sleep 300

if $tls ; then
    result_string=$(curl -o /dev/null -s -w "%{http_code}\n" https://$addr -k)
else
    result_string=$(curl -o /dev/null -s -w "%{http_code}\n" http://$addr)
fi

if [ "$result_string" = "200" ]; then
    echo "{\"result_str\": \"$result_string\", \"msg\": \"Status checked successfully\"}"
else
    echo "{\"failed\": true,\"result_str\": \"$result_string\", \"msg\": \"The check was executed with an error\"}"
fi


