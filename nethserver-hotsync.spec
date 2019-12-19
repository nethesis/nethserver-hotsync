Summary: NethServer Hotsync 
Name: nethserver-hotsync
Version: 2.0.3
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

