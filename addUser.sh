#!/bin/bash
add(){
	useradd $1 -g users -d /ome/$1
	pd = $(cat /dev/urandom |tr -dc 0-9-A-Z-a-z-|head -c ${1:-10})
	echo $pd
	echo $pd | passwd $1 --stdin 
	chown $1 /home/$1 -R
	chgrp users /home/$1 -R

	if [[ -n $2 ]]
	then
    dingTalkSendMsg.py $2 "Your account at $HOSTNAME has been created. Passwd: $pd"
	fi
}

add $1 $2 # $1 is the username $2 is the DingTalk account name. If you don't want inform the account owner please leave the $2 blank.
