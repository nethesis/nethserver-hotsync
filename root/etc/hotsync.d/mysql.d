#!/bin/bash

# source configuration file
[ -f /etc/hotsync.conf ] && source /etc/hotsync.conf

INCLUDE_FILE=$1
EXCLUDE_FILE=$2

#mysql hotsync
if rpm -q --quiet nethserver-mysql; then
    if rpm -q --quiet nethserver-mysql; then
        if [[ $DATABASES != 'disabled' ]]; then
	     # dump mysql tables
             /etc/e-smith/events/actions/mysql-dump-tables
	     #include mysql password file
	     echo "/etc/my.pwd" >> ${INCLUDE_FILE}
	     #include mysql backup
             echo "/var/lib/nethserver/backup/mysql/" >> ${INCLUDE_FILE}
        fi
    fi
fi

