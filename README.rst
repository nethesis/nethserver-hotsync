# NethServer HotSync

NethServer hotsync aims to reduce downtime in case of failure.
Normally, when a hardware damage occurs, the time needed to restore service is:

1. Fix/buy another server: from 4h to 2 days
2. Install OS: 30 minutes
3. Restore backup: from 10 minutes to 8 hours

In summary, users are able to start working again with data from the night before failure after a few hours/days.
Using hotsync, time 1 and 3 are 0, 2 is 5 minutes (time to activate spare server). Users are able to start working again in few minutes, using data from a few minutes before the crash.

Terminology:

MASTER is the production system
SLAVE is the spare server

1. SLAVE is switched on, with an IP address different than MASTER
2. every N minutes, MASTER makes a backup on SLAVE
3. An alert is generated in case of error

## How to activate a SLAVE

1. switch off MASTER if it's on
2. from NethGUI, restore configuration backup (data are already synced)

To put again in production original server, configure it as SLAVE, sync it, switch off current MASTER and restore configuration backup.

## hotsync
- is a shell script that is launched by cron every 15 minutes
- uses a lockfile to ensure that only one instance at a time is executed
- creates a list of file to include and exclude from rsync (using backup-data configuration and hotsync own logic)
- launch scripts in /etc/hotsync.d
- launch backup on MASTER
- launch an rsync that copy listed files from MASTER to SLAVE


