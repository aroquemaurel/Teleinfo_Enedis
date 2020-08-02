#!/bin/bash

if ! [ -f /tmp/teleinfo.pid ] 
then
	service teleinfo restart
fi

if [ -f /tmp/teleinfo.error ]
then
	if test `find /tmp/teleinfo.error -mmin +5`
	then
		echo "Restart teleinfo service"
		service teleinfo restart
	fi
fi
