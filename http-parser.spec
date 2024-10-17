# we use the upstream version from http_parser.h as the SONAME
%define somajor 2
%define sominor 0

%define libname %mklibname %{name} %{somajor}
%define devname %mklibname -d %{name}

Name:           http-parser
Version:        2.9.4
Release:        2
Summary:        HTTP request/response parser for C
Group:          System/Libraries
License:        MIT
URL:            https://github.com/joyent/http-parser
Source0:	https://github.com/joyent/http-parser/archive/v%{version}/%{name}-%{version}.tar.gz
# Build shared library with SONAME using gyp and remove -O flags so optflags take over
# TODO: do this nicely upstream
Patch1:		http-parser-gyp-sharedlib.patch
BuildRequires:	gyp
#BuildRequires:	python2-pkg-resources
BuildRequires:	python-pkg-resources

%description
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).

%package -n %{libname}
Summary:	A parser for HTTP messages written in C
Group:		System/Libraries
# Do this provide as a temp fix for nodejs
Provides:	http-parser = %{version}-%{release}

%description -n %{libname}
This is a parser for HTTP messages written in C. It parses both requests and
responses. The parser is designed to be used in performance HTTP applications.
It does not make any syscalls nor allocations, it does not buffer data, it can
be interrupted at anytime. Depending on your architecture, it only requires
about 40 bytes of data per message stream (in a web server that is per
connection).

%package -n %{devname}
Group:		Development/C
Summary:	Development headers and libraries for http-parser
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development headers and libraries for http-parser.

%prep
%setup -q
%autopatch -p0

%build
# TODO: fix -fPIC upstream
export CFLAGS='%{optflags} -fPIC'
gyp -f make --depth=`pwd` http_parser.gyp
%make_build BUILDTYPE=Release CC=%{__cc} CXX=%{__cxx}

%install
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}

install -pm644 http_parser.h %{buildroot}%{_includedir}

#install regular variant
install out/Release/lib.target/libhttp_parser.so.%{somajor} %{buildroot}%{_libdir}/libhttp_parser.so.%{somajor}.%{sominor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser.so.%{somajor}
ln -sf libhttp_parser.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser.so

#install strict variant
install out/Release/lib.target/libhttp_parser_strict.so.%{somajor} %{buildroot}%{_libdir}/libhttp_parser_strict.so.%{somajor}.%{sominor}
ln -sf libhttp_parser_strict.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser_strict.so.%{somajor}
ln -sf libhttp_parser_strict.so.%{somajor}.%{sominor} %{buildroot}%{_libdir}/libhttp_parser_strict.so

%check
export LD_LIBRARY_PATH='./out/Release/lib.target'
./out/Release/test-nonstrict
./out/Release/test-strict

%files -n %{libname}
%doc AUTHORS 
%{_libdir}/libhttp_parser.so.%{somajor}
%{_libdir}/libhttp_parser.so.%{somajor}.*
%{_libdir}/libhttp_parser_strict.so.%{somajor}
%{_libdir}/libhttp_parser_strict.so.%{somajor}.*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/libhttp_parser.so
%{_libdir}/libhttp_parser_strict.so
