#!/bin/bash

#
# Copyright (C) 2020 Nethesis S.r.l.
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

# freepbx hotsync
if rpm -q --quiet nethserver-freepbx; then
    # include freepbx conf and interface
    echo "/var/lib/asterisk/" >> ${INCLUDE_FILE}
    echo "/var/www/html/freepbx/" >> ${INCLUDE_FILE}
    echo "/etc/amportal.conf" >> ${INCLUDE_FILE}
    echo "/etc/asterisk/manager.conf" >> ${INCLUDE_FILE}
    echo "/etc/freepbx.conf" >> ${INCLUDE_FILE}
    echo "/usr/sbin/fwconsole" >> ${INCLUDE_FILE}
    
    # remove excluded freepbx files
    sed -i 's#/var/www/html/freepbx/##g' ${EXCLUDE_FILE}
    sed -i 's#/var/www/html/freepbx##g' ${EXCLUDE_FILE}
    
    # remove asterisk db from default exclusions: we need a first restore to avoid errors
    sed -i 's#/var/lib/nethserver/backup/mysql/asterisk.dump##g' ${EXCLUDE_FILE}
    
    # show alert if databases sync is disabled
    if [[ $DATABASES != 'enabled' ]]; then
        echo "[WARNING] Databases sync is disabled: asterisk may not work properly after promote. Please enable it."
    fi  
fi
