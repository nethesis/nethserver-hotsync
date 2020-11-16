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

# sync cron files

if [[ -d "/etc/cron.hourly" ]]; then
  echo "/etc/cron.hourly" >> ${INCLUDE_FILE}
fi

if [[ -d "/etc/cron.daily" ]]; then
  echo "/etc/cron.daily" >> ${INCLUDE_FILE}
fi

if [[ -d "/etc/cron.weekly" ]]; then
  echo "/etc/cron.weekly" >> ${INCLUDE_FILE}
fi

if [[ -d "/etc/cron.monthly" ]]; then
  echo "/etc/cron.monthly" >> ${INCLUDE_FILE}
fi
