#!/bin/bash

# source configuration file
[ -f /etc/hotsync.conf ] && source /etc/hotsync.conf

INCLUDE_FILE=$1
EXCLUDE_FILE=$2


# check that nethserver-webtop5 RPM is installed
if rpm -q --quiet nethserver-webtop5; then
    # check if postgresql rsync is enabled
    if [[ $DATABASES != 'disabled' ]]; then
        /usr/bin/su - postgres -c "pg_dump webtop5 > /var/lib/nethserver/webtop/backup/webtop.sql"
        echo "/var/lib/nethserver/webtop/backup/webtop.sql" >> ${INCLUDE_FILE}
    fi
fi
