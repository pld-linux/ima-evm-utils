#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	IMA/EVM signing utility and library
Summary(pl.UTF-8):	Biblioteka i narzędzie do podpisów IMA/EVM
Name:		ima-evm-utils
Version:	1.4
Release:	2
License:	GPL v2+
Group:		Applications/System
Source0:	https://downloads.sourceforge.net/linux-ima/%{name}-%{version}.tar.gz
# Source0-md5:	d1cb73c10857b5526ee1f37769c5458a
URL:		http://linux-ima.sourceforge.net/
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	keyutils-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libxslt-progs
BuildRequires:	openssl-devel >= 0.9.8
BuildRequires:	pkgconfig
BuildRequires:	tpm2-tss-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux kernel integrity subsystem is comprised of a number of different
components including the Integrity Measurement Architecture (IMA),
Extended Verification Module (EVM), IMA-appraisal extension, digital
signature verification extension and audit measurement log support.

The evmctl utility is used for producing and verifying digital
signatures, which are used by the Linux kernel integrity subsystem. It
is also used for importing keys into the kernel keyring.

Linux integrity subsystem allows to use IMA and EVM signatures. EVM
signature protects file metadata, such as file attributes and extended
attributes. IMA signature protects file content.

%description -l pl.UTF-8
Podsystem integralności jądra Linuksa składa się z kilku różnych
komponentów, w tym IMA (Integrity Measurement Architecture -
architektury pomiaru integralności), EVM (Extended Verification Module
- modułu rozszerzonej weryfikacji), rozszerzenia oceny IMA,
rozszerzenia weryfikacji podpisów cyfrowych oraz obsługi logowania
pomiaru audytu.

Narzędzie evmctl służy do tworzenia i weryfikacji podpisów cyfrowych
używanych przez podsystem integralności jądra Linuksa, a także do
importowania kluczy do obszaru jądra.

Podsystem integralności Linuksa pozwala na używanie podpisów IMA i
EVM. Podpisy EVM chronią metadane plików, takie jak atrybuty i
rozszerzone atrybuty plików. Podpisy IMA chronią zawartość plików.

%package lib
Summary:	IMA/EVM library
Summary(pl.UTF-8):	Biblioteka IMA/EVM
Group:		Libraries

%description lib
IMA/EVM library.

%description lib -l pl.UTF-8
Biblioteka IMA/EVM.

%package devel
Summary:	Header files for IMA/EVM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki IMA/EVM
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}

%description devel
Header files for IMA/EVM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki IMA/EVM.

%package static
Summary:	Static IMA/EVM library
Summary(pl.UTF-8):	Statyczna biblioteka IMA/EVM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static IMA/EVM library.

%description static -l pl.UTF-8
Statyczna biblioteka IMA/EVM.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-kernel-headers=/usr/include
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/ima-*.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README examples/ima-*.sh
%attr(755,root,root) %{_bindir}/evmctl
%{_mandir}/man1/evmctl.1*

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libimaevm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libimaevm.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libimaevm.so
%{_libdir}/libimaevm.la
%{_includedir}/imaevm.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libimaevm.a
%endif
