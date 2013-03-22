#
Summary:	OCS-Inventory NG - keeping track of the configuration and installed software
Summary(pl.UTF-8):	OCS-Inventory NG - śledzenie konfiguracji i zainstalowanego oprogramowania
Name:		ocs-inventory-ng
Version:	2.0.5
Release:	0.0.1
License:	GPL
Group:		Applications
Source0:	https://launchpad.net/ocsinventory-server/stable-2.0/2.0.5/+download/OCSNG_UNIX_SERVER-%{version}.tar.gz
# Source0-md5:	349904d03494b8fd9fc4eea1d6859729
Source1:	http://download.ocsinventory-ng.org/pub/plugins/PluginOcsOfficekey-2.2.4.tar.gz
# Source1-md5:	ec8c319a17f6a0d8b104cdc2a8f20127
Patch0:		%{name}-plugin-officekey.patch
URL:		http://www.ocsinventory-ng.org/
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-devel >= 1:5.6
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
Requires:	php(core) >= 4.3.2
Requires:	php(zip)
Requires:	webapps
Requires:	webserver(indexfile)
Suggests:	perl-SOAP-Lite
Suggests:	perl-XML-Entities
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

%description -l pl.UTF-8
Open Computer and Software Inventory Next Generation to aplikacja
zaprojektowana, aby pomóc administratorom sieci lub systemów w
śledzeniu konfiguracji komputerów i oprogramowania zainstalowanego w
sieci.

Dialog między komputerami klienckimi a serwerem zarządzającym jest
oparty na właściwych standardach, takich jak protokół HTTP i format
danych XML.

Serwer zarządzający działa na serwerze Apache/MySQL/PHP/Perl pod
Linuksem lub Windows NT.

Inwentaryzowane komputery klienckie mogą działać pod kontrolą systemu
Microsoft Windows 95/98/Me/NT4/2000/XP/2003 lub Linux.

Przy użyciu oprogramowania do zarządzania parkiem informatycznym,
takiego jak GLPI, otrzymamy potężne oprogramowanie do inwentaryzacji i
zarządzania parkiem z automatycznym uaktualnianiem konfiguracji
komputerów, zarządzaniem licencjami, help deskiem itd.

%prep
%setup -q -n OCSNG_UNIX_SERVER-%{version} -a1
%patch0 -p1

mv -f PluginOcsOfficekey-2.2.4/README{,-Officekey}.txt
mv -f PluginOcsOfficekey-2.2.4/CHANGES{,-Officekey}.txt

# combine sql files
cat PluginOcsOfficekey-2.2.4/*.sql >> ocsreports/files/ocsbase.sql
cat PluginOcsOfficekey-2.2.4/*.sql >> ocsreports/files/ocsbase_new.sql

# mimic setup.sh
sed -e 's,PATH_TO_LOG_DIRECTORY,/var/log/ocs-inventory-ng,g' \
    -i etc/logrotate.d/ocsinventory-server

sed -e 's,VERSION_MP,2,g' \
    -e 's,DATABASE_SERVER,localhost,g' \
    -e 's,DATABASE_PORT,3306,g' \
    -e 's,PATH_TO_LOG_DIRECTORY,/var/log/ocs-inventory-ng/,g' \
    -i etc/ocsinventory/ocsinventory-server.conf

sed -e 's,OCSREPORTS_ALIAS,/ocsreports,g' \
    -e 's,PATH_TO_OCSREPORTS_DIR,/usr/share/ocs-inventory-ng,g' \
    -e 's,PACKAGES_ALIAS,/download,g' \
    -e 's,PATH_TO_PACKAGES_DIR,/var/lib/ocs-inventory-ng/,g' \
    -i etc/ocsinventory/ocsinventory-reports.conf

# combine apache files
cat etc/ocsinventory/ocsinventory-{server,reports}.conf > etc/ocsinventory/ocsinventory.conf

# prepare db config and drop install.php
rm ocsreports/install.php
cat > ocsreports/dbconfig.inc.php << 'EOF'
<?php
define('DB_NAME', 'ocsweb');
define('SERVER_READ', 'localhost');
define('SERVER_WRITE', 'localhost');
define('COMPTE_BASE', 'ocs');
define('PSWD_BASE', 'ocs');
EOF

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

# ocsreports + plugins
cp -Rf ocsreports/* $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a PluginOcsOfficekey-2.2.4/cd_officepack $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/computer_detail
cp -a PluginOcsOfficekey-2.2.4/img/cd_* $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/computer_detail/img/
cp -a PluginOcsOfficekey-2.2.4/ms_plugins/ms_plugins_packoffice.php $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/main_sections/ms_plugins
cp -a PluginOcsOfficekey-2.2.4/img/ms_* $RPM_BUILD_ROOT%{_datadir}/%{name}/plugins/main_sections/img/

install etc/logrotate.d/ocsinventory-server $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ocs-inventory-ng
install etc/ocsinventory/ocsinventory.conf $RPM_BUILD_ROOT%{_webappconfdir}/apache.conf
install etc/ocsinventory/ocsinventory.conf $RPM_BUILD_ROOT%{_webappconfdir}/httpd.conf
install binutils/ipdiscover-util.pl $RPM_BUILD_ROOT%{_datadir}/%{name}/ipdiscover-util.pl

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
%doc README ocsreports/files/*.sql binutils/ocs-errors binutils/*.README PluginOcsOfficekey-2.2.4/*.txt PluginOcsOfficekey-2.2.4/msofficekey.vbs
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ocs-inventory-ng
%attr(750,root,http) %dir %{_webappconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webappconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webappconfdir}/httpd.conf
%{_datadir}/%{name}/
%dir %{perl_vendorlib}/Apache/Ocsinventory
%{perl_vendorlib}/Apache/Ocsinventory/*
%{perl_vendorlib}/Apache/Ocsinventory.pm
%attr(770,root,http) %dir %{_var}/log/%{name}
