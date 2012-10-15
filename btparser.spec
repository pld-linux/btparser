Summary:	Parser and analyzer for backtraces produced by GDB
Name:		btparser
Version:	0.20
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://fedorahosted.org/released/abrt/%{name}-%{version}.tar.xz
# Source0-md5:	dac50574a3015d6ca6eb588a2efb4686
URL:		http://fedorahosted.org/btparser
%ifarch %{x8664}
BuildRequires:	binutils-static
%endif
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Btparser is a backtrace parser and analyzer, which works with
backtraces produced by the GNU Project Debugger. It can parse a text
file with a backtrace to a tree of C structures, allowing to analyze
the threads and frames of the backtrace and work with them.

Btparser also contains some backtrace manipulation and extraction
routines:
- it can find a frame in the crash-time backtrace where the program
  most likely crashed (a chance is that the function described in that
  frame is buggy)
- it can produce a duplication hash of the backtrace, which helps to
  discover that two crash-time backtraces are duplicates, triggered by
  the same flaw of the code
- it can "rate" the backtrace quality, which depends on the number of
  frames with and without the function name known (missing function
  name is caused by missing debugging symbols)

%package libs
Summary:	Btparser library
Summary(pl.UTF-8):	Biblioteka btparser
Group:		Libraries
Requires:	python-libs
Requires:	python-modules

%description libs
Btparser libraries

%description libs -l pl.UTF-8
Biblioteka btparser.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package -n python-btparser
Summary:	Python bindings for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-btparser
Python bindings for %{name}.

%prep
%setup -q

%build
%ifarch %{x8664}
%configure \
	--enable-fingerprints
%else
%configure
%endif
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{py_sitedir}/btparser/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README RELEASE TODO
%attr(755,root,root) %{_bindir}/btparser
%{_mandir}/man1/btparser.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbtparser.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libbtparser.so.2

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/btparser.pc
%{_includedir}/btparser
%{_libdir}/libbtparser.so

%files -n python-btparser
%{py_sitedir}/btparser/*.py*
%attr(755,root,root) %{py_sitedir}/btparser/*.so
