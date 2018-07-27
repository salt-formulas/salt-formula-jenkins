#!/bin/bash

: "${JENKINS_URL:=http://localhost:8080}"
: "${WAIT_TIME:=300}"
: "${INTERVAL:=5}"

while [ $((WAIT_TIME -= INTERVAL)) -ge 0 ]; do
    if curl -fs -o /dev/null "$JENKINS_URL"; then
        STATUS=0
        break
    fi
    sleep $INTERVAL
done

exit ${STATUS:-124}
