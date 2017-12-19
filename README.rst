============
What is it ?
============

NethServer HotSync aims to reduce downtime in case of failure. Normally, when an hardware damage occurs, the time needed to restore service is:

* fix or buy another server: from 4h to 2 days
* install the OS: 30 minutes
* restore backup: from 10 minutes to 8 hours

In summary, users are able to start working again with data from the night before failure after a few hours or days. Using HotSync, time 1 and 3 become 0 and 2 becomes 5 minutes (time to activate the slave server). Users are able to start working again in few minutes, using data from a few minutes before the crash.

============
Requirements
============

Two server machines are needed:

* MASTER: active server on production
* SLAVE: warm backup server

============
How it works
============

**MASTER** machine is the currently production server and it makes a backup in the **SLAVE** machine every *"n"* minutes. When a crash occurs on the master, slave becomes active taking the same IP address of the master. Doing so the downtime is minimal, only the time to launch some commands on the SLAVE.

============
Installation
============

On both MASTER and SLAVE, install nethserver-hotsync: ::

    # yum install nethserver-hotsync

=============
Configuration
=============

MASTER configuration: ::

    [root@master]# config setprop rsyncd password <PASSWORD>
    [root@master]# config setprop hotsync role master
    [root@master]# config setprop hotsync SlaveHost <SLAVE_IP>
    [root@master]# signal-event nethserver-hotsync-update

SLAVE configuration: ::

    [root@slave]# config setprop rsyncd password <PASSWORD>
    [root@slave]# config setprop hotsync role slave
    [root@slave]# config setprop hotsync MasterHost <MASTER_IP>
    [root@slave]# signal-event nethserver-hotsync-update

**The <PASSWORD> must be the same on both master and slave.**

If *MySQL* or *PostgreSQL* are installed, they will be synchronized by default. To disable databases synchronization: ::

    [root@master]# config setprop hotsync databases disabled
    [root@master]# signal-event nethserver-hotsync-update

==============
How to restore
==============

The following procedure are to put the SLAVE in production when the master has been crashed.

1. switch off MASTER
2. from SLAVE bash execute: ::

       # hotsync-slave

3. from NethGUI go to "Backup (configuration)" and restore the configuration backup (data is already synchronized)
4. manually connect the modem to SLAVE machine
5. connect backup HD to SLAVE
6. connect the router

==============================
How to restore original server
==============================

To put again in production original crashed server:

1. configure it as SLAVE
2. synchronize it
3. switch off current MASTER
4. from bash execute: ::

       # hotsync-slave

5. restore configuration backup

==================
Supported packages
==================

* nethserver-nextcloud
* nethserver-mysql
* nethserver-mattermost
* nethserver-dnsmasq
* nethserver-squidguard
* nethserver-pulledpork
* nethserver-antivirus
* nethserver-samba-audit
* nethserver-freepbx > 14.0.3
* nethserver-webtop5 (z-push state is not synchronized)
* nethserver-collectd: sync /var/lib/collected
* nethserver-cups
* nethserver-dc
* nethserver-letsencrypt
* nethserver-nextcloud
* nethserver-sssd
* nethserver-directory
* nethserver-ibays
* nethserver-mail-server


===============================
How to synchronize custom paths
===============================

It is possible to customize HotSync adding all kind of data through the use of **plugins**. The directory of plugins is `/etc/hotsync.d`. Executable files in this directory, are executed before the synchronization.

`INCLUDE_FILE` and `EXCLUDE_FILE` are the files that contain the list of paths to include and to exclude to/from HotSync. Those two variables are passed as arguments to the scripts of this directory when they are executed.

If you want to add files to the synchronization, append them to the INCLUDE_FILE. Append them to EXCLUDE_FILE to remove from the synchronization.

============================
How to force synchronization
============================

From MASTER bash launch the command: ::

    # hotsync

==========
Components
==========

hotsync
=======

- is a shell script launched by cron every 15 minutes
- uses a lockfile to ensure that only one instance at a time is executed
- uses secure communication with rsync over stunnel
- creates a list of files to be included and another one to be excluded from rsync (using backup-data configuration and hotsync own logic)
- launch backup on MASTER
- launch an rsync that copy listed files from MASTER to SLAVE in a secure manner using stunnel
- if something fails, root is notified with an email
- you can check files that will be copied on the next synchronization using the command: ::
      
      hotsync --dry-run


hotsync-slave
=============

Executed on SLAVE, extracts from MASTER configuration backup the list of packages to install and install them.
