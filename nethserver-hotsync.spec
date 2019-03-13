Summary: NethServer Enterprise Hotsync 
Name: nethserver-hotsync
Version: 2.0.2
Release: 1%{?dist}
License: Firmware
Group: System Environment/Base
Source0: %{name}-%{version}.tar.gz
# Execute prep-sources to create Source1
Source1: %{name}-ui.tar.gz

Packager: Stefano Fancello <stefano.fancello@nethesis.it>
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

%install
rm -rf %{buildroot}
(cd root ; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist

#cockpit creation and installation
mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/
cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/

%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc README.rst


%changelog
* Fri Mar 23 2018 Davide Principi <davide.principi@nethesis.it> - 2.0.2-1
- Hotsync does not restore special shared folder ACLs  - Bug NethServer/dev#5433

* Mon Mar 12 2018 Davide Principi <davide.principi@nethesis.it> - 2.0.1-1
- Hotsync restore fails with no internet connection - Bug NethServer/dev#5430

* Fri Jan 12 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.0-1
- nethserver-hotsync: new implementation for NS 7 - NethServer/dev#5401

* Fri Jul 15 2016 Stefano Fancello <stefano.fancello@nethesis.it> - 1.0.0-1
- First package

