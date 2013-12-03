Summary:	Parser and analyzer for backtraces produced by GDB
Summary(pl.UTF-8):	Analizator śladów wywołań tworzonych przez GDB
Name:		btparser
Version:	0.25
Release:	4
License:	GPL v2+
Group:		Development/Tools
Source0:	https://fedorahosted.org/released/btparser/%{name}-%{version}.tar.xz
# Source0-md5:	7fcf3f97dd6df827151638a41855c5bb
URL:		http://fedorahosted.org/btparser/
%ifarch %{x8664}
BuildRequires:	binutils-static
%endif
BuildRequires:	glib2-devel >= 1:2.21
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xz
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

%description -l pl.UTF-8
Btparser to analizator śladów wywołań (backtrace'ów), działający ze
śladami tworzonymi przez debugger GDB z projektu GNU. Potrafi
przetworzyć plik tekstowy ze śladem na drzewo struktur C, co pozwala
na analizę wątków oraz ramek śladu wywołań i dalszą pracę z nimi.

Btparser zawiera także trochę procedur do obróbki i wydobywania śladów
wywołań:
- potrafi znaleźć ramkę w pośmiertnym śladzie wywołań, w której
  najprawdopodobniej nastąpiła wywrotka programu (możliwe, że to
  funkcja w tej ramce zawiera błąd)
- potrafi utworzyć skrót (hasz) śladu, pozwalający wykryć, czy dwa
  zadane ślady pośmiertne są duplikatami spowodowanymi tym samym
  błędem w kodzie
- potrafi "ocenić jakość" śladów, zależną od liczby ramek ze znaną i
  bez znanej nazwy funkcji (brak nazwy funkcji wynika z braku symboli
  diagnostycznych)

%package libs
Summary:	Btparser library
Summary(pl.UTF-8):	Biblioteka btparser
Group:		Libraries
Requires:	glib2 >= 1:2.21

%description libs
Btparser library.

%description libs -l pl.UTF-8
Biblioteka btparser.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.21

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package -n python-btparser
Summary:	Python bindings for %{name}
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki btparser
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-modules

%description -n python-btparser
Python bindings for %{name}.

%description -n python-btparser -l pl.UTF-8
Wiązania Pythona do biblioteki btparser.

%prep
%setup -q

%build
%configure \
%ifarch %{x8664}
	--enable-fingerprints
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{py_sitedir}/btparser/*.la

%py_postclean

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
%attr(755,root,root) %{_libdir}/libbtparser.so
%{_includedir}/btparser
%{_pkgconfigdir}/btparser.pc

%files -n python-btparser
%defattr(644,root,root,755)
%dir %{py_sitedir}/btparser
%{py_sitedir}/btparser/__init__.py[co]
%attr(755,root,root) %{py_sitedir}/btparser/_btparser.so
