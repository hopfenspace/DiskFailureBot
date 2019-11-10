#!/bin/bash

function getDiskStatus
{
	status=$(/opt/hp/hpssacli/bld/hpssacli ctrl slot=0 pd all show | grep physicaldrive)

    # you may need to change the amount of disks
	for i in $(seq 1 8); do
		curr=$(echo "$status" | grep "I:1:$i" | grep -Eo '(OK)|(Failed)')

		if [ "$curr" == "OK" ]; then
			echo "$i:0"
		else
			echo "$i:1"
		fi
	done
}

# you may need to change host/port of DiskFailureBot
getDiskStatus | openssl s_client \
	-CAfile diskfailurebot.pem -cert client-cert.pem -key client-key.pem \
	-connect "localhost:1337"
