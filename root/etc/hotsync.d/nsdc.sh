#!/bin/bash

#
# Copyright (C) 2018 Nethesis S.r.l.
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


# copy nsdc machine
if rpm -q --quiet nethserver-dc; then
    # check nsdc machine directory exists
    if [[ -d "/var/lib/machines/nsdc" ]]; then
        echo "/var/lib/machines/nsdc" >> ${INCLUDE_FILE}
    fi
    # check if nsdc is enabled
    if [[ -d "/etc/systemd/system/machines.target.wants" ]]; then
        echo "/etc/systemd/system/machines.target.wants" >> ${INCLUDE_FILE}
    fi
fi
