# TODO
# - spec name to ocs-inventory-ng.spec
# - webapps
# - agent
Summary:	OCS-Inventory NG - keeping track of the configuration and installed software
Summary(pl):	OCS-Inventory NG - �ledzenie konfiguracji i zainstalowanego oprogramowania
Name:		ocs-inventory-ng
Version:	1.0
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/ocsinventory/OCSNG_LINUX_SERVER_%{version}RC3-1.tar.gz
# Source0-md5:	014b06827371e47b3509965656ca18d3
Source1:	http://dl.sourceforge.net/ocsinventory/OCSNG_LINUX_AGENT_%{version}RC3.tar.gz
# Source1-md5:	34edd057f1937245d06c3515c0ff50ad
Source2:	http://dl.sourceforge.net/ocsinventory/OCS_Inventory_NG-Installation_and_Administration_Guide_1.7_EN.odt
# Source2-md5:	da52c1e4201dcbf249b2a71db9de6b5f
Source3:	http://dl.sourceforge.net/ocsinventory/OCS_Inventory_NG-Installation_and_Administration_Guide_1.7_EN.pdf
# Source3-md5:	bd9a9792bab51f6aae5109a1c39b0a48
Patch0:		%{name}-config.patch
URL:		http://ocsinventory.sourceforge.net/
Requires:	apache >= 1.3.33
Requires:	apache-mod_perl >= 1.29
Requires:	apache-mod_php >= 4.3.2
Requires:	perl-Apache-DBI >= 0.93
Requires:	perl-Compress-Zlib >= 1.33
Requires:	perl-DBD-mysql >= 2.9004
Requires:	perl-DBI >= 1.40
Requires:	perl-Net-IP >= 1.21
Requires:	perl-XML-Simple >= 2.12
Requires:	perl-base >= 1:5.6
Requires:	php-common >= 3:4.3.2
Requires:	php-pecl-zip
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_webappconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

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
powerful inventory and park management software with automatic updates
of computer configuration, license management, help desk and more.

%description -l pl
Open Computer and Software Inventory Next Generation to aplikacja
zaprojektowana, aby pom�c administratorom sieci lub system�w w
�ledzeniu konfiguracji komputer�w i oprogramowania zainstalowanego w
sieci.

Dialog mi�dzy komputerami klienckimi a serwerem zarz�dzaj�cym jest
oparty na w�a�ciwych standardach, takich jak protok� HTTP i format
danych XML.

Serwer zarz�dzaj�cy dzia�a na serwerze Apache/MySQL/PHP/Perl pod
Linuksem lub Windows NT.

Inwentaryzowane komputery klienckie mog� dzia�a� pod kontrol� systemu
Microsoft Windows 95/98/Me/NT4/2000/XP/2003 lub Linux.

Przy u�yciu oprogramowania do zarz�dzania parkiem informatycznym,
takiego jak GLPI, otrzymamy pot�ne oprogramowanie do inwentaryzacji i
zarz�dzania parkiem z automatycznym uaktualnianiem konfiguracji
komputer�w, zarz�dzaniem licencjami, help deskiem itd.

%package agent
Summary:	OCS-ng Inventory agent for PLD systems
Summary(pl):	Agent OCS-ng Inventory dla system�w PLD
Group:		Networking/Daemons

%description agent
OCS-ng Inventory agent for PLD systems.

%description agent -l pl
Agent OCS-ng Inventory dla system�w PLD.

%prep
%setup -q -n OCSNG_LINUX_SERVER_%{version}RC3-1 -a 1
%patch0 -p1

# undos the source
find '(' -name '*.php' -o -name '*.inc' -o  -name '*.conf' -o  -name '*.htc' -o  -name '*.js' -o  -name '*.dtd' -o  -name '*.pm' -o  -name '*.css' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%build
cd Apache
%{__perl} Makefile.PL \
		INSTALLDIRS=vendor
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd Apache
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..

install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_sysconfdir}/logrotate.d,%{_var}/log/%{name}}
install -d $RPM_BUILD_ROOT{%{_appdir},%{_webappconfdir}}
cp -Rf ocsreports/* $RPM_BUILD_ROOT%{_datadir}/%{name}

install Apache/logrotate.ocsinventory-NG $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ocs-inventory-ng
install Apache/ocsinventory.conf $RPM_BUILD_ROOT%{_webappconfdir}/apache.conf
install Apache/ocsinventory.conf $RPM_BUILD_ROOT%{_webappconfdir}/httpd.conf
install ipdiscover-util/ipdiscover-util.pl $RPM_BUILD_ROOT%{_datadir}/%{name}/ipdiscover-util.pl

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README ocs-errors $SOURCE2 $SOURCE3
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ocs-inventory-ng
%attr(750,root,http) %dir %{_webappconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webappconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webappconfdir}/httpd.conf
%attr(755,root,root) %{_bindir}/Ocsinventory_local.pl
%{_datadir}/%{name}/
%{perl_vendorlib}/
%attr(770,root,http) %dir %{_var}/log/%{name}

#%files agent
#%defattr(644,root,root,755)
