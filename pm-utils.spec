%define name pm-utils
%define version 1.4.1
%define rel %mkrel 6
%define quirks 20100619

Name: %name
Version: %version
Release: %rel 
Summary: Power management utilities and scripts
License: GPL
Group: System/Kernel and hardware
URL: http://pm-utils.freedesktop.org/wiki/
Source0: http://pm-utils.freedesktop.org/releases/%{name}-%{version}.tar.gz
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
Source27: 15sound
Source28: 91laptop-mode
Source50: power-policy.conf
Source51: pm-has-power-policy
Source52: http://pm-utils.freedesktop.org/releases/pm-quirks-%{quirks}.tar.gz
#- Mandriva
Patch100: pm-utils-1.2.4-service_status.patch
# (fc) 0.99.3-5mdv do not allow kernel hibernation if no resume partition is set
Patch101: pm-utils-1.2.4-checkresume.patch
Patch102: pm-utils-1.2.4-s2diskdev.patch
Patch103: pm-utils-1.2.0-uswsusp-default.patch
Patch104: pm-utils-1.2.4-s2both_quirks.patch
# (bor) ported from hal-info
Patch105:   pm-quirks-20100619-untested_quirks.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pkgconfig 
BuildRequires: dbus-devel
BuildRequires: xmlto

Obsoletes: pmscripts
Obsoletes: suspend-scripts
Provides: suspend-scripts = 1.27-2mdv2007.1

Requires: usermode-consoleonly
Requires: pciutils
Requires: radeontool
%ifnarch %arm %mips
Requires: vbetool
%endif
Requires: pm-fallback-policy
#Requires: suspend-s2ram
Requires: bootloader-utils

Suggests: suspend

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
%setup -q -a 52
#- Mandriva
%patch100 -p1 -b .service_status
%patch101 -p1 -b .checkresume
%patch102 -p1 -b .s2diskdev
%patch103 -p1 -b .uswsusp-default
%patch104 -p1 -b .s2both_quirks
%patch105 -p0

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

install -m 755 %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE27} %{SOURCE28} %{buildroot}%{_libdir}/pm-utils/sleep.d/
rm %{buildroot}%{_libdir}/pm-utils/sleep.d/01grub

install -m 644 %{SOURCE50} -D %{buildroot}%{_sysconfdir}/dbus-1/system.d/power-policy.conf
install -m 755 %{SOURCE51} %{buildroot}%{_bindir}/pm-has-power-policy
install -d -m 755 %{buildroot}/var/log
install -m 600 /dev/null %{buildroot}/var/log/pm-suspend.log

# quirks DB
cp -a video-quirks %{buildroot}%{_libdir}/pm-utils

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


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4.1-3mdv2011.0
+ Revision: 667789
- mass rebuild

* Wed Nov 24 2010 Andrey Borzenkov <arvidjaar@mandriva.org> 1.4.1-2mdv2011.0
+ Revision: 600326
- source52: install quirks DB
  patch105: untested quirks ported from hal-info packages

* Tue Nov 23 2010 Eugeni Dodonov <eugeni@mandriva.com> 1.4.1-1mdv2011.0
+ Revision: 600273
- Updated to 1.4.1.
  Removed requirements for HAL.

* Tue Feb 23 2010 Frederik Himpe <fhimpe@mandriva.org> 1.2.6.1-2mdv2010.1
+ Revision: 510371
- Fix suspend-scripts provides to fix theoretical impossible situation
  (bug #55814)

* Thu Jan 07 2010 Frederik Himpe <fhimpe@mandriva.org> 1.2.6.1-1mdv2010.1
+ Revision: 487336
- Update to new version 1.2.6.1

* Sun Nov 08 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.6-1mdv2010.1
+ Revision: 462907
- Update to new version 1.2.6
- Remove patch integrated upstream

* Mon Sep 28 2009 Olivier Blin <oblin@mandriva.com> 1.2.5-4mdv2010.0
+ Revision: 450275
- do not require vbetool on mips & arm (from Arnaud Patard)

* Tue May 26 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 1.2.5-3mdv2010.0
+ Revision: 379999
- Require usermode-consoleonly instead of full GUI usermode

* Mon May 18 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.5-2mdv2010.0
+ Revision: 377368
- Add upstream patch (via Debian) fixing typo in have_kms function

* Sun May 17 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 1.2.5-1mdv2010.0
+ Revision: 376630
- new version
  * remove patch1 (integrated upstream)
  * add URL
- make it Suggest suspend instead of Require; it works also without

* Thu Apr 16 2009 Olivier Blin <oblin@mandriva.com> 1.2.4-4mdv2009.1
+ Revision: 367710
- sound hook: fix parsing state file when sound programs have arguments (like pulseaudio)

* Sun Apr 12 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.4-3mdv2009.1
+ Revision: 366441
- Add upstream patch fixing name of
  /sys/devices/system/cpu/sched_smt_power_savings tuneable
  (Debian bug #518680)

* Mon Mar 23 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 1.2.4-2mdv2009.1
+ Revision: 360712
- patch104: process quirks during hybrid suspend by pm-utils not s2both.
  This is required because our suspend disables quirks processing in s2both.

* Sat Mar 21 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.4-1mdv2009.1
+ Revision: 359554
- Update to new version 1.2.4
- Remove patches integrated upstream
- Rediff patches (thanks to Andrey Borzenkov)

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-4mdv2009.1
+ Revision: 319077
- rebuild

* Tue Sep 23 2008 Olivier Blin <oblin@mandriva.com> 1.2.0-3mdv2009.0
+ Revision: 287645
- remove useless splash hook, splashy is now spawned by the resume utility

* Tue Sep 16 2008 Frederic Crozat <fcrozat@mandriva.com> 1.2.0-2mdv2009.0
+ Revision: 285167
- Update source24 to use --display for calling gnome-screensaver-command

* Fri Sep 12 2008 Olivier Blin <oblin@mandriva.com> 1.2.0-1mdv2009.0
+ Revision: 284254
- buildrequire xmlto for man pages build
- pass resume device when running s2both for hybrid suspend
- use /sys/power/state instead of non-packaged s2ram (we should maybe handle pmu too...)
- do not make xlock hook fail if X is not running
- check Xorg instead of X in xlock hook
- fix sourcing of functions in our custom hooks
- fix logging bug that was aborting help after the first hook (from upstream)
- add missing has_parameter function for auto-quirk feature (from upstream)
- default to uswsusp
- adapt checkresume patch (with some duplication of s2diskdev patch), not tested yet
- adapt and merge s2disk/resume_label patch to the new uswsusp module (hopefully supporting hybrid suspend), not tested yet
- drop pciutils-devel buildrequire, vbetool is not built here anymore
- replace wonky cmdline patch by better auto-quirks patch (from upstream git auto-quirks branch)
- add pkgconfig file in a new devel subpackage
- package doc files
- drop fhs/lib64 patch, we can not guarantee that all hooks are arch-independant (and lib64 issue is now handled correctly upstream)
- drop disable patch, we can now handle this in hal fdi files
- drop merged CVS patch
- rediff service status patch
- 1.2.0

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.99.4-5mdv2009.0
+ Revision: 265478
- rebuild early 2009.0 package (before pixel changes)

* Mon May 19 2008 Olivier Blin <oblin@mandriva.com> 0.99.4-4mdv2009.0
+ Revision: 209122
- handle more hal video quirks when running pm-suspend from command line (s3_bios, s3_mode, vga_mode3, dpms_suspend, reset_brightness)

* Fri Mar 21 2008 Olivier Blin <oblin@mandriva.com> 0.99.4-3mdv2008.1
+ Revision: 189458
- rename 93laptop-mode as 91laptop-mode so that it gets run after disk/hdparm script on thaw/resume (Colin Guthrie)

* Fri Mar 21 2008 Olivier Blin <oblin@mandriva.com> 0.99.4-2mdv2008.1
+ Revision: 189449
- reload laptop-mode service on resume/thaw (mainly to reapply hdparm settings)

* Sun Mar 02 2008 Olivier Blin <oblin@mandriva.com> 0.99.4-1mdv2008.1
+ Revision: 177649
- 0.99.4
- remove merged patches from CVS
- rediff s2disk and fhs patches

* Sun Feb 24 2008 Andrey Borzenkov <arvidjaar@mandriva.org> 0.99.3-7mdv2008.1
+ Revision: 174370
- fix previous fix :(

* Sun Feb 24 2008 Andrey Borzenkov <arvidjaar@mandriva.org> 0.99.3-6mdv2008.1
+ Revision: 174356
- update patch10: fix getting resume device from LABEL=
  while at it, simplify code and add UUID support

* Tue Feb 05 2008 Frederic Crozat <fcrozat@mandriva.com> 0.99.3-5mdv2008.1
+ Revision: 162626
- Patch11: do not allow kernel hibernation if no resume partition is set

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 07 2007 Frederic Crozat <fcrozat@mandriva.com> 0.99.3-4mdv2008.1
+ Revision: 116344
- Update patch4, one file was missing correct path for function file

* Wed Sep 19 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.99.3-3mdv2008.0
+ Revision: 90162
- rebuild

* Sat Aug 11 2007 Olivier Blin <oblin@mandriva.com> 0.99.3-2mdv2008.0
+ Revision: 61892
- support for specifying resume device by LABEL (from Andrey Borzenkov, #32314)

* Tue Jul 31 2007 Frederic Crozat <fcrozat@mandriva.com> 0.99.3-1mdv2008.0
+ Revision: 57054
- Release 0.99.3
- add hybrid-suspend template (doesn't do anything now)
- remove patches 4
- regenerate patch 1, 2, 5
- Patch6 (CVS): fix configuration load
- Patch7 (CVS): remove incorrect vbe stdin redirect
- Patch8 (Fedora): allow do disable suspend/hibernate with config file
- Patch9 (CVS): various fixes (radeon quirks, export variables, add support for brightness restoration)

* Tue Jul 24 2007 Olivier Blin <oblin@mandriva.com> 0.99.2-0.20070307.11mdv2008.0
+ Revision: 54955
- revert unwanted spec modifications
- add back removed comment
- use plain autoreconf

* Tue Jul 24 2007 David Walluck <walluck@mandriva.org> 0.99.2-0.20070307.10mdv2008.0
+ Revision: 54893
- fix build
- make power-policy.conf mode 644

* Wed May 30 2007 Olivier Blin <oblin@mandriva.com> 0.99.2-0.20070307.9mdv2008.0
+ Revision: 32731
- remove pam_stack comments (#31113)


* Tue Mar 27 2007 Olivier Blin <oblin@mandriva.com> 0.99.2-0.20070307.8mdv2007.1
+ Revision: 149040
- add script to kill and restore sound applications (ported from suspend-scripts and enhanced by Mark Stosberg, #28910)
- provide suspend-scripts = 1.27

* Fri Mar 23 2007 Olivier Blin <oblin@mandriva.com> 0.99.2-0.20070307.7mdv2007.1
+ Revision: 148238
- conflicts with too old mkinitrd and initscripts

* Sun Mar 11 2007 Olivier Blin <oblin@mandriva.com> 0.99.2-0.20070307.6mdv2007.1
+ Revision: 141339
- do not impose resume device to be on kernel command line, prefer the one from suspend.conf if present

* Fri Mar 09 2007 Olivier Blin <oblin@mandriva.com> 0.99.2-0.20070307.5mdv2007.1
+ Revision: 138614
- fix quirk matching when run from command line

* Thu Mar 08 2007 Frederic Crozat <fcrozat@mandriva.com> 0.99.2-0.20070307.4mdv2007.1
+ Revision: 135002
-Patch5: fix function path for laptool-tools (Mdv bug #29267)

* Thu Mar 08 2007 Olivier Blin <oblin@mandriva.com> 0.99.2-0.20070307.3mdv2007.1
+ Revision: 134982
- fix resume= matching on cmdline (thanks to Mooby for the report)

* Wed Mar 07 2007 Frederic Crozat <fcrozat@mandriva.com> 0.99.2-0.20070307.2mdv2007.1
+ Revision: 134558
- Update sources and add patch4: try to be FHS compliant and nice for lib64

* Wed Mar 07 2007 Frederic Crozat <fcrozat@mandriva.com> 0.99.2-0.20070307.1mdv2007.1
+ Revision: 134434
- CVS snapshot of 0.99.2 release (not yet out)
- Update sources 1, 10, 92, 30, 40, 06 for new functions location
- Regenerate patches 1 & 2
- Remove patches 0, 3, merged upstream
- Patch3 : allow quirks when running pm-suspend/hibernate from commandline

* Wed Mar 07 2007 Frederic Crozat <fcrozat@mandriva.com> 0.19-12mdv2007.1
+ Revision: 134206
- Update patch0 to fix radeon quirk launch
- Patch3 (CVS): pm-pmu doesn't output error message on fail anymore

* Fri Mar 02 2007 Frederic Crozat <fcrozat@mandriva.com> 0.19-11mdv2007.1
+ Revision: 131579
- Resync patch0 with upstream : use sysctl instead of echo, add support
  for radeon and vga_mode quirk

* Thu Feb 08 2007 Olivier Blin <oblin@mandriva.com> 0.19-10mdv2007.1
+ Revision: 117750
- fix group (#28612)

* Mon Jan 22 2007 Olivier Blin <oblin@mandriva.com> 0.19-9mdv2007.1
+ Revision: 112045
- add splash hook

* Fri Jan 19 2007 Olivier Blin <oblin@mandriva.com> 0.19-8mdv2007.1
+ Revision: 110825
- require pm-fallback-policy

* Thu Jan 18 2007 Olivier Blin <oblin@mandriva.com> 0.19-7mdv2007.1
+ Revision: 110279
- use userspace hibernate by default (by requiring the suspend package)
- add userspace hibernate support (using s2disk)
- add /etc/pm/config.d directory
- make suspend-scripts obsolete
- restart mysqld in 06mysqld hook
- add xlock hook (ported from suspend-scripts)
- add pcmcia hook (based on previous work from Andrey Borzenkov and Michael Reinsch on suspend-scripts)
- add disk hook (using hdparm)
- add network hook
- fix service status check
- add bootloader hook using rebootin and drop grub hook

* Sat Jan 13 2007 Olivier Blin <oblin@mandriva.com> 0.19-5mdv2007.1
+ Revision: 108330
- conflicts will old apmd containing on_ac_power

* Thu Jan 11 2007 Olivier Blin <oblin@mandriva.com> 0.19-4mdv2007.1
+ Revision: 107427
- add pm-has-power-policy helper

* Thu Jan 11 2007 Olivier Blin <oblin@mandriva.com> 0.19-3mdv2007.1
+ Revision: 107394
- allow console users to own org.freedesktop.Policy.Power interface

* Mon Jan 08 2007 Olivier Blin <oblin@mandriva.com> 0.19-2mdv2007.1
+ Revision: 105387
- obsolete pmscripts package
- use hal-info to get video resume info (from Richard Hughes) and drop Fedora video patch

* Sun Dec 17 2006 Colin Guthrie <cguthrie@mandriva.org> 0.19-1mdv2007.1
+ Revision: 98286
- Import pm-utils

