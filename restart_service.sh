#!/bin/bash

if test `find /tmp/teleinfo.error -mmin +5`
then
	echo "Restart teleinfo service"
	service teleinfo restart
fi
