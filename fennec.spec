
%define name	    fennec
%define version     4.0.1
%define release     %mkrel 1
%define fennecdir   %{_libdir}/%{name}-%{version}

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
BuildRequires:  xulrunner-devel
BuildRequires:  libnotify-devel
BuildRequires:  libiw-devel
BuildRequires:	yasm
BuildRequires:	libvpx-devel
BuildRequires:	bzip2-devel
BuildRequires:	mesagl-devel
BuildRequires:	libproxy-devel
Source0:	http://fr2.rpmfind.net/linux/mozilla/mobile/releases/%{version}/source/%{name}-%{version}.source.tar.bz2
Source2:	.mozconfig
Source3:	fennec.desktop
Source4:	icons_fennec.tar.bz2

%description
This is the Firefox Mobile (code name Fennec) web browser which 
aims to provide rich Internet experience for Inte-processor-based 
plataforms. Fennec is recommended for devices that have a small 
or touch screen.

%prep 
%setup -qn mozilla-2.1

%build
export CXXFLAGS="%optflags -fpermissive"
%configure2_5x \
	--enable-application=xulrunner \
	--enable-application=mobile \
	--disable-elf-hack \
	--with-pthreads \
	--with-system-jpeg \
	--with-system-zlib \
	--with-system-bz2 \
	--with-system-libevent \
	--without-system-png \
	--with-system-nspr \
	--with-system-nss \
	--disable-ldap \
	--disable-calendar \
	--disable-mailnews \
	--disable-chatzilla \
	--disable-composer \
	--disable-profilesharing \
	--disable-toolkit-qt \
	--disable-installer \
	--disable-updater \
	--disable-debug \
	--disable-pedantic \
	--disable-native-uconv \
	--disable-elf-dynstr-gc \
	--disable-crashreporter \
	--disable-strip \
	--enable-crypto \
	--disable-gnomevfs \
	--enable-gnomeui \
	--enable-places \
	--enable-storage \
	--enable-default-toolkit=cairo-gtk2 \
	--enable-official-branding \
	--enable-svg \
	--enable-svg-renderer=cairo \
	--enable-single-profile \
	--enable-startup-notification \
	--enable-system-cairo \
	--disable-javaxpcom \
	--enable-optimize \
	--enable-safe-browsing \
	--enable-xinerama \
	--enable-canvas \
	--enable-pango \
	--enable-xtf \
	--enable-wave \
	--enable-webm \
	--enable-ogg \
	--enable-xpcom-fastload \
	--enable-gio \
	--enable-dbus \
	--enable-image-encoder=all \
	--enable-image-decoders=all \
	--enable-extensions=default \
	--enable-system-hunspell \
	--enable-install-strip \
	--enable-url-classifier \
	--disable-faststart \
	--enable-smil \
	--disable-tree-freetype \
	--enable-canvas3d \
	--disable-coretext \
	--enable-necko-protocols=all \
	--disable-necko-wifi \
	--disable-tests \
	--disable-mochitest \
	--with-distribution-id=com.mandriva \
	--with-valgrind \
	--enable-jemalloc \
	--enable-system-sqlite \
	--enable-chrome-format=jar \
	--with-default-mozilla-five-home="%{fennecdir}"
%make

%install 
rm -fr %buildroot
make package

mkdir -p %{buildroot}%{fennecdir}
cp -R dist/fennec/* %{buildroot}%{fennecdir}

# desktop file
mkdir -p %{buildroot}%{_datadir}/{applications,icons}
cp -R %{SOURCE3} %{buildroot}%{_datadir}/applications

#icons
tar xjf %{SOURCE4} -C %{buildroot}%{_datadir}/icons

# executable script 
mkdir -p %{buildroot}%{_bindir}
echo "#!/bin/sh" >> %{buildroot}%{_bindir}/fennec
echo "%{fennecdir}/fennec" >> %{buildroot}%{_bindir}/fennec
chmod +x %{buildroot}%{_bindir}/fennec

# enable cursor
sed -i 's/^pref("browser.ui.cursor", false);/pref("browser.ui.cursor", true);/g' %{buildroot}%{fennecdir}/defaults/preferences/mobile.js 
 
# desktop-file-install --vendor="" \
#  --remove-category="Application" \
#  --add-category="Networking" \
#  --add-category="X-MandrivaLinux-CrossDesktop" \
#  --add-mime-type="application/vnd.ms-works;application/x-msworks-wp;zz-application/zz-winassoc-wps" \
#  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/fenne.desktop

%files
%defattr (-,root,root)
%{fennecdir}
%{_datadir}/applications/fennec.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_bindir}/fennec


