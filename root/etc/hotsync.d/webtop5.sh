#!/bin/bash

#
# Copyright (C) 2017 Nethesis S.r.l.
# http://www.nethesis.it - nethserver@nethesis.it
#
# This script is part of NethServer.
#
# NethServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or any later version.
#
# NethServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NethServer.  If not, see COPYING.
#

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
