#!/bin/bash

ping -c4 192.168.0.1 > /dev/null

if [ $? != 0 ] 
then
	date
	if [ -f /root/no_wifi ]
	then
		echo "A reboot has already processed... Try to wait"
		sleep 60
		ping -c2 192.168.0.1 > /dev/null

		if [ $? != 0 ] 
		then 
			echo "Try to ifconfig down / up"
			ifconfig wlan0 down
			sleep 5
			ifconfig wlan0 up
			exit 0
		else
			echo "Waiting is enough ! the network is back"
			rm no_wifi
		fi
	fi

	touch /root/no_wifi
	echo "There is no network access... Try to reboot it"
	reboot
else
	if [ -f /root/no_wifi ]
	then
		date
		echo "The network is back"
		rm no_wifi
	fi
fi

