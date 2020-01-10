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

#mysql hotsync
if rpm -q --quiet nethserver-mysql; then
    if [[ $DATABASES != 'disabled' ]]; then
        # dump mysql tables
        /etc/e-smith/events/actions/mysql-dump-tables
        # include mysql backup
        echo "/var/lib/nethserver/backup/mysql/" >> ${INCLUDE_FILE}
        # copy mysql tables to allow correct applications restore
        echo "/var/lib/mysql/mysql/" >> ${INCLUDE_FILE}
        # copy mysql secret to avoid errors before restore
        echo "/var/lib/nethserver/secrets/mysql" >> ${INCLUDE_FILE}
    fi
fi

