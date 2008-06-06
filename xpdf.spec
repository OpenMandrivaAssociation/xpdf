%define urwdir %{_datadir}/fonts/default/Type1
%define lesstifver	0.93.41
%define freetypever	2.1.5
%define x11dir		/usr/X11R6
%define build_lesstif	1
%define build_freetype2	0
%define usefreetype2	1
%define	pkgversion	3.02
%define fversion	3.02

Summary:	A PDF file viewer for the X Window System
Name:		xpdf
Version:	%{pkgversion}
Release:	%mkrel 11
License:	GPLv2+
Source:		ftp://ftp.foolabs.com/pub/xpdf/%{name}-%{fversion}.tar.bz2
Source1:	icons-%{name}.tar.bz2
Source2:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-chinese-simplified.tar.bz2
Source3:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-chinese-traditional.tar.bz2
Source4:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-cyrillic.tar.bz2
Source5:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-japanese.tar.bz2
Source6:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-korean.tar.bz2
Source7:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-thai.tar.bz2
Source8:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-greek.tar.bz2
Source9:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-latin2.tar.bz2
Source10:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-turkish.tar.bz2
Source11:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-hebrew.tar.bz2
Source12:	ftp://ftp.hungry.com/pub/hungry/lesstif/srcdist/lesstif-%{lesstifver}.tar.bz2
Source13:	ftp://ftp.freetype.org/freetype/freetype2/freetype-%{freetypever}.tar.bz2
Source14:	ftp://ftp.foolabs.com/pub/xpdf/%{name}-arabic.tar.bz2

Patch2:		%{name}-3.01-antihigh.patch
Patch3:		%{name}-3.02-mozilla.patch
Patch4:		%{name}-3.00-autohinting.patch
Patch5:		%{name}-2.02-ext.patch
Patch6:		%{name}-2.03-zoom.patch
# use some debian patches for static freetype 2.1.5
Patch9:		%{name}-2.03-ft215deb.patch
#
Patch10:	%{name}-3.01-xpdfrc3.patch
Patch11:	%{name}-3.00-pdftoppm.patch
Patch16:	%{name}-chinese.patch
Patch17:	%{name}-3.02-CAN-2005-0206.patch
Patch18:	%{name}-3.00-gcc401.patch
Patch19:	%{name}-3.01-core.patch
Patch20:	%{name}-3.01-crash.patch
Patch21:	%{name}-3.01-xfont.patch
Patch22:	%{name}-3.02pl1.patch
Patch23:	%{name}-3.02-CVE-2007-4352_5392_5393.patch
#
URL:		http://www.foolabs.com/xpdf/
Group:		Office
BuildRequires:	X11-devel
BuildRequires:	xpm-devel
BuildRequires:	t1lib-devel
BuildRequires:	freetype2-devel >= 2.0.5
BuildConflicts:	libpaper-devel
BuildRequires: autoconf
%if %build_lesstif
BuildRequires:	libfontconfig-devel
BuildConflicts:	lesstif-devel
%else
BuildRequires:	lesstif-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	urw-fonts
# Lesstiff user interface requires these (btw, why a static lesstif and freetype?)
Requires:	x11-font-adobe-75dpi
Requires:	x11-font-adobe-100dpi
Requires:	%name-common = %version-%release

%description
Xpdf is an X Window System based viewer for Portable Document Format (PDF)
files. PDF files are sometimes called Acrobat files, after Adobe Acrobat
(Adobe's PDF viewer).  Xpdf is a small and efficient program which uses
standard X fonts.

%package common
Group: Text tools
Summary:	Common files for xpdf and the applications based on it
Conflicts:	xpdf < 3.02-7

%description common
Xpdf is an X Window System based viewer for Portable Document Format (PDF)
files. PDF files are sometimes called Acrobat files, after Adobe Acrobat
(Adobe's PDF viewer).  Xpdf is a small and efficient program which uses
standard X fonts.

This package contains common files (such as UnicodeMap and xpdfrc) needed for
xpdf and the applications based on it.

%prep
%setup -q -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -n %{name}-%{fversion}

%patch2 -p1 -b .antihigh
%patch3 -p1 -b .mozilla
%patch4 -p1 -b .autohint
%patch5 -p1 -b .mktemp
%patch6 -p1 -b .zoom
%if %build_freetype2
%patch9 -p1 -b .deb
%endif
%patch10 -p1 -b .30
%patch11 -p1 -b .ppm
%patch16 -p1 -b .chinese
%patch17 -p1 -b .CAN-2005-0206
%patch18 -p1 -b .gcc401
%patch19 -p1 -b .core
%patch20 -p1 -b .crash
%patch21 -p1 -b .xfont
%patch22 -p1 -b .CVE-2007-3387
%patch23 -p1 -b .cve-2007-4352_5392_5393
%build
CURRENTDIR=`pwd`

# build a local lesstif library
%if %build_lesstif
(cd lesstif-%{lesstifver}
libtoolize -c -f
CFLAGS="$RPM_OPT_FLAGS" \
	./configure \
			--prefix=%{x11dir} \
			--libdir=%{x11dir}/%{_lib} \
			--disable-shared \
			--enable-static \
			--disable-build-12 \
			--disable-build-20 \
			--enable-build-21 \
			--enable-default-21 \
			--disable-maintainer-mode \
			--disable-debug
%make
make install \
	prefix=$CURRENTDIR/lesstif-local \
	libdir=$CURRENTDIR/lesstif-local/lib
)
%endif

# build a local freetype2 library
%if %build_freetype2
(cd freetype-%{freetypever}
%configure2_5x --disable-shared
%make
make install DESTDIR=$CURRENTDIR/freetype2-local \
)
%endif

# build xpdf
autoconf
export X_EXTRA_LIBS="-lXft -lXrender -lfontconfig -lz"
%configure2_5x --with-gzip \
	   --bindir=%{_bindir} \
	   --mandir=%{_mandir} \
	   --enable-a4-paper \
	   --enable-opi \
%if %build_lesstif
	   --with-Xm-library=$CURRENTDIR/lesstif-local/lib \
	   --with-Xm-includes=$CURRENTDIR/lesstif-local/include \
%endif
%if %build_freetype2
	   --enable-freetype2 \
	   --with-freetype2-includes=$CURRENTDIR/freetype2-local%{_includedir}/freetype2 \
	   --with-freetype2-library=$CURRENTDIR/freetype2-local%{_libdir} \
%endif
%if %usefreetype2
	   --enable-freetype2 \
	   --with-freetype2-includes=%{_includedir}/freetype2 \
%endif
	   --enable-japanese \
	   --enable-chinese-gb \
	   --enable-chinese-cns

make all

perl -pi -e 's@/usr/local/etc/@%{_sysconfdir}/@' doc/*.1 doc/*.5
perl -pi -e 's@/usr/local/share/ghostscript/fonts@%{urwdir}@' doc/sample-xpdfrc doc/*.1 doc/*.5
perl -pi -e 's@^#displayFontT1@displayFontT1@' doc/sample-xpdfrc
for i in chinese-simplified chinese-traditional cyrillic japanese \
	korean thai greek latin2 turkish hebrew arabic; \
	do
		perl -pi -e 's@/usr/local/share/xpdf@%{_datadir}/xpdf@' \
			xpdf-$i/add-to-xpdfrc \
			xpdf-$i/README
		echo >> doc/sample-xpdfrc
		cat xpdf-$i/add-to-xpdfrc >> doc/sample-xpdfrc
		rm xpdf-$i/add-to-xpdfrc 
	done
# Xpdf no longer supports X fonts
perl -pi -e 's/^displayCIDFontX/#displayCIDFontX/g' doc/sample-xpdfrc
perl -pi -e 's/^#urlCommand.*/urlCommand "www-browser %s"/' doc/sample-xpdfrc

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
make DESTDIR=%{buildroot} install
for i in chinese-simplified chinese-traditional cyrillic japanese \
	korean thai greek latin2 turkish hebrew arabic; \
	do
		mkdir -p %{buildroot}%{_datadir}/%{name}/$i
		cp -a xpdf-$i/* %{buildroot}%{_datadir}/%{name}/$i/
	done

install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/applications/
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Xpdf
Comment=Views PDF files
Exec=%_bindir/xpdf %f
Icon=%name
Terminal=false
Type=Application
StartupNotify=true
MimeType=text/pdf;text/x-pdf;application/pdf;application/x-pdf;
Categories=X-MandrivaLinux-Office-Publishing;Office;Viewer;
EOF


# mdk icons
install -d %{buildroot}%{_iconsdir}
tar xjf %SOURCE1 -C %{buildroot}%{_iconsdir}

# remove unpackaged files
rm -f %{buildroot}%{_bindir}/pdf* %{buildroot}%{_mandir}/man1/pdf*

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES README
%{_bindir}/xpdf
%{_mandir}/man1/xpdf.1*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/*.*
%{_liconsdir}/*.*
%{_miconsdir}/*.*

%files common
%defattr(-,root,root)
%{_datadir}/%{name}
%{_mandir}/man5/*
%config(noreplace) %{_sysconfdir}/xpdfrc

