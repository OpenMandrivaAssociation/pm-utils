%define name pm-utils
%define version 1.2.0
%define rel %mkrel 1

Name: %name
Version: %version
Release: %rel 
Summary: Power management utilities and scripts
License: GPL
Group: System/Kernel and hardware
Source0: pm-utils-%{version}.tar.gz
Source1: pm-suspend.pam
Source2: pm-hibernate.pam
Source3: pm-powersave.pam
Source4: pm-suspend.app
Source5: pm-hibernate.app
Source6: pm-powersave.app
Source7: pm-suspend-hybrid.app
Source8: pm-suspend-hybrid.pam
Source20: 01bootloader
Source21: 10network
Source22: 92disk
Source23: 30pcmcia
Source24: 40xlock
Source25: 06mysqld
Source26: 00splash
Source27: 15sound
Source28: 91laptop-mode
Source50: power-policy.conf
Source51: pm-has-power-policy
# from upstream git auto-quirks branch
Patch0: pm-utils-1.2.0-auto-quirks.patch
Patch1:	pm-utils-1.2.0-service_status.patch
Patch2: pm-utils-1.2.0-s2diskdev.patch
# (fc) 0.99.3-5mdv do not allow kernel hibernation if no resume partition is set
Patch11: pm-utils-0.99.3-checkresume.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: hal-devel 
BuildRequires: pkgconfig 
BuildRequires: dbus-devel

Obsoletes: pmscripts
Obsoletes: suspend-scripts
Provides: suspend-scripts = 1.27

Requires: usermode 
Requires: pciutils
Requires: radeontool
Requires: vbetool
Requires: hal-info
Requires: suspend
Requires: pm-fallback-policy

Conflicts: apmd < 3.2.2-11mdv2007.1
Conflicts: mkinitrd < 4.2.17-27mdv2007.1
Conflicts: initscripts < 8.48-5mdv2007.1

%description
The pm-utils package contains utilities and scripts
useful for power management.

%package devel
Summary: Files for development using %{name}
Group: Development/Other
Requires: %{name} = %{version}

%description devel
This package contains the pkg-config files for development
when building programs that use %{name}.

%prep
%setup -q
%patch0 -p1 -b .auto-quirks
%patch1 -p1 -b .service_status
%patch2 -p1 -b .s2diskdev
%patch11 -p1 -b .checkresume

# needed by auto-quirks patch0
autoreconf

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -m 755 -d %{buildroot}%{_sysconfdir}/pam.d
for x in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE8} ; do
	y=$(basename ${x%%.pam})
	install -T -m 644 $x %{buildroot}%{_sysconfdir}/pam.d/$y
done
install -m 755 -d %{buildroot}%{_sysconfdir}/security/console.apps/
for x in %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} ; do
	y=$(basename ${x%%.app})
	install -T -m 644 $x %{buildroot}%{_sysconfdir}/security/console.apps/$y
done
install -m 755 -d %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
for x in pm-hibernate pm-powersave pm-restart pm-shutdown pm-suspend pm-suspend-hybrid ; do
	ln -sf consolehelper $x
done
popd

install -m 755 %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{buildroot}%{_libdir}/pm-utils/sleep.d/
rm %{buildroot}%{_libdir}/pm-utils/sleep.d/01grub

install -m 644 %{SOURCE50} -D %{buildroot}%{_sysconfdir}/dbus-1/system.d/power-policy.conf
install -m 755 %{SOURCE51} %{buildroot}%{_bindir}/pm-has-power-policy
install -d -m 755 %{buildroot}/var/log
install -m 600 /dev/null %{buildroot}/var/log/pm-suspend.log


%clean
rm -rf %{buildroot}

%post
if [ ! -a %{_var}/log/pm-suspend.log ] ; then
        install -m 600 /dev/null %{_var}/log/pm-suspend.log
fi


%files
%defattr(-,root,root)
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}/*
%dir %{_sysconfdir}/pm
%dir %{_sysconfdir}/pm/power.d
%dir %{_sysconfdir}/pm/sleep.d
%dir %{_sysconfdir}/pm/config.d
%{_sysconfdir}/security/console.apps/*
%{_sysconfdir}/pam.d/*
%{_sysconfdir}/dbus-1/system.d/power-policy.conf
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/pm-utils
%{_mandir}/man*/*
%ghost %verify(not md5 size mtime) %{_var}/log/pm-suspend.log

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/%{name}.pc
