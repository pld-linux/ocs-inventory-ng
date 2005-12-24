Summary:	OCS-ng Inventory - keeping track of the configuration and installed software
Summary(pl):	OCS-ng Inventory - ¶ledzenie konfiguracji i zainstalowanego oprogramowania
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
URL:		http://ocsinventory.sourceforge.net/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open Computer and Software Inventory Next Generation is an application
designed to help a network or system administrator keep track of the
computer configuration and software installed on the network.

Dialog between client computers and management server is based on
actual standards, HTTP protocol and XML data formatting.

Management server runs on Apache/MySQL/PHP/Perl server, under Linux or
Windows NT based computers.

Inventoried client computers can run Microsoft Windows
95/98/Me/NT4/2000/XP/2003 or Linux operating systems.

Used with a park management software such as GLPI, you will have a
powerful inventory and park management software with automatic
updates of computer configuration, license management, help desk and
more.

%description -l pl
Open Computer and Software Inventory Next Generation to aplikacja
zaprojektowana, aby pomóc administratorom sieci lub systemów w
¶ledzeniu konfiguracji komputerów i oprogramowania zainstalowanego w
sieci.

Dialog miêdzy komputerami klienckimi a serwerem zarz±dzaj±cym jest
oparty na w³a¶ciwych standardach, takich jak protokó³ HTTP i format
danych XML.

Serwer zarz±dzaj±cy dzia³a na serwerze Apache/MySQL/PHP/Perl pod
Linuksem lub Windows NT.

Inwentaryzowane komputery klienckie mog± dzia³aæ pod kontrol± systemu
Microsoft Windows 95/98/Me/NT4/2000/XP/2003 lub Linux.

Przy u¿yciu oprogramowania do zarz±dzania parkiem informatycznym,
takiego jak GLPI, otrzymamy potê¿ne oprogramowanie do inwentaryzacji i
zarz±dzania parkiem z automatycznym uaktualnianiem konfiguracji
komputerów, zarz±dzaniem licencjami, help deskiem itd.

%package agent
Summary:	OCS-ng Inventory agent for PLD systems
Summary(pl):	Agent OCS-ng Inventory dla systemów PLD
Group:		Networking/Daemons

%description agent
OCS-ng Inventory agent for PLD systems.

%description agent -l pl
Agent OCS-ng Inventory dla systemów PLD.

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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO

#%files agent
#%defattr(644,root,root,755)
