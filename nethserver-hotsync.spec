Summary: NethServer Enterprise Hotsync 
Name: nethserver-hotsync
Version: 1.0.0
Release: 1%{?dist}
License: Firmware
Group: System Environment/Base
Source0: %{name}-%{version}.tar.gz
Packager: Stefano Fancello <stefano.fancello@nethesis.it>
BuildArch: noarch
Requires: nethserver-base nethserver-backup-config rsync stunnel
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


%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update

%changelog
* Fri Jul 15 2016 Stefano Fancello <stefano.fancello@nethesis.it> - 1.0.0-1
- First package

