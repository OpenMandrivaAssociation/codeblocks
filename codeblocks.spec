%define major		0
%define libname_orig	lib%{name}
%define libname		%mklibname %{name} 0
%define develname	%mklibname -d %{name}

Name:		codeblocks
Version:	10.05
Release:	%mkrel 4
Summary:	A C++ IDE
Group:		Development/Other
License:	GPLv3
URL:		http://www.codeblocks.org/
Source0:	http://download.berlios.de/codeblocks/%{name}-%{version}-src.tar.bz2
BuildRequires:	zip
BuildRequires:  autoconf
BuildRequires:  wxgtku2.8-devel
BuildRequires:	imagemagick
Suggests:	gcc-c++
Patch0:		codeblocks-10.05-gcc47.patch
Patch1:		codeblocks-10.05-wxChartCtrl-crash.patch

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
%patch0 -p1
%patch1 -p1

%build
%define Werror_cflags %nil
%configure2_5x --with-contrib-plugins=all --with-wx-config=%{_bindir}/wx-config-unicode --disable-static
%make LIBS="-lX11 -pthread"

%install
%makeinstall_std

find %{buildroot} -name '*.la' | xargs rm

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale 48x48 src/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32x32 src/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16x16 src/mime/codeblocks.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%files
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
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
