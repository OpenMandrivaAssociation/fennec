
%define name	    fennec
%define version     1.0
%define release     %mkrel 0.a1.4
%define fennecdir   %{_libdir}/%{name}-%{version}
%define _provides_exceptions libfreebl3.so\\|libimgicon.so\\|libmozjs.so\\|libMyService.so\\|libnkgnomevfs.so\\|libnptest.so\\|libnptest.so\\|libnspr4.so\\|libnss3.so\\|libnssckbi.so\\|libnssdbm3.so\\|libnssutil3.so\\|libnullplugin.so\\|libplc4.so\\|libplds4.so\\|libsmime3.so\\|libsoftokn3.so\\|libsqlite3.so\\|libssl3.so\\|libtestdynamic.so\\|libunixprintplugin.so\\|libxpcomsample.so\\|libxpcom.so\\|libxul.so

%define _requires_exceptions libmozjs.so\\|libnspr4.so\\|libnspr4.so\\|libnss3.so\\|libnssutil3.so\\|libplc4.so\\|libplds4.so\\|libsmime3.so\\|libsoftokn3.so\\|libsqlite3.so\\|libssl3.so\\|libxpcom.so\\|libxul.so

# update
# %# define subrel 1

Name:		%{name}
Summary:	Fennec - the Moblin Web Browser for Mandriva-Mini
Version:	%{version}
Release:	%{release}
License: 	MPL
Vendor:		Mandriva
Packager:	Rafael da Veiga Cabral <cabral@mandriva.com>
Group:	        Networking/WWW
Url: 		http://www.moblin.org/projects/moblin-browser
# BuildRoot:      %{_tmppath}/%{name}-%{version}-buildroot

BuildRequires: autoconf2.1
BuildRequires: alsa-lib-devel

BuildRequires:	gtk+2-devel
BuildRequires:	libx11-devel
BuildRequires:	unzip
BuildRequires:	zip
#(tpg) older versions doesn't support apng extension
BuildRequires:	libpng-devel >= 1.2.25-2
BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	libcairo-devel
BuildRequires:	glib2-devel
BuildRequires:	libIDL2-devel
BuildRequires:	makedepend
#(tpg) don't use system nss and nspr as they are not updated to latest version which supports ff3
BuildRequires:	nss-devel
BuildRequires:	nspr-devel
BuildRequires:	startup-notification-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	lcms-devel
BuildRequires:	python-devel
# (fhimpe) Starting from Firefox 3.0.1, at least sqlite 3.5.9 is needed
# so only use system sqlite on Mandriva >= 2009.0
%if %mdkversion >= 200900
BuildRequires:	libsqlite3-devel >= 3.5.9
%endif
BuildRequires:	valgrind
BuildRequires:	rootcerts
BuildRequires:	libxt-devel
BuildRequires:	hunspell-devel
BuildRequires:	doxygen
BuildRequires:	libgnome-vfs2-devel
BuildRequires:	libgnome2-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	java-rpmbuild
BuildRequires:  xulrunner-devel-unstable

# Requires: 	man > 1.0
# Requires:	sed = %{sedversion}

# Source0: 	http://ftp.mozilla.org/pub/mozilla.org/mozilla.org/mozilla.org/firefox/releases/3.1b1/source/firefox-3.1b1-source.tar.bz2

# Tag FENNEC_A1
Source0: 	http://hg.mozilla.org/mozilla-central/archive/cab97aca485d.tar.bz2

# Tag FENNEC_A1
Source1:        http://hg.mozilla.org/mobile-browser/archive/b394a7122c10.tar.bz2	
Source2:	.mozconfig
Source3:	fennec.desktop
Source4:	icons_fennec.tar.bz2

# Patch0:		testpackfix1.patch

# subpackage 
# %package testpack

%description
This is the Firefox Mobile (code name Fennec) web browser which 
aims to provide rich Internet experience for Inte-processor-based 
plataforms. Fennec is recommended for devices that have a small 
or touch screen.

%prep 

%setup -n mozilla-central-cab97aca485d
tar xjf %{SOURCE1} -C %{_builddir}

mv %{_builddir}/mobile-browser* %{_builddir}/mozilla-central-cab97aca485d/mobile
cp %{SOURCE2} %{_builddir}/mozilla-central-cab97aca485d


%build 

# got from firefox
# export PREFIX="%{_prefix}"
# export LIBDIR="%{_libdir}"
# export CFLAGS="%{optflags}"
# export CXXFLAGS="$CFLAGS"

cd %{_builddir}/mozilla-central-cab97aca485d/
make -f client.mk build

%install 

cd %{_builddir}/mobilebase/mobile
make package

rm -rf %{buildroot}
mkdir -p %{buildroot}%{fennecdir}
cp -R %{_builddir}/mobilebase/mobile/dist/fennec/* %{buildroot}%{fennecdir}

# desktop file
mkdir -p %{buildroot}%{_datadir}/{applications,icons}
cp -R %{SOURCE3} %{buildroot}%{_datadir}/applications

#icons
tar xjf %{SOURCE4} -C %{buildroot}%{_datadir}/icons

# executable script 
mkdir -p %{buildroot}%{_bindir}
echo "#!/bin/bash" >> %{buildroot}%{_bindir}/fennec
echo "/usr/lib/fennec-1.0/fennec" >> %{buildroot}%{_bindir}/fennec
chmod +x %{buildroot}%{_bindir}/fennec

# enable cursor
sed -i 's/^pref("browser.ui.cursor", false);/pref("browser.ui.cursor", true);/g' %{buildroot}%{fennecdir}/defaults/preferences/mobile.js 
 
# desktop-file-install --vendor="" \
#  --remove-category="Application" \
#  --add-category="Networking" \
#  --add-category="X-MandrivaLinux-CrossDesktop" \
#  --add-mime-type="application/vnd.ms-works;application/x-msworks-wp;zz-application/zz-winassoc-wps" \
#  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/fenne.desktop

%clean

%pre

%post

%preun 

%postun

%files
%defattr (-,root,root)

# xulrunner files 
%dir %{fennecdir}/xulrunner
%dir %{fennecdir}/xulrunner/res
%{fennecdir}/xulrunner/res/*.*
# %dir %{fennecdir}/xulrunner/samples
# %{fennecdir}/xulrunner/samples/*.*
# %dir %{fennecdir}/xulrunner/dtd
# %{fennecdir}/xulrunner/*.*
%dir %{fennecdir}/xulrunner/res/entityTables
%{fennecdir}/xulrunner/res/entityTables/*.*
%dir %{fennecdir}/xulrunner/res/fonts
%{fennecdir}/xulrunner/res/fonts/*.*
%dir %{fennecdir}/xulrunner/res/html
%{fennecdir}/xulrunner/res/html/*.*
%dir %{fennecdir}/xulrunner/components
%{fennecdir}/xulrunner/components/*.*
%dir %{fennecdir}/xulrunner/dictionaries
%{fennecdir}/xulrunner/dictionaries/*.*
%dir %{fennecdir}/xulrunner/greprefs
%{fennecdir}/xulrunner/greprefs/*.*
%dir %{fennecdir}/xulrunner/modules
%{fennecdir}/xulrunner/modules/*.*
%dir %{fennecdir}/xulrunner/defaults
%dir %{fennecdir}/xulrunner/defaults/autoconfig
%{fennecdir}/xulrunner/defaults/autoconfig/*.*
%dir %{fennecdir}/xulrunner/icons
%{fennecdir}/xulrunner/icons/*.*
%dir  %{fennecdir}/xulrunner/plugins
%{fennecdir}/xulrunner/plugins/*.*
%dir %{fennecdir}/xulrunner/chrome
# %dir %{fennecdir}/chrome/icons
# %{fennecdir}/xulrunner/chrome/icons/*.*
%{fennecdir}/xulrunner/chrome/*.*
%dir %{fennecdir}/xulrunner/defaults
%dir %{fennecdir}/xulrunner/defaults/autoconfig
%{fennecdir}/xulrunner/defaults/autoconfig/*.*
%dir %{fennecdir}/xulrunner/defaults/pref
%{fennecdir}/xulrunner/defaults/pref/*.*
%dir %{fennecdir}/xulrunner/defaults/profile
%dir %{fennecdir}/xulrunner/defaults/profile/US
%{fennecdir}/xulrunner/defaults/profile/US/*.*
%dir %{fennecdir}/xulrunner/defaults/profile/US/chrome
%{fennecdir}/xulrunner/defaults/profile/US/chrome/*.*
%dir %{fennecdir}/xulrunner/defaults/profile/chrome
%{fennecdir}/xulrunner/defaults/profile/chrome/*.*
%{fennecdir}/xulrunner/defaults/profile/*.*
%{fennecdir}/xulrunner/*
%{fennecdir}/xulrunner/.autoreg

# fennec files
%{fennecdir}/application.ini
%{fennecdir}/fennec

%dir %{fennecdir}/components
%{fennecdir}/components/nsTelProtocolHandler.js
%{fennecdir}/components/aboutFirstrun.js

%dir %{fennecdir}/searchplugins
%{fennecdir}/searchplugins/wikipedia.xml
%{fennecdir}/searchplugins/answers.xml
%{fennecdir}/searchplugins/yahoo.xml
%{fennecdir}/searchplugins/google.xml

%dir %{fennecdir}/chrome
%{fennecdir}/chrome/en-US.jar
%{fennecdir}/chrome/firstrun.jar
%{fennecdir}/chrome/browser.manifest
%{fennecdir}/chrome/en-US.manifest
%{fennecdir}/chrome/firstrun.manifest
%{fennecdir}/chrome/classic.jar
%{fennecdir}/chrome/classic.manifest
%{fennecdir}/chrome/browser.jar

%dir %{fennecdir}/defaults
%dir %{fennecdir}/defaults/preferences
%{fennecdir}/defaults/preferences/mobile.js

#desktop file
%{_datadir}/applications/fennec.desktop

#icons
%{_datadir}/icons/hicolor/*/apps/*

#executable script
%{_bindir}/fennec

%changelog 

* Wed Oct 22 2008 Rafael da Veiga Cabral - <cabral@mandriva.com> 1.0-0.a1.1mdv2009.1
- Revision 
- Version release 1.0a1
- Desktop icons worked fom first_run_splash.png (content.jar)


