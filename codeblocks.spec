%define Werror_cflags %nil
%global optflags %{optflags} -fpermissive -fno-strict-aliasing
%define major		0
%define libname_orig	lib%{name}
%define libname		%mklibname %{name} 0
%define develname	%mklibname -d %{name}

Name:		codeblocks
Version:	13.12
Release:	2
Summary:	A C++ IDE
Group:		Development/Other
License:	GPLv3
URL:		https://www.codeblocks.org/
Source0:	http://sourceforge.net/projects/codeblocks/files/Sources/12.11/%{name}_%{version}-1.tar.gz
Source1:	%{name}.png
Source100:	%{name}.rpmlintrc
BuildRequires:	zip
BuildRequires:  autoconf
BuildRequires:  wxgtku2.8-devel
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(gamin)
BuildRequires:	libboost-devel
Requires:       %{libname} >= %{EVRD}
Suggests:	gcc-c++


%description
Code::Blocks is a free C++ IDE built specifically to meet the most 
demanding needs of its users. It was designed, right from the start, 
to be extensible and configurable.
Built around a plugin framework, Code::Blocks can be extended with 
plug-in DLLs. It includes a plugin wizard so you can compile your own
plug-ins!

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
%setup -qn %{name}-%{version}

%build
%configure2_5x --with-contrib-plugins=all --disable-static
%make

%install
%makeinstall_std


mkdir -p %{buildroot}%{_iconsdir}/hicolor/{128x128,256x256}/apps
convert -scale 128x128 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png
install -m 0644 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png

chmod +x %{buildroot}%{_datadir}/%{name}/lexers/lexer_bash.sample

%files
%doc README AUTHORS BUGS COMPILERS TODO NEWS ChangeLog
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/*/*.png
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png

%files -n %{libname}
%doc README ChangeLog
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%doc BUGS COMPILERS TODO
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
