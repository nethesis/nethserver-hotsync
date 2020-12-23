Summary: NethServer Hotsync 
Name: nethserver-hotsync
Version: 2.2.1
Release: 1%{?dist}
License: GPLv3
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-cockpit.tar.gz
BuildArch: noarch
Requires: nethserver-base nethserver-backup-config rsync stunnel nethserver-backup-data
URL: %{url_prefix}/%{name}
BuildRequires: nethserver-devtools

%description
NethServer Hotsync is a tool that simplifies configuration of rsync to keep two NethServer up to date

%pre
# ensure srvmgr user exists:
if ! id srvmgr >/dev/null 2>&1 ; then
   useradd -r -U -G adm srvmgr
fi

%prep
%setup -q

%build
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist


%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc README.rst
%attr(0440,root,root) /etc/sudoers.d/50_nsapi_nethserver_hotsync


%changelog
* Sat Dec 05 2020 Federico Ballarini <fed.ballarini@gmail.com> - 2.2.1-1
- HotSync: ufdbGuard error while fixing permissions - Bug NethServer/dev#6355

* Thu Nov 26 2020 Federico Ballarini <fed.ballarini@gmail.com> - 2.2.0-1
- HotSync: cron sync and avoid execution on slave host - Bug NethServer/dev#6328
- HotSync: permissions are not fixed after master sync - Bug NethServer/dev#6335

* Sat Feb 8 2020 Federico Ballarini <fed.ballarini@gmail.com> - 2.1.4-1
- HotSync: hide rsyncd password field - NethServer/dev#6054
- HotSync: getmail status is not synced - Bug NethServer/dev#6055

* Sun Jan 12 2020 Federico Ballarini <fed.ballarini@gmail.com> - 2.1.3-1
- HotSync: add logs view - NethServer/dev#6027
- Avoid to restore nextcloud twice

* Sun Jan 12 2020 Federico Ballarini <fed.ballarini@gmail.com> - 2.1.2-1
- HotSync: suricata permissions are not set properly - Bug NethServer/dev#6024
- HotSync: nextcloud is not restored properly - Bug NethServer/dev#6025
- HotSync: avoid cron execution - Bug NethServer/dev#6026

* Fri Jan 10 2020 Federico Ballarini <fed.ballarini@gmail.com> - 2.1.1-1
- HotSync: missing db and files cause errors - Bug NethServer/dev#6010

* Wed Jan 08 2020 Federico Ballarini <fed.ballarini@gmail.com> - 2.1.0-1
- Cockpit: add HotSync interface - NethServer/dev#5996
- HotSync: freepbx is not restored properly - Bug NethServer/dev#6008
- HotSync: permissions are not set properly on slave host - Bug NethServer/dev#6009
- HotSync: nsdc and machines.target status are not synced - Bug NethServer/dev#6011
- HotSync: avoid logs sync - NethServer/dev#6012
- HotSync: backup-data shouldn't be executed on slave host - NethServer/dev#6013
- HotSync: improve promote action - NethServer/dev#6015

* Wed Oct 16 2019 Stefano Fancello <stefano.fancello@nethesis.it> - 2.0.3-1
- Avoid useless email if scheduled too often

* Fri Mar 23 2018 Davide Principi <davide.principi@nethesis.it> - 2.0.2-1
- Hotsync does not restore special shared folder ACLs  - Bug NethServer/dev#5433

* Mon Mar 12 2018 Davide Principi <davide.principi@nethesis.it> - 2.0.1-1
- Hotsync restore fails with no internet connection - Bug NethServer/dev#5430

* Fri Jan 12 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.0-1
- nethserver-hotsync: new implementation for NS 7 - NethServer/dev#5401

* Fri Jul 15 2016 Stefano Fancello <stefano.fancello@nethesis.it> - 1.0.0-1
- First package

