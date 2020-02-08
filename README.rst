==================
nethserver-hotsync
==================

What is it ?
============

HotSync aims to reduce downtime in case of failure, syncing your NethServer with another one, that will be manually activated in case of master server failure.

Normally, when a hardware damage occurs, the time needed to restore service is:

* fix or buy another server: from 4h to 2 days
* install the OS: 30 minutes
* restore backup: from 10 minutes to 8 hours

In summary, users are able to start working again with data from the night before failure after a few hours/days. Using HotSync, time 1 and 3 are 0, 2 is 5 minutes (time to activate spare server). Users are able to start working again in few minutes, using data from a few minutes before the crash.

By default all data included in backup are synchronized every 15 minutes. MariaDB databases are synchronized too, unless databases synchronization isn’t disabled. Applications that use PostgreSQL are synchronized (Mattermost, Webtop5) unless databases synchronization isn’t disabled.

Requirements
============

Two server machines are needed:

* MASTER: active server on production
* SLAVE: warm backup server

For a correct restore, it’s suggested to configure HotSync on two identical servers or two servers with same network cards number, name and position. If the master and slave servers differ, the restore procedure may behave unexpectedly (see Troubleshooting section on NethServer docs).

How it works
============

**MASTER** machine is the currently production server and it makes a backup in the **SLAVE** machine every *"n"* minutes. When a crash occurs on the master, slave becomes active taking the same IP address of the master. Doing so the downtime is minimal, only the time to launch some commands on the SLAVE.

Installation
============

On both MASTER and SLAVE, install nethserver-hotsync: ::

    # yum install nethserver-hotsync --enablerepo=nethforge

Configuration
=============

MASTER configuration: ::

    [root@master]# config setprop rsyncd password <PASSWORD>
    [root@master]# config setprop hotsync role master
    [root@master]# config setprop hotsync SlaveHost <SLAVE_IP>
    [root@master]# signal-event nethserver-hotsync-save

SLAVE configuration: ::

    [root@slave]# config setprop rsyncd password <PASSWORD>
    [root@slave]# config setprop hotsync role slave
    [root@slave]# config setprop hotsync MasterHost <MASTER_IP>
    [root@slave]# signal-event nethserver-hotsync-save

**The <PASSWORD> must be the same on both master and slave.**

If *MySQL* or *PostgreSQL* are installed, they will be synchronized by default. To disable databases synchronization: ::

    [root@master]# config setprop hotsync databases disabled
    [root@master]# signal-event nethserver-hotsync-save

You can update these settings also from Cockpit interface.

How to restore
==============

The following procedure puts the SLAVE in production when the master has crashed.

1. switch off MASTER
2. if the SLAVE machine must run as network gateway, connect it to the router/modem with a network cable
3. following command changes the IP address and cuts off the network connection. If you are connected through an ssh console, launch the ``screen`` command ::

    [root@slave]# screen

4. on SLAVE launch command, and read carefully its output ::

    [root@slave]# hotsync-promote
   
   If no Internet connection is detected (e.g. you are restoring a firewall on a machine that was passing through crashed master for Internet connection), the scripts will purpose you some options:

    1. Restore master network configuration (IMPORTANT: use this option only if two servers are identical - NIC number, names and positions must be identical)
    2. Fix network configuration from Cockpit GUI (when restoring on different hardware)
    3. Continue without internet: assign correct roles before proceed with this option. Some events could fails (not recommended)

5. If necessary go to Server Manager or Cockpit GUI, in page Network and reassign roles to network interfaces as master one. Remember also to recreate bridge if you have configured DC. In case of DC errors consult troubleshooting section before proceed with network restore.
6. launch command ::

    [root@slave]# /sbin/e-smith/signal-event post-restore-data

7. if an USB backup is configured on MASTER, connect the backup HD to SLAVE

How to restore original server
==============================

To put again in production original crashed server:

1. configure it as SLAVE
2. synchronize it
3. switch off current MASTER
4. from bash execute: ::

       # hotsync-slave

5. restore configuration backup following above instructions


How to synchronize custom paths
===============================

It is possible to customize HotSync adding all kind of data through the use of **plugins**. The directory of plugins is `/etc/hotsync.d`. Executable files in this directory, are executed before the synchronization.

`INCLUDE_FILE` and `EXCLUDE_FILE` are the files that contain the list of paths to include and to exclude to/from HotSync. Those two variables are passed as arguments to the scripts of this directory when they are executed.

If you want to add files to the synchronization, append them to the INCLUDE_FILE. Append them to EXCLUDE_FILE to remove from the synchronization.

How to force synchronization from MASTER to SLAVE
=================================================

From MASTER bash launch the command: ::

    # hotsync

How to force packages installation on SLAVE
===========================================

*"hotsync-slave"* script extracts from MASTER configuration backup the
list of packages to install and install them. You can force the operation
executing bash command: ::

    # hotsync-slave

Components
==========

hotsync
-------

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
-------------

Automatically executed on SLAVE every 60 minutes, extracts from MASTER
configuration backup the list of packages to install and install them.

Supported packages
==================

* nethserver-antivirus
* nethserver-backup-config
* nethserver-backup-data
* nethserver-base
* nethserver-c-icap
* nethserver-cockpit
* nethserver-collectd
* nethserver-cups
* nethserver-dante
* nethserver-dc
* nethserver-dedalo
* nethserver-directory
* nethserver-dnsmasq
* nethserver-duc
* nethserver-ejabberd
* nethserver-evebox
* nethserver-fail2ban
* nethserver-firewall-base
* nethserver-freepbx > 14.0.3
* nethserver-httpd
* nethserver-hylafax
* nethserver-iaxmodem
* nethserver-ipsec-tunnels
* nethserver-janus
* nethserver-letsencrypt
* nethserver-lightsquid
* nethserver-mail
* nethserver-mattermost
* nethserver-mysql
* nethserver-ndpi
* nethserver-netdata
* nethserver-nextcloud
* nethserver-ntopng
* nethserver-nut
* nethserver-openssh
* nethserver-openvpn
* nethserver-pulledpork
* nethserver-restore-data
* nethserver-roundcubemail
* nethserver-samba
* nethserver-samba-audit
* nethserver-squid
* nethserver-squidclamav
* nethserver-squidguard
* nethserver-sssd
* nethserver-subscription
* nethserver-suricata
* nethserver-vpn-ui
* nethserver-vsftpd
* nethserver-webtop5 (z-push state is not synchronized)

Packages nethserver-ntopng and nethserver-evebox are reinstalled without migrating history.

Please read the docs before proceed with restore.
