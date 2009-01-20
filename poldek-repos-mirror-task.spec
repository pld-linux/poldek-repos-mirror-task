%define		mirror	task
Summary:	Mirror source for poldek
Name:		poldek-repos-mirror-%{mirror}
Version:	2.99
Release:	0.9
License:	GPL v2+
Group:		Applications/System
Source0:	%{name}.conf
Source1:	%{name}-multilib.conf
URL:		http://poldek.pld-linux.org/
Requires:	poldek
Provides:	poldek-source-main
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/poldek/repos.d

%description
Mirror source for poldek.

%package multilib
Summary:	Mirror multilib source for poldek
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Provides:	poldek-source-multilib

%description multilib
Mirror multilib source for poldek.

%prep
%setup -q -c -T

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%ifarch i486 i686 ppc sparc alpha athlon
%define		_ftp_arch	%{_target_cpu}
%endif
%ifarch %{x8664}
%define		_ftp_arch	x86_64
%define		_ftp_alt_arch	i686
%endif
%ifarch i586
%if "%{pld_release}" == "ti"
%define		_ftp_arch	i586
%else
%define		_ftp_arch	i486
%endif
%endif
%ifarch pentium2 pentium3 pentium4
%define		_ftp_arch	i686
%endif
%ifarch sparcv9 sparc64
%define		_ftp_arch	sparc
%endif

sed -e '
	s|%%ARCH%%|%{_ftp_arch}|g
' < %{SOURCE0} > $RPM_BUILD_ROOT%{_sysconfdir}/mirror-%{mirror}.conf

%ifarch %{x8664}
sed '
	s|%%ARCH%%|%{_ftp_alt_arch}|g
' < %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/mirror-%{mirror}-multilib.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mirror-%{mirror}.conf

%ifarch %{x8664}
%files multilib
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mirror-%{mirror}-multilib.conf
%endif
