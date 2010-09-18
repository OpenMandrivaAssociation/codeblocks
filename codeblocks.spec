%define major		0
%define libname_orig	lib%{name}
%define libname		%mklibname %{name} 0
%define develname	%mklibname -d %{name}

Name:		codeblocks
Version:	10.05
Release:	%mkrel 2
Summary:	A C++ IDE
Group:		Development/Other
License:	GPLv3
URL:		http://www.codeblocks.org/
Source0:	http://download.berlios.de/codeblocks/%{name}-%{version}-src.tar.bz2
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
%setup -qn %{name}-%{version}-release

%build
%define Werror_cflags %nil
%configure2_5x --with-contrib-plugins=all --with-wx-config=%{_bindir}/wx-config-unicode
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale 48x48 src/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32x32 src/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16x16 src/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

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
%{_libdir}/wxSmithContribItems
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
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
