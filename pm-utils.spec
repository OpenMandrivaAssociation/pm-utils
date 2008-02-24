%define name pm-utils
%define version 0.99.3
%define rel %mkrel 7

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
Source50: power-policy.conf
Source51: pm-has-power-policy
Patch1:	pm-utils-0.99.3-service_status.patch
Patch2: pm-utils-0.99.3-s2disk.patch
# (fc) 0.99.2-0.20070307.1mdv allow pm-hibernate/suspend to be called on command line
Patch3: pm-utils-0.99.2-cmdline.patch
# (fc) 0.99.2-0.20070307.2mdv be really FHS compliant
Patch4: pm-utils-fhs.patch
# (fc) 0.99.3-1mdv fix config loading (CVS)
Patch6: pm-utils-0.99.3-cfg.patch
# (fc) 0.99.3-1mdv remove vbe input redirect (CVS)
Patch7: pm-utils-0.99.3-vbe-redirect.patch
# (fc) 0.99.3-1mdv allow to disable suspend/hibernate using config file (Fedora bug #216459)
Patch8: pm-utils-0.99.3-disable.patch
# (fc) 0.99.3-1mdv cvs fixes (radeon quirks, export variable, add support for brightness restoration)
Patch9: pm-utils-0.99.3-cvsfixes.patch
Patch10: pm-utils-0.99.3-resume_label.patch
# (fc) 0.99.3-5mdv do not allow kernel hibernation if no resume partition is set
Patch11: pm-utils-0.99.3-checkresume.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: hal-devel 
BuildRequires: pkgconfig 
BuildRequires: pciutils-devel
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

%prep
%setup -q
%patch1 -p1 -b .service_status
%patch2 -p1 -b .s2disk
%patch3 -p1 -b .cmdline
%patch4 -p1 -b .fhs
%patch6 -p1 -b .cfg
%patch7 -p1 -b .vbe-redirect
%patch8 -p1 -b .disable
%patch9 -p1 -b .cvsfixes
%patch10 -p1 -b .resume_label
%patch11 -p1 -b .checkresume

#needed by patch4
autoreconf

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

install -m 755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d
for x in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE8} ; do
	y=$(basename ${x%%.pam})
	install -T -m 644 $x $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/$y
done
install -m 755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/security/console.apps/
for x in %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} ; do
	y=$(basename ${x%%.app})
	install -T -m 644 $x $RPM_BUILD_ROOT/%{_sysconfdir}/security/console.apps/$y
done
install -m 755 -d $RPM_BUILD_ROOT/%{_bindir}
pushd $RPM_BUILD_ROOT/%{_bindir}
for x in pm-hibernate pm-powersave pm-restart pm-shutdown pm-suspend pm-suspend-hybrid ; do
	ln -sf consolehelper $x
done
popd

install -m 755 %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27} $RPM_BUILD_ROOT%{_datadir}/pm-utils/sleep.d/
rm $RPM_BUILD_ROOT%{_datadir}/pm-utils/sleep.d/01grub

install -m 644 %{SOURCE50} -D $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/power-policy.conf
install -m 755 %{SOURCE51} $RPM_BUILD_ROOT%{_bindir}/pm-has-power-policy
install -d -m 755 $RPM_BUILD_ROOT/var/log
install -m 600 /dev/null $RPM_BUILD_ROOT/var/log/pm-suspend.log


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -a %{_var}/log/pm-suspend.log ] ; then
        install -m 600 /dev/null %{_var}/log/pm-suspend.log
fi


%files
%defattr(-,root,root)
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
%{_datadir}/pm-utils
%{_mandir}/man*/*
%ghost %verify(not md5 size mtime) %{_var}/log/pm-suspend.log
