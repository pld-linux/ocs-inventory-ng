#
Summary:	OCS-ng Inventory
Summary(pl):	OCS-ng Inventory
Name:		ocs-ng-inventory
Version:	1.0
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/ocsinventory/OCSNG_LINUX_SERVER_%{version}-RC1.tar.gz
# Source0-md5:	3fbc457d43f0ba7a3848d7cf7aa8bc09
Source1:	http://dl.sourceforge.net/ocsinventory/OCSNG_LINUX_AGENT_%{version}-RC1.tar.gz
# Source1-md5:	2381218545de4e546e992b0d2076bebf
Source2:	http://dl.sourceforge.net/ocsinventory/OCSNG_LINUX_SERVER_PATCH_%{version}-RC1-1.tar.gz
# Source2-md5:	513831077e60b7b38da5382c953ec55c
URL:		http://ocsinventory.sourceforge.net
#BuildRequires:	-
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	group(foo)
#Provides:	user(foo)
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open Computer and Software Inventory Next Generation is an application
designed to help a network or system administrator keep track of the
computer configuration and software installed on the network.

Dialog between client computers and management server is based on
actual standards, HTTP protocol and XML data formatting.

Management server runs on Apache/MySQL/PHP/PERL server, under Linux or
Windows NT based computers.

Inventoried client computers can run Microsoft Windows
95/98/Me/NT4/2000/XP/2003 or Linux operating systems.

Used with a parc management software such as GLPI, you will have a
powerfull inventory and parc management software with automatic
updates of computer configuration, license management, help desk and
more.

%description -l pl

%package agent
Summary:	-
Summary(pl):	-
Group:		-

%description agent

%description agent -l pl

%prep
%setup -q -n OCSNG_LINUX_SERVER_1.0-RC1
#%setup -q -n OCSNG_LINUX_AGENT_1.0-RC1
#%setup -q -c -T
#%setup -q -n %{name}
#%%setup -q -n %{name}-%{version}.orig -a 1
#%patch0 -p1

# undos the source
#find '(' -name '*.php' -o -name '*.inc' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

# remove CVS control files
#find -name CVS -print0 | xargs -0 rm -rf

%build
# if ac/am/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%%{__intltoolize}
#%%{__gettextize}
#%%{__libtoolize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
#cp -f /usr/share/automake/config.sub .
%configure
%{__make}

#%{__make} \
#	CFLAGS="%{rpmcflags}" \
#	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO

%files agent
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
