#!/bin/bash

wait_for_http() {
    local url="$1"
    local max_seconds=1000
    local end_time=$(( $(date +%s) + max_seconds ))
    local success='false'
    echo "Waiting for $url"
    while [ "$(date +%s)" -lt "$end_time" ]; do  # Loop until interval has elapsed.
        sleep 2
        if [ "$(curl -s -o /dev/null -L -w '%{http_code}' "$url")" == "200" ]; then
            success='true'
            break
        fi
    done
    if [ "$success" = 'true' ]; then
        exit 0
    else
        exit 1
    fi
}

wait_for_http "${1:-http://localhost/api/v2/}"