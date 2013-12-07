%define quirks 20100619

Name:		pm-utils
Version:	1.4.1
Release:	8
Summary:	Power management utilities and scripts
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://pm-utils.freedesktop.org/wiki/
Source0:	http://pm-utils.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source1:	pm-suspend.pam
Source2:	pm-hibernate.pam
Source3:	pm-powersave.pam
Source4:	pm-suspend.app
Source5:	pm-hibernate.app
Source6:	pm-powersave.app
Source7:	pm-suspend-hybrid.app
Source8:	pm-suspend-hybrid.pam
Source20:	01bootloader
Source21:	10network
Source22:	92disk
Source23:	30pcmcia
Source24:	40xlock
Source25:	06mysqld
Source27:	15sound
Source28:	91laptop-mode
Source50:	power-policy.conf
Source51:	pm-has-power-policy
Source52:	http://pm-utils.freedesktop.org/releases/pm-quirks-%{quirks}.tar.gz
#- Mandriva
Patch100:	pm-utils-1.2.4-service_status.patch
# (fc) 0.99.3-5mdv do not allow kernel hibernation if no resume partition is set
Patch101:	pm-utils-1.2.4-checkresume.patch
Patch102:	pm-utils-1.2.4-s2diskdev.patch
Patch103:	pm-utils-1.2.0-uswsusp-default.patch
Patch104:	pm-utils-1.2.4-s2both_quirks.patch
# (bor) ported from hal-info
Patch105:	pm-quirks-20100619-untested_quirks.patch

# Use append instead of write for init_logfile (#660329)
Patch200:	pm-utils-1.4.1-init-logfile-append.patch
# Fix typo in 55NetworkManager (#722759)
Patch201:	pm-utils-1.4.1-networkmanager-typo-fix.patch
# Add support for grub2 in 01grub hook
Patch202:	pm-utils-1.4.1-grub2.patch
# Fix hooks exit code logging
Patch203:	pm-utils-1.4.1-hook-exit-code-log.patch
# Fix line spacing in logs to be easier to read (#750755)
Patch204:	pm-utils-1.4.1-log-line-spacing-fix.patch
# Fix NetworkManager dbus methods (fd.o #42500 / RH #740342)
Patch205:	pm-utils-1.4.1-nm_method.patch
# Add support for in-kernel (from kernel 3.6) suspend to both (#843657)
Patch206:	pm-utils-1.4.1-add-in-kernel-suspend-to-both.patch

BuildRequires:	xmlto
BuildRequires:	pkgconfig(dbus-1)
Requires:	usermode-consoleonly
Requires:	pciutils
Requires:	radeontool
%ifnarch %arm %mips
Requires:	vbetool
Requires:	bootloader-utils
%endif
Requires:	pm-fallback-policy
#Requires:	suspend-s2ram
Suggests:	suspend
# conflict with laptop-mode-tools, its functionalities overlap pm-utils, and
# upstream thinks it should conflict
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=612710#59
# (ahmad) 18-05-2011
# (cg) Updated:	Let's replace it completely (mga#5603)
%rename	laptop-mode-tools 1.61-2

%description
The pm-utils package contains utilities and scripts
useful for power management.

%package devel
Summary:	Files for development using %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the pkg-config files for development
when building programs that use %{name}.

%prep
%setup -q
%setup -q -a 52
#- Mandriva
%apply_patches

%build
%configure2_5x
%make

%install
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

%ifnarch %arm %mips
source20=%{SOURCE20}
%endif
install -m 755 ${source20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE27} %{SOURCE28} %{buildroot}%{_libdir}/pm-utils/sleep.d/
rm %{buildroot}%{_libdir}/pm-utils/sleep.d/01grub

install -m 644 %{SOURCE50} -D %{buildroot}%{_sysconfdir}/dbus-1/system.d/power-policy.conf
install -m 755 %{SOURCE51} %{buildroot}%{_bindir}/pm-has-power-policy
install -d -m 755 %{buildroot}/var/log
install -m 600 /dev/null %{buildroot}/var/log/pm-suspend.log

# quirks DB
cp -a video-quirks %{buildroot}%{_libdir}/pm-utils

%post
if [ ! -a %{_var}/log/pm-suspend.log ] ; then
        install -m 600 /dev/null %{_var}/log/pm-suspend.log
fi


%files
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
%{_libdir}/pkgconfig/%{name}.pc

