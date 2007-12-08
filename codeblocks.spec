%define libname_orig lib%{name}
%define libname %mklibname %{name} 0
%define develname %mklibname -d %{name}

Name:		codeblocks
Version:	1.0
Release:	%mkrel 0.rc2.1
Summary:	An open source, cross platform, free C++ IDE
Group:		Development/Other
License:	GPL
URL:		http://www.codeblocks.org/
Source:		%{name}-%{version}rc2.tar.bz2
Patch0:		codeblocks-1.0rc2-fix-extraqualification.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	zip
BuildRequires:	dos2unix
BuildRequires:  autoconf
BuildRequires:  libwxgtku2.6-devel

%description
Code::Blocks is a free C++ IDE built specifically to meet the most 
demanding needs of its users. It was designed, right from the start, 
to be extensible and configurable.
Built around a plugin framework, Code::Blocks can be extended with 
plugin DLLs. It includes a plugin wizard so you can compile your own plugins!

Features:

   Highlights:

    * Open Source! GPL2, no hidden costs.
    * Cross-platform. Runs on Linux or Windows (uses wxWidgets).
    * Made in GNU C++. No interpreted languages or proprietary libs needed.
    * Comes in two presentations: Standalone, and MinGW bundle
    * Devpack support (optional)
    * Extensible thru plugins (SDK available in the downloads section)

  Compiler-related features:

    * Multiple compiler support:
       	  o GCC (MingW / Linux GCC)
          o MSVC++
          o Digital Mars
          o Borland C++ 5.5
          o Open Watcom
    * Compiles directly or with makefiles
    * Predefined project templates
    * Custom template support
    * Uses XML format for project files.
    * Multi-target projects
    * Workspaces support
    * Imports MSVC projects and workspaces
         (NOTE: assembly code and inter-project dependencies not supported yet)
    * Imports Dev-C++ projects
    * Integrates with GDB for debugging
 
  Interface Features:

    * Syntax highlighting, customizable and extensible
    * Code folding for C++ and XML files.
    * Tabbed interface
    * Code completion plugin
    * Class Browser
    * Smart indent
    * One-key swap between .h and .c/.cpp files
    * Open files list for quick switching between files (optional)
    * External customizable "Tools"
    * To-do list management with different users 
%files
%defattr(-,root,root)
%doc README COPYING AUTHORS BUGS COMPILERS TODO NEWS ChangeLog
%{_bindir}/codeblocks
%{_bindir}/console_runner
%{_datadir}/application-registry/codeblocks.applications
%{_datadir}/applications/codeblocks.desktop
%dir %{_datadir}/codeblocks
%{_datadir}/codeblocks/*.zip
%{_datadir}/codeblocks/*.txt
%dir %{_datadir}/codeblocks/icons
%{_datadir}/codeblocks/icons/*.ico
%{_datadir}/codeblocks/icons/*.xpm
%dir %{_datadir}/codeblocks/images
%{_datadir}/codeblocks/images/*.png
%dir %{_datadir}/codeblocks/images/16x16
%{_datadir}/codeblocks/images/16x16/*.png
%dir %{_datadir}/codeblocks/images/codecompletion
%{_datadir}/codeblocks/images/codecompletion/*.png
%dir %{_datadir}/codeblocks/lexers
%{_datadir}/codeblocks/lexers/*.sample
%{_datadir}/codeblocks/lexers/*.xml
%dir %{_datadir}/codeblocks/plugins
%{_datadir}/codeblocks/plugins/*.la
%{_datadir}/codeblocks/plugins/*.so
%dir %{_datadir}/codeblocks/templates
%{_datadir}/codeblocks/templates/*.cpp
%{_datadir}/codeblocks/templates/*.cbp
%{_datadir}/codeblocks/templates/*.png
%{_datadir}/codeblocks/templates/*.template
%{_datadir}/codeblocks/templates/*.h
%{_datadir}/codeblocks/templates/*.c
%{_datadir}/codeblocks/templates/*.bmp
%{_iconsdir}/gnome/48x48/mimetypes/gnome-mime-application-x-codeblocks.png
%{_datadir}/mime-info/codeblocks.keys
%{_datadir}/mime-info/codeblocks.mime
%{_datadir}/mime/packages/codeblocks.xml
%{_datadir}/pixmaps/codeblocks.png

#--------------------------------------------------------------------

%package -n %{libname}
Summary:        %name  library
Group:          Graphical desktop/KDE
Provides:       %{libname_orig} = %{version}-%{release}
Requires:       %name = %version-%release

%description -n %{libname}
Library for %name

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcodeblocks.so.0
%{_libdir}/libcodeblocks.so.0.0.1
%{_libdir}/libwxscintilla.so.0
%{_libdir}/libwxscintilla.so.0.0.1

#--------------------------------------------------------------------

%package -n %{develname}
Summary:        Headers of %name for development
Group:          Development/C
Requires:       %{libname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{libname_orig}-devel = %{version}-%{release}

%description -n %{develname}
Headers of %{name} for development.

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libcodeblocks.la
%{_libdir}/libcodeblocks.so
%{_libdir}/libwxscintilla.la
%{_libdir}/libwxscintilla.so
%{_libdir}/pkgconfig/codeblocks.pc

#--------------------------------------------------------------------

%prep

%setup -n codeblocks-1.0rc2
%patch0 -p0

%build
chmod a+x bootstrap acinclude.m4 src/update
dos2unix bootstrap acinclude.m4 codeblocks.pc.in configure.in Makefile.am

# clean up files which cause confusion when switch versions of auto*
rm -rf autom4te.cache

# Fire up autotools
libtoolize --force --copy && \
        aclocal $ACLOCAL_FLAGS && \
        autoheader && \
        automake --include-deps --add-missing --foreign --copy && \
        autoconf


%configure
%make

%install
make DESTDIR=%buildroot install

%clean
