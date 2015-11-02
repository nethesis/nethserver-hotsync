Summary: NethServer Enterprise Hotsync 
Name: nethserver-hotsync
Version:  0.0.8
Release:  1%{dist}
License: Firmware
Group: System Environment/Base
Source0: %{name}-%{version}.tar.gz
Packager: Stefano Fancello <stefano.fancello@nethesis.it>
BuildArch: noarch
Requires: nethserver-base nethserver-backup-config nethserver-backup-data rsync
BuildRequires: nethserver-devtools
AutoReq: no

%description
NethServer Hotsync is a tool that simplifies configuration of rsync to keep two NethServer up to date


%prep
%setup -q

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-%{release}-filelist

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)

%changelog
