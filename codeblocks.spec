%define major		0
%define libname_orig	lib%{name}
%define libname		%mklibname %{name} 0
%define develname	%mklibname -d %{name}
%define	pkgdatadir	%{_datadir}/%{name}
%define	pkglibdir	%{_libdir}/%{name}
%define	plugindir	%{pkglibdir}/plugins

Name:		codeblocks
Version:	8.02
Release:	%mkrel 4
Summary:	A C++ IDE
Group:		Development/Other
License:	GPLv3
URL:		http://www.codeblocks.org/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.bz2
# Fedora packaging rules
Patch1:         codeblocks-plugins.patch
# update to recent standards + bug #487796 (http://developer.berlios.de/patch/?func=detailpatch&patch_id=2567&group_id=5358)
Patch2:         codeblocks-desktop.patch
# bug #461120 (http://developer.berlios.de/patch/?func=detailpatch&patch_id=2568&group_id=5358)
Patch3:         codeblocks-run.patch
# bug #469096 (fixed in upstream svn revision 5159)
Patch4:         codeblocks-8.02-gcc-detect.patch
# fix for gcc 4.4/glibc 2.9.90 http://developer.berlios.de/patch/index.php?func=detailpatch&patch_id=2699&group_id=5358
Patch5:         codeblocks-drop-const.patch
# fix GSocket conflict between glib >= 2.21 and wxGTK
Patch6:         codeblocks-8.02-gsocket.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	zip
BuildRequires:  autoconf
BuildRequires:  wxgtku2.8-devel
BuildRequires:	imagemagick
Suggests:	gcc-c++

%description
Code::Blocks is a free C++ IDE built specifically to meet the most 
demanding needs of its users. It was designed, right from the start, 
to be extensible and configurable.
Built around a plugin framework, Code::Blocks can be extended with 
plugin DLLs. It includes a plugin wizard so you can compile your own
plugins!

%package -n %{libname}
Summary:        Shared library for %{name}
Group:          System/Libraries
Provides:       %{libname_orig} = %{version}-%{release}

%description -n %{libname}
Shared libraries for %{name}.

%package -n %{develname}
Summary:        Development headers for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{libname_orig}-devel = %{version}-%{release}

%description -n %{develname}
Development headers for %{name}.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p0 -b .run
%patch4 -p0 -b .gcc-detect
%patch5 -p1 -b .gcc44
%patch6 -p1 -b .gsocket

# fix the dir, where plugins are installed
for p in astyle autosave classwizard codecompletion compilergcc debuggergdb defaultmimehandler openfileslist projectsimporter scriptedwizard todo xpmanifest
do
	sed -i 's|$(pkgdatadir)/plugins|@libdir@/@PACKAGE@/plugins|' src/plugins/$p/Makefile.*
done

for p in AutoVersioning BrowseTracker ThreadSearch byogames cb_koders codesnippets codestat dragscroll envvars help_plugin keybinder lib_finder profiler regex_testbed source_exporter symtab wxSmith wxSmithContribItems
do
	sed -i 's|$(pkgdatadir)/plugins|@libdir@/@PACKAGE@/plugins|' src/plugins/contrib/$p/Makefile.*
done

sed -i 's|$(pkgdatadir)/plugins|@libdir@/@PACKAGE@/plugins|' src/plugins/contrib/wxSmith/plugin/Makefile.*

sed -i 's|@libdir@|%{_libdir}|' src/sdk/configmanager.cpp

# remove execute bits from source files
find src/plugins/contrib/regex_testbed -type f -exec chmod a-x {} ';'
find src/plugins/compilergcc -type f -exec chmod a-x {} ';'

# fix version inside the configure script
sed -i 's/1\.0svn/%{version}/g' configure

%build
%configure2_5x --with-contrib-plugins=all
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make

%install
rm -rf %{buildroot}
%makeinstall_std INSTALL="/usr/bin/install -p"

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale 48x48 src/setup/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32x32 src/setup/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16x16 src/setup/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README AUTHORS BUGS COMPILERS TODO NEWS ChangeLog
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*.1*
%{_datadir}/applications/codeblocks.desktop
%{_datadir}/%{name}
%{_iconsdir}/*/*/*/*
%{_datadir}/mime/packages/codeblocks.xml
%{_datadir}/pixmaps/codeblocks.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.*a
%{_libdir}/*.so
%{_libdir}/pkgconfig/codeblocks.pc
%{_includedir}/%{name}
