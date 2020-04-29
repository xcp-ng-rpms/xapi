# -*- rpm-spec -*-

Summary: xapi - xen toolstack for XCP
Name:    xapi
Version: 1.160.2
Release: 1.3%{?dist}
Group:   System/Hypervisor
License: LGPL+linking exception
URL:  http://www.xen.org

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz
Source1: SOURCES/xapi/guefi
Source2: SOURCES/xapi/guefi.sh
Source3: SOURCES/xapi/guefi-secureboot
Source4: SOURCES/xapi/guefi-secureboot.sh


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1


# XCP-ng patches
Patch1000: xapi-1.160.1-allow-migrate_send-during-RPU.XCP-ng.patch
Patch1001: xapi-1.160.1-zstd-support.XCP-ng.patch
Patch1002: xapi-1.160.1-open-vxlan-port-for-sdn-controller.XCP-ng.patch
Patch1003: xapi-1.160.2-create-plugged-vif-and-vbd-and-suspended-vm.XCP-ng.patch
Patch1004: xapi-1.160.2-open-openflow-port.XCP-ng.patch

BuildRequires: ocaml-ocamldoc
BuildRequires: pam-devel
BuildRequires: xen-devel
BuildRequires: libffi-devel
BuildRequires: zlib-devel
BuildRequires: git
BuildRequires: gmp-devel
BuildRequires: libuuid-devel
BuildRequires: make
BuildRequires: python2-devel
BuildRequires: xs-opam-repo
BuildRequires: ocaml-xcp-idl-devel
BuildRequires: ocaml-xen-api-libs-transitional-devel
BuildRequires: forkexecd-devel
BuildRequires: message-switch-devel
BuildRequires: ocaml-rrdd-plugin-devel
BuildRequires: ocaml-netdev-devel
BuildRequires: ocaml-tapctl-devel
BuildRequires: systemd-devel
BuildRequires: pciutils-devel
BuildRequires: xen-dom0-libs-devel
BuildRequires: xenopsd-devel
%global _use_internal_dependency_generator 0
%global __requires_exclude *caml*
AutoReqProv: no

%description
XCP toolstack.

%if 0%{?coverage:1}
%package        cov
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: XAPI is built with coverage enabled
%description    cov
XAPI is built with coverage enabled
%files          cov
%endif

%package core
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: The xapi toolstack
Group: System/Hypervisor
%if 0%{?coverage:1}
Requires:       %{name}-cov = %{version}-%{release}
%endif
Requires: hwdata
Requires: redhat-lsb-core
Requires: stunnel_xs
Requires: vhd-tool
Requires: libffi
Requires: busybox
Requires: m2crypto
Requires: net-tools
Requires: vmss
Requires: python-six
Requires: python-pyudev
Requires: gmp
#Requires: xapi-storage-plugins
#Requires: xapi-clusterd
Requires: zstd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd

%description core
This package contains the xapi toolstack.

%package xe
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: The xapi toolstack CLI
Group: System/Hypervisor

%description xe
The command-line interface for controlling XCP hosts.

%package tests
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: Toolstack test programs
Group: System/Hypervisor
Requires: net-tools

%description tests
This package contains a series of simple regression tests.

%package client-devel
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: xapi Development Headers and Libraries
Group:   Development/Libraries
Requires: ocaml-xen-api-libs-transitional-devel
Requires: ocaml-xcp-idl-devel
Requires: xs-opam-repo

%description client-devel
This package contains the xapi development libraries and header files
for building addon tools.

%package datamodel-devel
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: xapi Datamodel headers and libraries
Group:   Development/Libraries
Requires: ocaml-xen-api-libs-transitional-devel
Requires: ocaml-xcp-idl-devel

%description datamodel-devel
This package contains the internal xapi datamodel as a library suitable
for writing additional code generators.


%package doc
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: Xen-API documentation
Group:   Development/Documentation

%description doc
This package contains Xen-API documentation in html format.

%prep
%autosetup -p1

%build
./configure %{?coverage:--enable-coverage}
ulimit -s 16384 && COMPILE_JAVA=no %{__make}
make doc

%check
COMPILE_JAVA=no %{__make} test
mkdir %{buildroot}/testresults
find . -name 'bisect*.out' -exec cp {} %{buildroot}/testresults/ \;
ls %{buildroot}/testresults/

%install
rm -rf %{buildroot}

DESTDIR=$RPM_BUILD_ROOT %{__make} install

SITEDIR=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
for f in XenAPI XenAPIPlugin inventory; do
	for e in py pyc pyo; do
		echo $SITEDIR/$f.$e
	done
done > core-files

ln -s /var/lib/xcp $RPM_BUILD_ROOT/var/xapi
mkdir $RPM_BUILD_ROOT/etc/xapi.conf.d
mkdir $RPM_BUILD_ROOT/etc/xcp

mkdir -p %{buildroot}/etc/xenserver/features.d
%{__install} -D -m 644 %{SOURCE1} %{buildroot}/etc/xenserver/features.d/guefi
%{__install} -D -m 755 %{SOURCE2} %{buildroot}/etc/xenserver/features.d/guefi.sh
%{__install} -D -m 644 %{SOURCE3} %{buildroot}/etc/xenserver/features.d/guefi-secureboot
%{__install} -D -m 755 %{SOURCE4} %{buildroot}/etc/xenserver/features.d/guefi-secureboot.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post core
%systemd_post cdrommon@.service
%systemd_post xapi-domains.service
%systemd_post perfmon.service
%systemd_post genptoken.service
%systemd_post xapi.service
%systemd_post attach-static-vdis.service
%systemd_post save-boot-info.service
%systemd_post mpathalert.service

%preun core
%systemd_preun cdrommon@.service
%systemd_preun xapi-domains.service
%systemd_preun perfmon.service
%systemd_preun xapi.service
%systemd_preun attach-static-vdis.service
%systemd_preun save-boot-info.service
%systemd_preun mpathalert.service

%postun core
%systemd_postun cdrommon@.service
%systemd_postun xapi-domains.service
%systemd_postun perfmon.service
%systemd_postun genptoken.service
%systemd_postun xapi.service
%systemd_postun attach-static-vdis.service
%systemd_postun save-boot-info.service
%systemd_postun mpathalert.service

%files core -f core-files
%defattr(-,root,root,-)
/opt/xensource/bin/xapi
%config(noreplace) /etc/xapi.conf
/etc/logrotate.d/audit
/etc/pam.d/xapi
/etc/cron.d/xapi-logrotate.cron
/etc/cron.daily/license-check
/opt/xensource/libexec/legacy-management-interface
/opt/xensource/libexec/xapi-init
/opt/xensource/libexec/xapissl
/opt/xensource/libexec/attach-static-vdis
/opt/xensource/libexec/save-boot-info
%config(noreplace) /etc/sysconfig/perfmon
%config(noreplace) /etc/sysconfig/xapi
/etc/xcp
/etc/xapi.conf.d
/etc/xapi.d/base-path
/etc/xapi.d/plugins/DRAC.py
/etc/xapi.d/plugins/DRAC.pyo
/etc/xapi.d/plugins/DRAC.pyc
/etc/xapi.d/plugins/echo
/etc/xapi.d/plugins/extauth-hook
/etc/xapi.d/plugins/extauth-hook-AD.py
/etc/xapi.d/plugins/extauth-hook-AD.pyo
/etc/xapi.d/plugins/extauth-hook-AD.pyc
/etc/xapi.d/plugins/firewall-port
/etc/xapi.d/plugins/iLO.py
/etc/xapi.d/plugins/iLO.pyo
/etc/xapi.d/plugins/iLO.pyc
/etc/xapi.d/plugins/iLOPowerON.xml
/etc/xapi.d/plugins/openvswitch-config-update
/etc/xapi.d/plugins/perfmon
/etc/xapi.d/plugins/power-on-host
/etc/xapi.d/plugins/wake-on-lan
/etc/xapi.d/plugins/wlan.py
/etc/xapi.d/plugins/wlan.pyo
/etc/xapi.d/plugins/wlan.pyc
/etc/xapi.d/plugins/iovirt
/etc/xapi.d/plugins/install-supp-pack
/etc/xapi.d/plugins/disk-space
/etc/xapi.d/efi-clone
/etc/xapi.d/extensions
/etc/xapi.d/mail-languages/en-US.json
/etc/xapi.d/mail-languages/zh-CN.json
/etc/xapi.d/mail-languages/ja-JP.json
%config(noreplace) /etc/xensource/xapi-logrotate.conf
%config(noreplace) /etc/xensource/db.conf
%config(noreplace) /etc/xensource/db.conf.rio
/etc/xensource/master.d/01-example
/etc/xensource/master.d/03-mpathalert-daemon
%config(noreplace) /etc/xensource/pool.conf
/opt/xensource/bin/fix_firewall.sh
/opt/xensource/bin/update-ca-bundle.sh
/opt/xensource/bin/mpathalert
/opt/xensource/bin/perfmon
/opt/xensource/bin/static-vdis
/opt/xensource/bin/xapi-autostart-vms
/opt/xensource/bin/xapi-db-process
/opt/xensource/bin/xapi-wait-init-complete
/opt/xensource/bin/xe-backup-metadata
/opt/xensource/bin/xe-edit-bootloader
/opt/xensource/bin/xe-get-network-backend
/opt/xensource/bin/xe-mount-iso-sr
/opt/xensource/bin/xe-restore-metadata
/opt/xensource/bin/xe-reset-networking
/opt/xensource/bin/xe-scsi-dev-map
/opt/xensource/bin/xe-set-iscsi-iqn
/opt/xensource/bin/xe-toolstack-restart
/opt/xensource/bin/xe-xentrace
/opt/xensource/bin/xe-switch-network-backend
/opt/xensource/bin/xe-enable-all-plugin-metrics
/opt/xensource/bin/xva-rewrite-scsiid
/opt/xensource/bin/xe-install-supplemental-pack
/opt/xensource/bin/hfx_filename
/opt/xensource/bin/pv2hvm
/opt/xensource/bin/xe-enable-ipv6
/etc/bash_completion.d/xe-switch-network-backend
/opt/xensource/bin/xsh
%attr(700, root, root) /opt/xensource/gpg
/etc/xensource/bugtool/xapi.xml
/etc/xensource/bugtool/xapi/stuff.xml
/etc/xensource/bugtool/xenopsd.xml
/etc/xensource/bugtool/xenopsd/stuff.xml
/opt/xensource/libexec/list_plugins
/opt/xensource/libexec/sm_diagnostics
/opt/xensource/libexec/xn_diagnostics
/opt/xensource/libexec/thread_diagnostics
/opt/xensource/libexec/InterfaceReconfigure.py
/opt/xensource/libexec/InterfaceReconfigure.pyo
/opt/xensource/libexec/InterfaceReconfigure.pyc
/opt/xensource/libexec/InterfaceReconfigureBridge.py
/opt/xensource/libexec/InterfaceReconfigureBridge.pyo
/opt/xensource/libexec/InterfaceReconfigureBridge.pyc
/opt/xensource/libexec/InterfaceReconfigureVswitch.py
/opt/xensource/libexec/InterfaceReconfigureVswitch.pyo
/opt/xensource/libexec/InterfaceReconfigureVswitch.pyc
/opt/xensource/libexec/backup-metadata-cron
/opt/xensource/libexec/backup-sr-metadata.py
/opt/xensource/libexec/backup-sr-metadata.pyo
/opt/xensource/libexec/backup-sr-metadata.pyc
/opt/xensource/libexec/block_device_io
/opt/xensource/libexec/cdrommon
/opt/xensource/libexec/daily-license-check
/opt/xensource/libexec/fence
/opt/xensource/libexec/generate_ssl_cert
/opt/xensource/libexec/host-backup
/opt/xensource/libexec/host-bugreport-upload
/opt/xensource/libexec/host-display
/opt/xensource/libexec/host-restore
/opt/xensource/libexec/interface-reconfigure
/opt/xensource/libexec/interface-visualise
/opt/xensource/libexec/link-vms-by-sr.py
/opt/xensource/libexec/link-vms-by-sr.pyo
/opt/xensource/libexec/link-vms-by-sr.pyc
/opt/xensource/libexec/logs-download
/opt/xensource/libexec/pbis-force-domain-leave
/opt/xensource/libexec/mail-alarm
/opt/xensource/libexec/nbd-firewall-config.sh
/opt/xensource/libexec/nbd_client_manager.py
/opt/xensource/libexec/nbd_client_manager.pyo
/opt/xensource/libexec/nbd_client_manager.pyc
/opt/xensource/libexec/print-custom-templates
/opt/xensource/libexec/probe-device-for-file
/opt/xensource/libexec/genptoken
/opt/xensource/libexec/restore-sr-metadata.py
/opt/xensource/libexec/restore-sr-metadata.pyo
/opt/xensource/libexec/restore-sr-metadata.pyc
/opt/xensource/libexec/set-hostname
/opt/xensource/libexec/shell.py
/opt/xensource/libexec/shell.pyo
/opt/xensource/libexec/shell.pyc
/opt/xensource/libexec/update-mh-info
/opt/xensource/libexec/upload-wrapper
/opt/xensource/libexec/xapi-health-check
/opt/xensource/libexec/xapi-logrotate.sh
/opt/xensource/libexec/xapi-rolling-upgrade
/opt/xensource/libexec/xha-lc
/opt/xensource/libexec/xe-syslog-reconfigure
/opt/xensource/libexec/usb_reset.py
/opt/xensource/libexec/usb_reset.pyo
/opt/xensource/libexec/usb_reset.pyc
/opt/xensource/libexec/usb_scan.py
/opt/xensource/libexec/usb_scan.pyo
/opt/xensource/libexec/usb_scan.pyc
/etc/xensource/usb-policy.conf
/opt/xensource/packages/post-install-scripts/debian-etch
/opt/xensource/packages/post-install-scripts/debug
/etc/xensource/udhcpd.skel
/opt/xensource/debug/rbac_static.csv
/etc/xapi.d/host-post-declare-dead/10resetvdis
/var/xapi
/opt/xensource/debug/debug_ha_query_liveset
/opt/xensource/debug/event_listen
/opt/xensource/debug/import-update-key
/opt/xensource/debug/vncproxy
/opt/xensource/debug/with-vdi
%{_unitdir}/cdrommon@.service
%{_unitdir}/xapi-domains.service
%{_unitdir}/perfmon.service
%{_unitdir}/genptoken.service
%{_unitdir}/xapi.service
%{_unitdir}/attach-static-vdis.service
%{_unitdir}/save-boot-info.service
%{_unitdir}/mpathalert.service
%config(noreplace) /etc/xenserver/features.d/guefi
%config(noreplace) /etc/xenserver/features.d/guefi-secureboot
/etc/xenserver/features.d/guefi.sh
/etc/xenserver/features.d/guefi-secureboot.sh

%files xe
%defattr(-,root,root,-)
/opt/xensource/bin/xe
/usr/bin/xe
/etc/bash_completion.d/xe

%files tests
%defattr(-,root,root,-)
/opt/xensource/debug/perftest
/opt/xensource/debug/quicktest
/opt/xensource/debug/quicktestbin

%global ocaml_dir /usr/lib/opamroot/ocaml-system
%global ocaml_libdir %{ocaml_dir}/lib
%global ocaml_docdir %{ocaml_dir}/doc

%files client-devel
%defattr(-,root,root,-)
%{ocaml_libdir}/xapi-types/*
%exclude %{ocaml_libdir}/xapi-types/*.cmt
%exclude %{ocaml_libdir}/xapi-types/*.cmti
%{ocaml_libdir}/xapi-consts/*
%exclude %{ocaml_libdir}/xapi-consts/*.cmt
%{ocaml_libdir}/xapi-client/*
%exclude %{ocaml_libdir}/xapi-client/*.cmt
%exclude %{ocaml_libdir}/xapi-client/*.cmti
%{ocaml_libdir}/xapi-cli-protocol/*
%exclude %{ocaml_libdir}/xapi-cli-protocol/*.cmt

%files datamodel-devel
%defattr(-,root,root,-)
%{ocaml_libdir}/xapi-database/*
%exclude %{ocaml_libdir}/xapi-database/*.cmt
%exclude %{ocaml_libdir}/xapi-database/*.cmti
%{ocaml_libdir}/xapi-datamodel/*
%exclude %{ocaml_libdir}/xapi-datamodel/*.cmt
%exclude %{ocaml_libdir}/xapi-datamodel/*.cmti

%files doc
%defattr(-,root,root,-)
%{_datarootdir}/xapi/doc/*
%exclude %{ocaml_docdir}/*

%if 0%{?coverage:1}
%package testresults
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api/archive?at=v1.160.2&format=tar.gz&prefix=xapi-1.160.2#/xen-api-1.160.2.tar.gz) = 5ba6c01e485c61eefb69e520e641a918653ee2d1
Summary: Coverage files from unit tests
%description testresults
Coverage files from unit tests

%files testresults
%defattr(-,root,root,-)
/testresults
%endif

%changelog
* Fri Apr 24 2020 Benjamin Reis <benjamin.reis@vates.fr> - 1.160.2-1.3
- Patch xapi-1.160.2-open-openflow-port.XCP-ng.patch added
- Open OpenFlow port when a SDN controller is set and close it when SDN controller is unset

* Mon Mar 30 2020 Benjamin Reis <benjamin.reis@vates.fr> - 1.160.2-1.2
- Patch xapi-1.160.2-create-suspended-vm.XCP-ng.patch delete
- Patch xapi-1.160.2-xapi-1.160.2-create-plugged-vif-and-vbd-and-suspended-vm.XCP-ng.patch added

* Tue Mar 17 2020 Benjamin Reis <benjamin.reis@vates.fr> - 1.160.2-1.1
- Patch xapi-1.160.2-create-suspended-vm.XCP-ng.patch added

* Fri Oct 18 2019 Igor Druzhinin <igor.druzhinin@citrix.com> - 1.160.2-1
- CA-314317: Protect PVS-cache get_or_recreate_vdi by mutex

* Tue Jun 25 2019 Benjamin Reis <benjamin.reis@vates.fr> - 1.160.1-1.2
- Patch xapi-1.160.1-open-vxlan-port-for-sdn-controller.XCP-ng.patch added

* Mon Apr 29 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 1.160.1-1.1
- New release for XCP-ng 8.0
- Rediff patch xapi-1.160.1-allow-migrate_send-during-RPU.XCP-ng.patch
- Rediff xapi-1.160.1-zstd-support.XCP-ng.patch re-applied
- Patch xapi-1.110.1-fix-SXM-from-pre-7.3-hosts.backport.patch dropped, since it is included in main sources
- Remove dependency to non-free packages again

* Thu Mar 21 2019 Edwin Török <edvin.torok@citrix.com> - 1.160.1-1
- CA-310173: remember multipath status with static vdi data

* Mon Mar 18 2019 Christian Lindig <christian.lindig@citrix.com> - 1.160.0-1
- CA-311705: Add VDI usage checking for metadata backup scripts

* Thu Mar 07 2019 Christian Lindig <christian.lindig@citrix.com> - 1.159.0-1
- CP-29134 Update versions for Naples release

* Tue Mar 05 2019 Christian Lindig <christian.lindig@citrix.com> - 1.158.0-1
- CA-311823: Do not raise alerts for "new CPU features"

* Mon Feb 25 2019 Christian Lindig <christian.lindig@citrix.com> - 1.157.0-1
- Revert "CA-290024: Reject booting pv-iommu VMs on a host where the premap is yet to complete"

* Mon Feb 25 2019 Christian Lindig <christian.lindig@citrix.com> - 1.156.0-1
- CA-310971: consider enabling the host again after plugging clustering PBDs
- CA-309815: add dependencies in perfmon.service

* Wed Feb 20 2019 Christian Lindig <christian.lindig@citrix.com> - 1.155.0-1
- CA-309048 handle domain sockets for wsproxy (#3816)

* Tue Feb 19 2019 Christian Lindig <christian.lindig@citrix.com> - 1.154.0-1
- CA-304473: lock the db before flush_and_exit on master

* Wed Feb 13 2019 Christian Lindig <christian.lindig@citrix.com> - 1.153.0-1
- CA-309809: avoid a stuck GFS2 mount by checking quorate state before PBD plug
- ocp-indent xapi-clustering.ml

* Wed Feb 06 2019 Rob Hoes <rob.hoes@citrix.com> - 1.152.0-1
- CP-29962: Ignore monitor_config_file for GVT-g VGPU types

* Tue Feb 05 2019 Christian Lindig <christian.lindig@citrix.com> - 1.151.0-1
- CP-30578: check if clustering required and wait for quorum
- Simplify .travis-xs-opam.sh

* Fri Feb 01 2019 Christian Lindig <christian.lindig@citrix.com> - 1.150.0-1
- CP-30527: use Memory for unit conversions
- CP-30527: Gather Xen capabilities from xenopsd
- CP-30527: Fetch Xen version from xenopsd
- CP-30527: Remove Xenctrl check when reading host memory
- CP-30527: Constrict usage of xenopsd to gather host info

* Tue Jan 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.149.0-1
- CP-30508: Reliably detect IOMMU presence in host

* Wed Jan 23 2019 Christian Lindig <christian.lindig@citrix.com> - 1.148.0-1
- Prepare for Dune 1.6
- Makefile: remove OPAM_PREFIX, OPAM_LIBDIR

* Tue Jan 22 2019 Christian Lindig <christian.lindig@citrix.com> - 1.147.0-1
- CA-307829: XSI-216 Add active state in update_vgpu
- CA-272180: report suspend ack failures on API
- CA-272180: report suspend timeouts on API
- Replaced jbuild files with dune.

* Wed Jan 09 2019 Christian Lindig <christian.lindig@citrix.com> - 1.146.0-1
- CP-29673: allow checkpoint op for VM with vgpu
- CA-302456: Do not clear 'resident_on' during a checkpoint operation
- CA-304576: Allow checkpoint on suspended VM with Nvidia vGPU
- CA-307012: Avoid checking power_state for checkpoint while creating VGPU.

* Mon Jan 07 2019 Christian Lindig <christian.lindig@citrix.com> - 1.145.0-1
- CA-300719: Block export >2TB VDI to VHD format

* Wed Jan 02 2019 Christian Lindig <christian.lindig@citrix.com> - 1.144.0-1
- Use sets not lists

* Tue Dec 18 2018 Christian Lindig <christian.lindig@citrix.com> - 1.143.0-1
- CP-28659, CP-28662: Add VM.NVRAM field
- CP-28662: send NVRAM to xenopsd
- CP-29070: prevent changes to NVRAM while the VM is running
- CP-29420: read_record_internal: avoid intermediate lists and deep call stacks
- CP-29420: finer grained locking for xenopsd metadata
- CP-29169: call varstore-rm on UEFI VM clone
- CP-28675: Add a VM_SECURE_BOOT_FAILED message type
- CP-29857: forbid qemu-upstream-uefi device-model on Bios
- CP-29857: defer setting device-model until first VM.start
- CP-29857: do not reject qemu-upstream-uefi for vUSB
- CP-29936: override control/feature-suspend if data/cant_suspend_reason is set
- CP-29967: add varstored-guard to xe-toolstack-restart
- CP-30032: spawn varstore-rm in a chroot (#3782)
- CP-29002: add unit test for VM.NVRAM field

* Fri Dec 14 2018 Christian Lindig <christian.lindig@citrix.com> - 1.142.0-1
- Remove some unused binaries, tests, and values
- CA-281176: hide deprecated VDI operations from the allowed_operations field

* Tue Dec 11 2018 Patrick Fox <patrick.fox@citrix.com> - 1.140.0-uefi
- Add guefi feature flag

* Mon Dec 10 2018 Christian Lindig <christian.lindig@citrix.com> - 1.141.0-1
- Use dune and define profile "gprof" for profiling

* Tue Dec 04 2018 Christian Lindig <christian.lindig@citrix.com> - 1.140.0-1
- CA-300644: return immediately when attach-static-vdis failed
- Reference xapi-inventory instead of xcp-inventory; the latter is being deprecated.
- Reference xapi-idl instead of xcp; the latter is being deprecated.

* Fri Nov 30 2018 Christian Lindig <christian.lindig@citrix.com> - 1.139.0-1
- Revert "CP-28951: Add message of xen low memory alarm"
- CA-302538: Disallow restore across partition layout changes

* Wed Nov 28 2018 Christian Lindig <christian.lindig@citrix.com> - 1.138.0-1
- CP-29757: block SXM of encrypted VDIs
- CP-29757: Add new VDI_IS_ENCRYPTED exception

* Tue Nov 27 2018 Christian Lindig <christian.lindig@citrix.com> - 1.137.0-1
- CP-30039: Generate automatically the release and class files for 
  the xapi project docs; added release date to the releases.
- Use lowercase for class filenames.
- Improved field doc so we don't need extra doc notes for it i
  on xapi-project.github.io
- CA-298465: Only try to detach locally attached updates when booting
- Added some historical data.
- CA-299554 XSI-132 use correct vCPU count for dom0

* Thu Nov 22 2018 Christian Lindig <christian.lindig@citrix.com> - 1.136.0-1
- CA-300103 designate a single Tools SR, delete others

* Fri Nov 16 2018 Christian Lindig <christian.lindig@citrix.com> - 1.135.0-1
- New ocaml-rpc

* Fri Nov 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.134.0-1
- CA-290024: Reject booting pv-iommu VMs on a host where the 
  premap is yet to complete

* Tue Nov 06 2018 Christian Lindig <christian.lindig@citrix.com> - 1.133.0-1
- Restored mustache in the dependencies of xapi-datamodel as it 
  is needed for doc generation.
- XSO-244/CA-168413: Show minimum role per message in the API reference markdown.
- CA-294900 remove network_sriov on network reset
- CA-302194 XSI-87 apply guest agent config on start

* Wed Oct 31 2018 Christian Lindig <christian.lindig@citrix.com> - 1.132.0-1
- Update opam files for Opam 2 (#3752)

* Mon Oct 29 2018 Christian Lindig <christian.lindig@citrix.com> - 1.131.0-1
- CA-300115 lower VM.assert_operation_valid permissions

* Wed Oct 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.130.0-1
- CA-297137: Don't update current_domain_type if xenopsd returns undefined
- CA-300715: Use Dup fd to avoid close twice.
- Increase VDI size for metadata backups.

* Mon Oct 22 2018 Christian Lindig <christian.lindig@citrix.com> - 1.129.0-1
- CA-299944: Proxy requests to updates
- CA-300210: Add 'CIPHER_SERVER_PREFERENCE' option in xapi ssl config
- CP-29687: Remove TLS_RSA_WITH_AES_128_CBC_SHA(AES128-SHA) for CC
- Cleanup Context module a little
- Eliminate redundant Context.task_in_database field
- Encode difference between real and dummy tasks in Ref.t type
- Move Context.get_task_name to TaskHelper.get_name
- Move Helpers.short_string_of_ref to Ref.short_string_of
- Remove confusing "forwarded task destroyed" log lines
- Remove dead code from Context module
- Remove unused __context arg from Context constructors
- Remove unused Context.string_of
- Remove unused Server.dispatch function

* Thu Oct 18 2018 Edwin Török <edvin.torok@citrix.com> - 1.128.0-1
- Add quicktests for 2GB vdi TAR import export
- CP-29605 CP-29604: Query sparseness of VDIs during TAR export
- Use opam2 container in travis
- CA-297297 Make create_row idempotent
- Wrap entire function in lock
- Use opam2 container in travis
- Make code non quadratic, Fix style and comments
- CA-297343: Use transform_xenops_exn in pool_migrate
- Address latest review comments

* Thu Oct 11 2018 Rob Hoes <rob.hoes@citrix.com> - 1.127.0-1
- CP-28301: validate and send HVM-boot-params["firmware"] to xenopsd
- CP-28659: Add VM.NVRAM field
- CP-28662: send NVRAM to xenopsd
- CP-28662: use record instead of string map for NVRAM
- CP-28662: do not display NVRAM by default
- CP-29070: introduce VM.set_NVRAM_EFI_variables for varstored
- CP-29070: prevent changes to NVRAM while the VM is running
- CA-299371: mark NVRAM as hidden by default
- CP-29196: Enable FIPS mode if existence of cc preparations (#3722)
- CP-29696: Change the order of cipher base on latest requirement

* Tue Oct 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.126.0-1
- CP-29521: VDI import/export in TAR format

* Thu Oct 04 2018 Christian Lindig <christian.lindig@citrix.com> - 1.125.0-1
- CA-297520: Ensure we can always turn exceptions into at least internal errors
- Reduce number of DB calls when resynchronising PIF params
- Set PIF.capabilities for physical PIFs only
- The MTU of a bond slave comes from its master's bridge
- Remove spammy log line in xapi_pif_helpers.ml
- Remove unnecessary call to xcp-networkd
- Confirm that the interface exists before querying IP configuration
- Improve update_getty

* Mon Oct 01 2018 Christian Lindig <christian.lindig@citrix.com> - 1.124.0-1
- CP-28923: Add sm capability for large and thinly provisioned VDIs
- CP-28951: Add message of xen low memory alarm
- Move implementations_of_backend to xcp-idl

* Wed Sep 26 2018 Christian Lindig <christian.lindig@citrix.com> - 1.123.0-1
- CA-290696: Update task to un-cancellable after xenopsd notify xapi (#3696)
- XSO-886: Do not add micro version to the pv_drivers_version if
  the latter is empty.
- CA-298318: Set the SM name_label correctly

* Mon Sep 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.122.0-1
- CP-27110: Use PPX storage interface
- CP-27110: Use opaque VDI and SR types

* Wed Sep 19 2018 Christian Lindig <christian.lindig@citrix.com> - 1.121.0-1
- CP-29084: Rebranding XenServer to Citrix Hypervisor in Toolstack.

* Tue Sep 18 2018 Christian Lindig <christian.lindig@citrix.com> - 1.120.0-1
- Revert "Workaround for NVIDIA-130"
- CA-293417: pool_update_download_handler: include Content-Type in HTTP response
- CA-293417: unit test for path verification in /update/ handler
- CA-293417: fix path verification in /update/ handler

* Mon Sep 17 2018 Rob Hoes <rob.hoes@citrix.com> - 1.119.0-2
- Remove CA-293417 patch

* Mon Sep 17 2018 Christian Lindig <christian.lindig@citrix.com> - 1.119.0-1
- Refine the format of generated db_actions code
- CP-29389: Delete duplicate function 'parse_device_config'
- Remove patch for "* Workaround for NVIDIA-130"

* Fri Sep 14 2018 Christian Lindig <christian.lindig@citrix.com> - 1.118.0-2
- move NVIDIA patch to source code repository

* Wed Sep 12 2018 Christian Lindig <christian.lindig@citrix.com> - 1.118.0-1
- CA-293678 SXM in partially upgraded pool with pre-7.3 hosts fails
- Update opam files

* Tue Sep 11 2018 Christian Lindig <christian.lindig@citrix.com> - 1.117.0-1
- Reduce amount of log messages when importing

* Wed Sep 05 2018 Christian Lindig <christian.lindig@citrix.com> - 1.116.0-1
- CA-293085: Stop xapi-nbd before eject
- CA-291569: Change config for stunnel
- CP-29015: Set correct ciphers for stunnel server
- CA-295828: set 'fips = no' for both ssl-legacy mode and non-legacy mode
- CA-296204: Reduce stunnel RSA key length to 2048- Use PPX Xenops interface
- database/jbuild: link only ppx_sexp_conv.runtime-lib


* Fri Aug 31 2018 Christian Lindig <christian.lindig@citrix.com> - 1.115.0-1
- CA-289625: Use jemalloc

* Tue Aug 28 2018 Christian Lindig <christian.lindig@citrix.com> - 1.114.0-1
- Simplify PPX processing in jbuild files

* Tue Aug 21 2018 Christian Lindig <christian.lindig@citrix.com> - 1.113.0-1
- CA-294874 xe-toolstack-restart reformat
- CA-294874 xe-toolstack-restart: add message-switch
- Update to newer interface requirements of Task_server
- Add opam dependency on ctypes

* Mon Aug 13 2018 Christian Lindig <christian.lindig@citrix.com> - 1.112.0-1
- Bumped the minor api version as well as the client min and max version numbers to 2.11.
- CA-294917: Added branding to the lima release.

* Mon Aug 06 2018 Christian Lindig <christian.lindig@citrix.com> - 1.110.1-1
- Bumped the minor api version as well as the client min and max version 
  numbers to 2.11.
- CA-294917: Added branding to the lima release.

* Thu Aug 02 2018 Rob Hoes <rob.hoes@citrix.com> - 1.111.0-2
- Added CA-293417 patch

* Wed Aug 01 2018 Christian Lindig <christian.lindig@citrix.com> - 1.111.0-1
- CP-28116: reintroduce VM quicktests
- CA-286723: Replace timeboxed api call with a better solution

* Mon Jul 30 2018 Christian Lindig <christian.lindig@citrix.com> - 1.110.0-1
- CA-294281: Network reset: warn if networkd.db could not be deleted
- CA-293399: Corrupted PCI information in xapi database
- CP-28936: Assert that a host has enough pCPUs to run a VM

* Wed Jul 25 2018 Christian Lindig <christian.lindig@citrix.com> - 1.109.0-1
- xapi.opam: remove unused nbd dependency
- CA-293399: Ensure we don't allow invalid utf8 strings into the db
- CA-294281: Network reset: warn if networkd.db could not be deleted
- CA-293399: Corrupted PCI information in xapi database

* Thu Jul 19 2018 Thomas Mckelvey <thomas.mckelvey@citrix.com> - 1.108.0-2
- CP-28711: Get rid of corosync feature flag

* Wed Jul 18 2018 Christian Lindig <christian.lindig@citrix.com> - 1.108.0-1
- CA-293858: Further prevention of logrotate running on old partition scheme
- CA-289997: Add a test for Xapi_vdi.update_allowed_operations
- CA-289997: Fix allowed_operations when VBDs are attached

* Fri Jul 13 2018 Christian Lindig <christian.lindig@citrix.com> - 1.107.0-1
- CA-289650: Wait for the pidfile from udhcpd before releasing lock
- CA-289898: GC dangling references from 'Host.updates_requiring_reboot'
- CA-290840: VM.attached_PCIs field not properly cleanup when reverting 
             from snapshot
- CA-291017: Unable to connect server in pool of 64 physical hosts
- CA-292676: Apply 'VDI missing' logic to picking SRs too
- CA-292676: Filter out missing VDIs when looking for some to use
- CA-293786: Cluster.get_network should not be restricted to pool admin
- CP-28753: drop unused CLUSTER_HOST_CREATION_FAILED message
- CP-28844: Allow pool operator to perform clustering operations

* Wed Jul 11 2018 Christian Lindig <christian.lindig@citrix.com> - 1.106.0-1
- CA-287525 replace OPasswd with implementation in C

* Tue Jul 10 2018 Christian Lindig <christian.lindig@citrix.com> - 1.105.0-1
- CA-289735: do not disable clustering daemon on shutdown from xapi-domains
- CA-292063: detach static VDIs when HA is disarmed on boot
- CP-27694: fail with NOT_IMPLEMENTED if there is no clustering daemon available
- CP-27915: test that VBD.create isn't allowed for cbt_metadata VDI
- CP-28753: add CLUSTER_HOST_FENCING message
- CP-28753: always detach all static VDIs
- Quicktest to run VDI ops on empty VDI with max supported size

* Tue Jul 03 2018 Christian Lindig <christian.lindig@citrix.com> - 1.104.0-1
- CA-292621: ensure PIF has an IP before calling clustering methods
- CA-292432: Add quicktest for static-vdis script

* Thu Jun 28 2018 Christian Lindig <christian.lindig@citrix.com> - 1.103.0-1
- Merge of GFS2 and QEMU upstream features
- CP-28561: Cluster.get_network fails if cluster_hosts lack common network
- CP-28561: Test Cluster.get_network
- CA-289996: Should declare VMs with SR-IOV VFs non-agile for HA purposes
- CA-292372: Create SM objects for all running SMAPIv2 drivers
- CP-28132: Implement & move to VDI.attach2 SMAPIv2 call, deprecate VDI.attach
- CP-28132: Storage_migrate.with_activated_disk: use finally to detach VDI
- CP-28132: attach now directly returns the xenstore directory
- CP-28132: update static-vdis script after attach changes
- CP-28132: remove domain_uuid from attach response
- CP-27560 set device model default to "qemu-upstream-compat"
- CP-27560 ensure device model is qemu-upstream-compat
- CP-27560 during xapi upgrade, upgrade VM device model
- CP-27560 increment database version
- CA-290006 update snapshot device model profile
- Remove unnecessary reference of Api_errors

* Tue Jun 26 2018 Christian Lindig <christian.lindig@citrix.com> - 1.102.0-1
- CP-28477: Cluster_host.force_destroy ignores exn
- CP-28477: Cluster_host.forget deletes cluster_host if successful
- CP-28477, CP-26179: Forward Cluster.destroy, pool_destroy works without
- XOP-948: Add a test for restricting SR allowed_operations during RPU
- XOP-948: Restrict SR allowed_operations during RPU
- CP-28227: Add API errors to clustering datamodel
- CP-28477, CP-26179: make the info message more clear
- Remove obsolete clustering quicktest
- Generalize quicktest filtering

* Wed Jun 20 2018 Stefano Panella <stefano.panella@citrix.com> - 1.101.0-2
- Enable GFS2 feature flag

* Tue Jun 19 2018 Christian Lindig <christian.lindig@citrix.com> - 1.101.0-1
- CP-28117: restart HA VMs in parallel when recovering from host failure

* Fri Jun 15 2018 Christian Lindig <christian.lindig@citrix.com> - 1.100.0-1
- CA-287838: Slave Dom0 becomes incorrect state in DB after pool join
- CA-290450: quicktest_vdi_ops_data_integrity: test large VDIs too
- CA-290466: Add quicktest to test parallel VDI dom0 attach limit
- CA-272147: add quicktest for SR.set_name_label & description
- CA-291136: skip hosts which do not have an IP address yet
- CA-291136: wait for carrier on management interface
- CA-291164: avoid race condition in waiting for management IP address
- CA-291163: avoid race condition on waiting for clustering IP
- CA-290526: Update location for cluster stack supported SRs file (#3631)
- merge safe-string patches: all strings are now immutable
- nbd_client_manager: increase number of /dev/nbds and wait for a free one
- drop debug/graph: not built anymore
- remove legacy graph and rfb ocaml libraries
- test/test_pool_license: reduce deprecation warnings

* Thu Jun 14 2018 Cheng Zhang<cheng.zhang@citrix.com> - 1.99.0-4
- Remove experimental flag of SRIoV feature

* Mon Jun 11 2018 Christian Lindig <christian.lindig@citrix.com> - 1.99.0-1
- Merge GFS2 branch: 
  CP-24692 CP-25121 CP-26147 CP-25121 CP-25121 CP-25121 CP-25121 CP-26199
  CP-26912 CP-26912 CP-26912 CP-26912 CP-26912 CP-26912 CP-26912 CP-27172
  CP-27172 CP-27466 CP-28213 CP-28213 CP-28406 CP-28406 CP-28406 CP-28406
- CA-290237: Add Cluster_host.joined field to represent cluster membership
- CA-290237: Prevent data races blocking pool-join on bonds and VLANs
- CA-290237: Wait for clustering IP before resyncing host
- CA-290471: fix wrong token timeout in XenCenter (#3611)
- CA-290686: fix forwarding of Cluster_host.forget
- CA-290891: Add quicktest for VDI export & import
- Hardcode token value thresholds in Constants module
- Test Cluster.create fails for invalid token parameters

* Tue Jun 05 2018 Christian Lindig <christian.lindig@citrix.com> - 1.98.0-1
- CA-289623: Added missing branding; removed duplicate comment.
- Rename Xapi_vm_snapshot.default_values to overrides
- CA-290874: Always derive domain_type from HVM_boot_policy on VM.revert
- CA-290874: On start and resume, always ensure that the domain type is set

* Thu May 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.97.0-1
- CA-289319: Kolkata Update application failure: HANDLE_INVALID
- CA-289907: Base pool.cpu_info:features_hvm on HVM-capable hosts only
- CA-289907: Update pool_cpu_features unit test
- CA-275120: XenAPI methods only callable by SM are publicly visible
- XSI-6: Corrected and completed event class documentation enhancements.
- Quicktest: add support for comparing record fields
- Quicktest: check snapshot VDI fields
- Moved the output of gen_json.ml into the _build folder.
- Removed obsolete docbook and pdf format of the API Reference.
- Split API Reference into two files, one for classes and types and 
  one for error handling.
- xapi-database: make safe-string compliant
- xapi-types: make safe-string compliant

* Fri May 18 2018 Christian Lindig <christian.lindig@citrix.com> - 1.96.0-1
- pci/lib_test: disable tests until we move back to upstream library
- travis-python-nosetests: fix tests

* Mon May 14 2018 Christian Lindig <christian.lindig@citrix.com> - 1.95.0-1
- CP-27911: Port tests to Alcotest
- CP-27899: Convert quicktests to Alcotest

* Thu May 10 2018 Christian Lindig <christian.lindig@citrix.com> - 1.94.0-1
- CA-287921: nbd_client_manager: track nbd device -> nbd server mapping
- CA-289140: log the exception from PBD plug without doing other API calls
- CA-289140: ignore missing PBDs on startup
- CA-289620: Remove redundant log of events_watch
- CP-27911: Port test_host_helpers to Alcotest
- CP-27911: Port test_xapi_xenops to Alcotest
- CP-27911: Port test_sr_update_vdis to Alcotest
- CP-27911: Port test_bond to Alcotest
- CP-27911: Port test_tunnel to Alcotest
- CP-27911: Port test_pvs_server to Alcotest
- CP-27911: Port test_xapi_vbd_helpers to Alcotest
- CP-27911: Port test_network_sriov to Alcotest
- CP-26583: Upgrade Xapi to use PPX-based Rrdd idl
- CP-26583: Update error: Rrd_failure -> Rrdd_internal_error
- Speed up update_all_allowed_operations: VDI
- Add randomized quicktest to check VDI.copy data integrity
- quicktest_vdi_copy_data_integrity: write random bytes from urandom

* Wed May 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.93.0-3
- Make SRIOV an experimental feature (off by default)

* Tue May 01 2018 Christian Lindig <christian.lindig@citrix.com> - 1.93.0-1
- CA-273986: Add test for Cluster.create cleanup
- CA-284520: Adding pool pre-check for clustering enabled
- CA-288411: make the cache work after a toolstack restart
- cli_protocol.ml: replace deprecated use of String.set with Bytes
- rfb_randomtest.ml: replace deprecated use of String.set
- gen_rbac.ml: replace deprecated use of String.set
- tasks.ml: add missing ignore
- cli_progress_bar.ml: replace deprecated use of String.set
- record_util.ml: use String.lowercase_ascii
- sparse_encoding.ml: replace deprecated use of String.set
- extauth_plugin_ADpbis.ml: replace deprecated use of String.set
- storage_mux.ml: replace use of deprecated Stdext.Fun.++
- rbac_audit.ml: replace use of deprecated String.set
- xapi_sm.ml: replace use of deprecated Stdext.Fun.++
- xapi_pif.ml: replace use of deprecated Stdext.Fun.id
- nbd_client_manager: provide error message for exceptions
- CA-288394: nbd_client_manager: add program name to log lines
- nbd_client_manager: extract program into main method
- CP-27880: drop incorrect all-zero diagnostic counters and deprecate diagnostic-db-log
- CP-27880: collect timing, db and net statistics in bugtools
- CP-27880: move Stats to xapi-database
- CP-27880: collect timing stats from redo_log
- CA-288635: redo_log: only log WriteField if the value actually changed
- CA-288635: block_device_io: reduce number of O_DSYNC writes to half in action_write_delta
- CA-288635: increase db flush chunk size

* Mon Apr 23 2018 Christian Lindig <christian.lindig@citrix.com> - 1.92.0-1
- CA-267687: Logs of VBD operation check that inspects operations of 
  VBD's VDI do not match returned errors
- XSI-6: Event class documentation enhancements.
- CA-287865: Forwarded task calling Message_forwarding.xxx resulting 
  current task being early marked completed
- CA-286874: Redundant checks for SR-IOV when implementing VDI migration (#3547)
- CA-287854: Add cluster stack constants and check cluster stack valid for
- CA-287854: Test Cluster.create fails with invalid cluster stack
- CA-286165: Only non-VF PCI need to update dependencies
- CA-287863: Reorgnize the code
- CA-287863: xe vm-shutdown complete the task too early
- CA-287929: fix incorrect log message (11428 > 11428)
- CA-281638: Set pool.ha_cluster_stacks upon Cluster.create/destroy success, 
  not on Cluster_host operations
- CA-281638: Add tests for Pool.ha_cluster_stack selection
- CA-287343: Update HA failure tolerance plan for corosync/GFS2 and 
  add unit tests
- CA-244573: Storage migration state lost after xapi restarting
- CA-244573: XenMotion fails after previously attempted SXM is
  interrupted by XAPI restart and vm goes into suspended state
- CA-288347: Do not take clustering lock in SR.probe
- CA-288312: Don't update HOSTNAME in /etc/sysconfig/network
- ocp-indent cluster_stack_constraints and test_cluster(ing)
- xapi_services.ml: use Re.Emacs instead of the deprecated Re_emacs
- xa_auth_stubs: add missing header file
- Network_event_loop: make sure no duplicated interfaces are 
  passed to firewall script
- Improve documentation: Cannot is one word.
- Remove deleted quicktests from all_tests list
- Remove quicktest_encodings
- Move quicktest_vm_placement from quicktests to unit tests
- Move quicktest_vm_memory_constraints from quicktests to unit tests
- Convert Test_network_event_loop to alcotest
- Port Test_event to Alcotest
- Port test_network to Alcotest
- Port test_pgpu to Alcotest
- Port test_xapi_db_upgrade to Alcotest
- Port test_pci_helpers to Alcotest
- Port test_pool_db_backup to Alcotest
- Port test_pool_restore_database to Alcotest
- Port test_workload_balancing to Alcotest

* Wed Apr 11 2018 Christian Lindig <christian.lindig@citrix.com> - 1.91.0-1
- CA-286338: Inter-host VM copy failed from source host to a slave in a pool
- CP-27544: Log cluster/host opaquerefs for message forwarding
- CP-27544: Add debug info to Cluster calls
- CP-27544: Add logging for success/failure of cluster_host API calls
- CP-27544: Move debug line to prevent duplication
- CP-27544: Convert clustering code failures to internal_errors
- CP-27544: Errors report opaquerefs instead of UUIDs
- CP-27544: Pattern-match for empty list in clustering code
- CP-27544: Specify whether no cluster_host is found or none match in
- CA-287503: fix static-vdis for SMAPIv3
- CA-285840: Check for host liveness in the new stunnel hook
- Hyphenate xe clustering params instead of using underscores

* Thu Apr 05 2018 Christian Lindig <christian.lindig@citrix.com> - 1.90.0-1
- CA-286364: When creating guest_metrics, ensure all fields reflect current state
- CP-27346: Add SR.probe_ext
- Bump database schema version
- Add option type to datamodel
- Add SR UUID to SR.probe return type
- CP-27140: Fix result parsing of SR.probe quicktest
- CP-27343: SR probe: add clustering lock, assert cluster_host enabled (#3542)

* Wed Apr 04 2018 Marcello Seri <marcello.seri@citrix.com> - 1.89.0-2
- Update SPEC file to get rid of rpmbuild warnings

* Wed Apr 04 2018 Christian Lindig <christian.lindig@citrix.com> - 1.89.0-1
- Port Test_clustering and Test_clustering_allowed_operations to Alcotest
- CA-268511: Prevent live PIF unplugging when clustering is enabled
- CA-285605: Make PIF.set_disallow_unplug idempotent
- CA-285605: Update tests for idempotent PIF.set_disallow_unplug
- CA-285605: Do nothing if value is the same
- CA-282006: Prevent IP reconfiguration on a live cluster network
- CA-282006: Update PIF.{forget, reconfigure_ip(v4,v6)} declarations in datamodel with new errors
- CA-282006: Add quicktest to check clustering assertions prevent IP reconfiguring
- CA-285349: Replace only-sr-name flag with use-default-sr
- CA-285349: Split  into two internal functions to unplug PBDs, then disable clustering
- CA-285349: Move disable_clustering from Xapi_pbd.ml to Xapi_cluster_host.{ml, mli}
- CA-285349: Introduce API errors cluster_stack_in_use, pif_allows_unplug
- CA-285349: Change errors raised, refactor required_cluster_stack assertion
- CA-285349: Update unit test with new error
- CA-280423: Open/close xapi-clusterd port when starting/stopping daemon (#3509)
- CA-286294: Add function to individually resync a host to its cluster objects
- CA-286294: Move Xapi_cluster.pool_resync logic to Xapi_cluster_host.resync_host
- CA-286294: PBD.plug individually resyncs hosts instead of the entire pool
- Start/stop nbd-client for qemu datapath using a new script
- CP-26169: Prevent turning on clustering when HA is enabled
- CA-285281: Make SR.probe quicktest idempotent
- Add backwards-compatible SR.probe output for SMAPIv3
- SR.probe never returns a Probe anymore
- Add SR UUID to SR.probe return type
- Inline Xmlm_tree into where it's used
- CA-281638: Set Pool.ha_cluster_stack when enabling/disabling clustering

* Tue Apr 03 2018 Christian Lindig <christian.lindig@citrix.com> - 1.88.0-1
- CA-275591: remove dead code
- CA-282684: VDI migration with vGPU is failing when vGPU size is big (#3540)

* Wed Mar 28 2018 Christian Lindig <christian.lindig@citrix.com> - 1.87.0-1
- CP-24805: permit other defaults when ensuring device-model profile in platform
- CP-24805: set the default VM.platform device-model profile during upgrade
- CP-24805: add the fallback device-model profiles for each qemu-upstream stage
- CP-24805: use the proper 'fallback' terminology present in the design
- CP-24805: trigger db upgrade based on Jura version
- CP-25713: update usb_reset to work with deprivileged QEMU
- CA-285511: TCUSBPassBetweenVMWithinPool: No route to host
- CP-27452: save/restore uid/gid of device file

* Wed Mar 28 2018 Christian Lindig <christian.lindig@citrix.com> - 1.86.0-1
- Fix typo of `modprobe`
- CA-260638 Bonds are created on interfaces which participates in FCoE
- CA-285596: Suppress host.set_iscsi_iqn during RPU

* Thu Mar 22 2018 Marcello Seri <marcello.seri@citrix.com> - 1.85.0-1
- CP-25797 Add network SR-IOV model
- CP-23644: Add network sriov as a feature
- CP-26302: Add driver_name in PCI object
- CP-26333 Add PIF.PCI field
- CP-26430:fix autocompletion error of network-sriov
- CP:26014:Set reserved_pci to Ref.null when vm halted.
- refine based on Lindig's comments
- Clarify function comments based on Marcello's comments
- Temporary fix to make xapi a sucessful build (#3427)
- CP-25699 Refine PIF type check related stuff
- Code refine
- CP-25699 Network sriov create/destroy
- CP-25699 call networkd when enable/disable sriov
- CP-25699 Add UT for vlan/bond/tunnel/network_sriov
- CP-25795: Support network SR-IOV VF backed vif.
- CP-25795: Add PCIs of network SR-IOV VFs into metadata.
- CP-25795: Enhance backend_of_network function.
- Fix indentation
- CP-26857: Blocking 'forget' on SR-IOV logical PIF
- Remove vlan-on-vlan support
- CP-27001 Update pci status after enable/disable sriov
- Move function `is_device_underneath_same_type` to new place
- Rename exception `network_is_not_sriov_compatible` to `network_incompatible_with_sriov`
- CP-26627 Isolate sriov/sriov vlan network from other network
- Add unit test for vlan/bond/tunnel
- Rename and move `assert_sriov_pif_compatible_with_network` to `assert_network_compatible_with_sriov`
- CP-26148: Function for Network SR-IOV get free capacity
- CP-25811: Update host selection and resource reservation for VM with SR-IOV VIFs
- CP-26606: Unit tests for choose host with SR-IOV
- CP-26608: Disallow SR-IOV VIF plug/unplug
- CP-23782: Add license restriction for VF usage
- CP-27201 Add network sriov precheck for pool join
- CP-27201 Sync network sriov from master to slave when slave restarting
- CP-27201 Best effort bring up sriov logical PIFs when xapi start
- CP-27201 Gc sriovs when gcing PIFs
- CP-27201 refine `sync_vlans` and `sync_tunnels`
- CP-27329: Make Network SR-IOV Sync Do Plug on Slave
- CP-27381: Auto-plug SR-IOV physical PIF
- CP-27381: Auto-unplug SR-IOV logical PIF
- CP-23788: VM guest metrics can read SR-IOV VF IPs
- CP-23788: Add unitest for VM guest metrics to read SR-IOV VF IPs
- CP-27381: Make "SRIOV" in debug message consistent as upper case
- CP-27272: Restore lost codes in merge commit
- Fix for VM without SR-IOV VIF start failed
- CA-285897: Filter out un-attached VF-backed vifs in PCI metadata
- CA-280342: Bad error message when migration fails
- CP-27446: Change the way for getting SR-IOV object from PIF when group
- CA-286292: VLAN PIF on SR-IOV status is incorrect after restarting
- CA-286135: Bring up bond when bring up SR-IOV physical
- CA-281178: Update allowed operations in consider_enabling_host
- CA-286135: Bring down SR-IOV physical PIF when bring down bond

* Wed Mar 21 2018 Christian Lindig <christian.lindig@citrix.com> - 1.84.0-1
- CP-27433 remove checks for vgpu_migration_enabled()

* Thu Mar 15 2018 Christian Lindig <christian.lindig@citrix.com> - 1.83.0-2
- CP-27433 remove vgpu_migration feature flag - it is now on by default

* Thu Mar 15 2018 Christian Lindig <christian.lindig@citrix.com> - 1.83.0-1
- CA-284492: Ignore vGPU live-migratability in migrate_send for halted VMs

* Thu Mar 15 2018 Christian Lindig <christian.lindig@citrix.com> - 1.82.0-1
- remove Legacy module
- datamodel_values: remove unused to_xml
- idl: revert datamodel_values to_rpc change and use to_ocaml_string instead
- datamodel_values: correctly stringify numbers also when they are negative
- gen_api: prevent default values for VCustom fields, these may contain 
  code that break the unmarshaller
- gen_api, datamodel_values: get defaults for VCustoms suitable for the API generator
- database: simplify types after removing bigbuffer
- importexport: use Rpc.to_string instead of Jsonrpc.to_string
- Port test to Aloctest
- Fix typo in VLAN test
- database: resurrect db_cache_test
- db_rpc_common_v2: completely remove Read_set_ref
- Eliminate fd leak in timebox

* Fri Mar 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.81.0-1
- Fix release info for domain_type fields
- CA-270622: HA max tolerance is wrong for >16-host pools
- CA-271491: Creating NFS SR on 64-host pool ~7x slower than 16-host
- Move to xapi-travis-scripts coverage script
- Add Test_client using Client module to test auto-generated layers
- database: resurrect additional test
- Simplify nbd_info Alcotest comparator

* Mon Mar 05 2018 Christian Lindig <christian.lindig@citrix.com> - 1.80.0-1
- CA-282112: Fix domain_type setting during SXM from older releases

* Mon Mar 05 2018 Christian Lindig <christian.lindig@citrix.com> - 1.79.0-1
- Quicktest_vdi_copy: clean up
- CA-277464: Quicktest_vdi_copy: wait for VBD unplug before destroying VDI
- CP-24206: handle redirections issued by SM
- CA-274267: Make permanent_vdi_detach and _detach_by_uuid work for SMAPIv3
- CA-272163: Redirect snapshot to host that has activated VDI (if any)
- Convert Test_basic to Alcotest
- Convert Test_agility to Alcotest
- Convert Test_daemon_manager to Alcotest
- Remove Test_basic
- CP-25621: Add Host.iscsi_iqn to datamodel
- CP-25621: Add stub set_iscsi_iqn function
- CP-25621: Add iscsi_iqn to the CLI
- CP-25621: Add the setter and the watcher thread
- CP-25621: Start other-config watcher thread
- CP-25621: Actually do the set in Host.set_iscsi_iqn
- CP-25621: Fix implementation of Host.set_iscsi_iqn
- CP-25621: Add a unit test for xapi_host_helpers.ml
- CP-25621: Add a test of the updated implementation of set_iscsi_iqn
- Xapi_host_helpers: re-add comment about MD3000i alias bug workaround
- CP-25621: Add an mli file for xapi_host_helpers
- CP-25621: Respond to review comments from @gabori
- CP-26457: Make multipath configuration a host parameter
- Sync ISCSI iqn and multipathing config files at startup
- Host.set_iscsi_iqn: reject empty string
- Add SR Multipath capability
- Update firstboot scripts to use the new API for setting the iSCSI IQN
- CA-274585: allow unplugging statefile VDI
- CA-274585: unplug all local PBDs on shutdown/reboot
- CA-277346: do not get stuck detaching metadata VDI
- CA-277346: stop (DB) requests when shutting down the master
- Tasks.with_tasks_destroy: add a function that waits for tasks with a timeout
- Convert host evacuation script into ocaml
- CP-24677: Add Cluster and Cluster_host classes to datamodel
- CP-24684: Add CLI for Cluster.pool_create
- Fix the SDK
- CP-24678 CP-24679: Implement Cluster.create and Cluster_host.create
- CP-24865: Implement Cluster.pool_auto_join logic
- CP-24865: Add a test for the dbsync code
- Make Cluster.create go through message_forwarding
- CP-24680: Add CLI for Cluster.create
- CP-24680: Add CLI for Cluster_host.create
- CP-24680: Add CLI getters/setters for Cluster and Cluster_host
- CP-24680: Remove code duplication; use new `get_param` function
- CP-24680: Use RPC functions to get cluster operation strings
- Correctly auto-complete UUIDs in cluster-host-* CLI calls
- CP-24682/CP-24683: Implement Cluster_host.enable/disable
- CP-24687: Add concurrency to Cluster/Cluster_host creation
- CP-24687: Simplify the pool valid operations code
- CP-24688: Add unit tests for clustering-related allowed operations
- CP-24689: Implement host-local clustering lock
- Reorganize clustering code
- quicktest: allow filtering by SR name
- CA-271525: Split 'ip_of_host' in two to allow reuse of parts
- CA-271525: Rearrange the cluster_host creation code
- CA-271525: Add some code to fix the prerequisites
- CA-271525: Add a test for the prerequisite stuff
- CP-25607: Add a Cluster.pool_resync API call
- CP-25607: Add a CLI for Cluster.pool_resync
- CA-271525: Ensure the types are correct in pif_of_host
- CA-271525: Add a test for create_as_necessary
- CA-271525: Add mli files for Xapi_cluster_host and xapi_cluster
- CP-25607: Rename a parameter of Cluster.pool_resync
- CA-271525: Address review comments from @gabori
- CP-24690: Refactor code into separate function
- CP-24690: Take clustering lock and verify cluster_host is enabled
- CP-24690: Use API errors for cluster_host being enabled/disabled
- CP-24690: Add tests for new clustering functionality
- CA-270443: Avoid deadlock in SR.create / PBD.plug
- CA-274113: Create hosts as enabled on the slave
- CA-274107: Forward cluster host enable/disable to correct host
- CP-25261: Implement Cluster_host.destroy and its CLI
- CP-25261: Fix Cluster_host.create CLI
- CP-25261: Fix Cluster_host.disable prerequisites
- CP-25261: Implement Cluster.destroy and its CLI
- Cluster_host: fix type mismatch
- CP-25971: Cannot cleanly destroy a disabled node
- quicktest: do not run ISO tests when explicitly picking another SR
- quicktest_cbt: run test only on specified SR
- Add Cluster.pool_destroy
- Cluster.pool_create: remove pool parameter
- CP-24681: Use feature flag to disable clustering
- Reverting adding feature flags until we have v6d changes
- Update allowed operations when creating Cluster & Cluster_host
- Reinstating feature flag/licensing check
- Test that Cluster_host.destroy is disallowed when SR is attached
- CA-275728: disallow Cluster_host.destroy if SR is still attached
- [CP-25892] Use cluster init_config instead of address
- CP-26038: log UUIDs instead of opaquerefs where possible
- CP-26038: plumb through debug task
- CP-25890: xe-toolstack-restart should know about xapi-clusterd
- CP-26200: s/rel_jura/rel_kolkata/
- [CP-26175] Allow setting corosync timeouts in xe cluster-create
- [CP-26175] Validate timeout parameters in xapi_cluster
- Fix Xapi_clustering.assert_cluster_host_is_enabled_for_matching_sms
- CP-26166: run Cluster.pool_resync on PBD.plug
- Test_clustering: add tests for no Cluster_host or non-gfs2 SR
- CP-24694: disable clustering on shutdown after unplugging the PBDs
- Pool.eject: remove host from cluster, if it's a member
- Make Cluster_host.enable/disable idempotent
- Cluster.pool_resync: ensure enabled Cluster_hosts are enabled
- CP-24694: disable Cluster_host on shutdown and reenable on startup
- CP-24694: allow shutdown/reboot operations when the hosts that are down are disabled
- [CA-273985] Take clustering lock only if SM requires a cluster stack
- CA-275786: Check PIF prerequisites when creating cluster
- CP-26197, CP-25397: Do not run xapi-clusterd if clustering is turned off
- [CP-25971] Introduce Cluster.pool_force_destroy (#3423)
- CA-282012: enable/disable clustering daemon (#3430)
- Update to latest API from team/ring3/master
- Remove scripts/examples/python/shutdown.py
- Add kolkata release
- Port Test_cluster and Test_cluster_host to Alcotest
- Be more conservative about clustering APIs: lifecycle=prototyped
- Typo in readme (#3484)

* Wed Feb 28 2018 Christian Lindig <christian.lindig@citrix.com> - 1.78.0-1
- Resurrect a database unit test
- CP-24206: check snapshot works when VDI is activated on different hosts
- CA-271525: Add a test_rpc field to the context
- CA-271525: Move over all uses of 'test_mode' to use the mock rpc function instead.
- Tar_unix: replace Tar_unix.Archive.multicast_n_string with its implementation
- Make attach_and_activate independent of domain type
- Revert "Create a VM_metrics object for dom0 at start up"
- Create_misc: rename ensure_domain_zero_guest_metrics_record
- Ensure that a metrics record for dom0 is created immediately
- Introduce fields VM.domain_type and VM_metrics.current_domain_type
- Introduce VM.set_domain_type
- Override VM.set_HVM_boot_policy
- Update CLI for new VM.domain_type field
- Update CLI for new VM_metrics.current_domain_type field
- Set VM boot config based on VM.domain_type
- Replace internal uses of VM.HVM_boot_policy by VM.domain_type
- DB upgrade rule for VM.domain_type
- Set VM.domain_type on VMs imported from older releases
- Set VM_metrics.current_domain_type upon xenopsd change events
- Allow hotplug of VBDs into PVinPVH guests
- Allow PVinPVH domains to do power-state operations always
- Specify the domain_type used by test_no_migrate more coherently.
- Correctly generate devid for VBDs for PVinPVH
- Remove more conflating of hvm with emulated devices
- Switch to memory.ml from xcp-idl
- Update memory_check.ml for PV-in-PVH
- PV-in-PVH VMs need static-max to start
- Add new helper to get domain_type regardless of the power_state
- Rename will_have_qemu_from_domain_type to needs_qemu_from_domain_type
- Remove hvm helpers, which are now unused
- Make current_domain_type correct for suspended VMs
- Ensure the current_domain_type field is persisted in the db
- Restrict domain_type upgrade rule to `unspecified VMs
- Handle domain zero specially in DB upgrade task for domain type
- Remove unused helpers
- Simplify Helpers.boot_method type
- Extend ResetCPUFlags test for PVinPVH case
- Simplify & speed up data_destroy timing tests
- remove old (and never compiled in jbuilder/oasis) executables
- xapi: separate xapi, quicktest and tests in separate folders
- CP-26685 Adapt network interface when porting ppx
- CP-24688: Refactor `with_pool_operation` to be easily testable
- CA-271525: Log everything from the unit-test suite
- CA-272147: Fix SR.set_name_label and _description for SMAPIv3
- CA-277346: log backtrace when parsing HA liveset

* Thu Feb 22 2018 Christian Lindig <christian.lindig@citrix.com> - 1.77.0-1
- CA-283754: treat potential internal errors from V6
- Fix json backend
- Testing: Convert tests to Alcotest
- Refactoring: move modules into files
- Backwards-compatibility: Move api_versions back to datamodel
- Cleanup: Remove redundant pipe definitions
- Remove field_has_effect from VBD.mode in favour of explicit declaration 
  of setter
- Remove redundant effectful fields (after CA-11132)
- Remove effectful 'actions_after_crash' in favour of explicit setter

* Mon Feb 19 2018 Christian Lindig <christian.lindig@citrix.com> - 1.76.0-1
- Move datamodel types into sub modules
- Consistently name and use other Datamodel types already in modules
- CA-283632/XOP-919: Add VM reference to VM_FAILED_SHUTDOWN_ACK error
- VDI.create: explicitly specify cbt_enabled = false
- VDI.snapshot, clone: pass down complete vdi_info
- vdi_info_of_vdi_rec: use try-with and List.assoc
- Update readme and maintainer info (#3449)
- Revert "Fixed an issue with device number in script"
- CA-283654: Fix kpartx arguments
- Match default file list to pygrub.
- Fixed display of Plugging VBD message.
- CA-280981: Import dom0 record on pool join

* Fri Feb 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.75.0-1
- Return modified device_config in SR.create SMAPIv2 call
- CP-24350: plumb through sharable flag
- Test CA-274152: SR.scan should update VDI.sharable
- Xapi_sr.update_vdis: correctly set VDI.sharable field
- CP-26444: static-vdis: need to save/pass uuid to SR.attach with SMAPIv3
- CA-259369: Make sure we don't return SRmaster in the update 
  device-config after SR.create
- CP-20544: initialize coverage for XAPI itself too
- CA-281002 CA-271406 let XSM+vGPU fail if VM reboots
- Remove redundant mtc.ml

* Wed Feb 07 2018 Christian Lindig <christian.lindig@citrix.com> - 1.74.0-1
- CP-26717: Xapi now compatible with PPX-based Gpumon
- CA-268763: Add logic to Xapi_host.create to limit host numbers
- CA-266936: Use a CArray instead of an ocaml Buffer
- CA-271867: Local-to-local storage migration fails with out-of-space

* Fri Feb 02 2018 Christian Lindig <christian.lindig@citrix.com> - 1.73.0-1
- Convert Test_vm_check_operation_error to alcotest
- Fixed an issue with device number in script

* Wed Jan 31 2018 Christian Lindig <christian.lindig@citrix.com> - 1.72.0-1
- CA-276638, CA-281320: Catch handle_invalid in Valid_ref_list
- Port Test_vdi_allowed_operations to alcotest

* Fri Jan 26 2018 Christian Lindig <christian.lindig@citrix.com> - 1.71.0-1
- Depend on new tar-unix ocamlfind package
- CP-26098: Upgrade xapi to use PPX-based v6d interface

* Wed Jan 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.70.0-1
- Use alcotest for test suite, update opam file and dependencies

* Fri Jan 19 2018 Christian Lindig <christian.lindig@citrix.com> - 1.69.0-1
- CP-26471: Message switch has been renamed after been ported to jbuilder.
- Added explicit dependency to message-switch-unix and synchronised the opam file with the one in xs-opam.

* Tue Jan 16 2018 Christian Lindig <christian.lindig@citrix.com> - 1.68.0-1
- xapi-database: add missing xapi-stdext dependency
- xapi-database: add necessary xapi-stdext dependencies
- xapi-types: add necessary xapi-stdext dependencies
- idl: use xapi-stdext sub libraries in the generated code
- xapi-database: get rid of deprecated stdext stuff
- xapi_db_process: cleanup dependencies
- cdrommon: cleanup dependencies
- events: cleanup dependencies
- graph: cleanup dependencies
- datamodel: cleanup dependencies
- license: cleanup dependencies
- mpathalert: cleanup dependencies
- perfest: cleanup dependencies
- rfb: cleanup dependencies
- util: cleanup dependencies
- vncproxy: cleanup dependencies
- xapi-cli-protocol: cleanup dependencies
- xapi-client: cleanup dependencies
- META.in: artifacts of old build - removing
- xapi-types: cleanup dependencies
- xe-cli: cleanup dependencies
- xsh: cleanup dependencies
- xapi-types: add comment on non-tail-recursive implementation
- test_cpuid_helpers: fix comparison tests
- Add Cpuid_helpers.is_equal
- Add unit tests for Cpuid_helpers.is_equal
- Use is_equal in is_subset and is_strict_subset
- XOP-908/CA-279498: Zero-extend CPU features when comparing old and new sets
- CA-279502: Set the correct release for the is_default_template field (#3401)
- bisect_ppx for XAPI
- use more CPUs when building XAPI
- CP-20544: Initialize coverage dispatcher
- configure: add --enable-coverage
- Update .travis-opam-coverage.sh

* Thu Jan 11 2018 Christian Lindig <christian.lindig@citrix.com> - 1.67.0-1
- CP-24602, CP-24605: Renamed libraries after porting to jbuilder.
- CP-26469: Defined release jura.
- CA-271406 infer_vgpu_map: VM might not be live
- CA-279161 if unavailable, don't update pGPU compat data
- Travis: if travis tests fail exit with code 1

* Mon Jan 08 2018 Christian Lindig <christian.lindig@citrix.com> - 1.66.0-1
- This release adds support for vGPU migration
- CA-276964 on import, set suspend_SR to null when unknown
- CP-23025: Document the JsonRpc protocol in the error handling section.
- CA-270463 refactor xapi_vm_lifecycle.check_vgpu()
- CA-270463 allowed ops: check vGPU is suspendable
- CA-270463 Merge is_nvidia_vgpu and is_suspendable
- CA-273306: do not assert the VM power_state during VM.checkpoint
- Add compat metadata field to vGPU in datamodel
- Add {update,clear}_vgpu_metadata
- Add call to clear_vgpu_metadata in VM.resume
- Add update.vgpu_metadata in VM.suspend
- Check vGPU/pGPU compatibility
- CP-26076 block VM.checkpoint on any VM with a vGPU
- CA-274957: simplify and reorganise Nvidia VGPU compatibility check
- xapi_pgpu_helpers: avoid multiple calls to get all pgpus
- CP-26145: prevent vgpu-migration of VMs between pre-Jura and Jura/later hosts during RPU
- CA-275660 release vGPUs from VM on suspend (#3364)
- Travis test: output only failure message

* Wed Jan 03 2018 Christian Lindig <christian.lindig@citrix.com> - 1.65.0-1
- Correct FCoE SR to uppercase
- CA-266936: Move pci lookups to string_opt to prevent some segfaults
- CA-266936: Update xapi to use the new pci lookup functions
- Trim the result after executing script with forkhelper
- xapi_pci_helpers, xapi_vgpu_helpers: add pci lookup debugging information
- xapi-database: add necessary xapi-stdext dependencies
- xapi-types: add necessary xapi-stdext dependencies
- idl: use xapi-stdext sub libraries in the generated code
- xapi-database: get rid of deprecated stdext stuff

* Mon Dec 18 2017 Christian Lindig <christian.lindig@citrix.com> - 1.64.0-1
- CA-178651: FCoE NIC is not prevented from unplugging
- Valid_ref_list: add iter function
- Quicktest_cbt: don't fail in cleanup due to VDI refs becoming invalid
- Add a fix and test for setting an empty string as a key in a map
- cdrommon: fix incorred dependencies, missing stdext fix

* Tue Dec 12 2017 Christian Lindig <christian.lindig@citrix.com> - 1.63.0-1
- Add jbuildered version of pci for debugging purposes
- Remove unnecessary pci dependency
- pci: Add LICENSE and CHANGES to fulfill the LICENSE requirements
- Defined new api release kolkata and bumped the api version to 2.10.
- Corrected reindent recipe (the old one was not working).
  Ocp-indented datamodel.ml and datamodel_types.ml.
- xapi: oPasswd -> opasswd for support to version 1.0.2

* Tue Dec 05 2017 Christian Lindig <christian.lindig@citrix.com> - 1.62.0-1
- CA-271874: Local-to-local storage migration using CLI, without specifying VDI-map, fails badly
- CA-274936: more strict typing of API for 'a Ref.t conversions from Rpc.t
- CA-271874: Local-to-local storage migration using CLI, without specifying VDI-map, fails badly -rework
- CA-274994: Set the error code for JsonRpc v2.0 to a non-zero value.
- CP-23025: Documented the Json-Rpc protocol in the API reference.
- CA-271874: Local-to-local storage migration using CLI, without specifying VDI-map, fails badly -rework++

* Wed Nov 29 2017 Christian Lindig <christian.lindig@citrix.com> - 1.61.0-2
- Add back changelog entries that were lost in a merge

* Fri Nov 24 2017 Christian Lindig <christian.lindig@citrix.com> - 1.61.0-1
- [CA-271014] Only get local SRs on the physical utilisation thread
- [CA-271014] Reduce Database calls in get_all_plugged_srs
- fix compatibility for older python (doesn't know context [SSL])
- CA-269706: Prevent snapshot-destroy command to destroy normal VM (#3331)
- CA-273239: Template-xxx CLI commands are allowed on non-template
  VMs (#3337)
- CP-24877: CBT quicktest: verify xapi's DB is in sync with SM after
  CBT ops using VDI.update
- xapi-datamodel: add missing dependency on mustache
- CA-274079: Removing one Pusb removes all Pusbs in the pool
- Bumped the API version to 2.8.
- The xenopsd library has been renamed to xapi-xenopsd.
- Removed remaining instance of oclock.

* Wed Nov 15 2017 Rob Hoes <rob.hoes@citrix.com> - 1.60.1-1
- CA-262059: Remove VDI.resize_online - no SM backends support it
- CA-272679: Fix error args of feature check for VM.pool_migrate
- CA-271852 XenServer build date hardcoded to 1970-01-01
- CA-265117: xapi.conf server_cert_path not respected

* Mon Nov 06 2017 Rob Hoes <rob.hoes@citrix.com> - 1.60.0-1
- CA-271857: Add a fix for start-of-day xenopsd sync
- CA-272126: Don't get NVidia vGPU types from XML file for now.

* Thu Nov 02 2017 Rob Hoes <rob.hoes@citrix.com> - 1.59.0-1
- CA-271052: pool join fixup
- CA-269137: get_nbd_info: get subject from TLS cert
- CP-25372: Prefer non-wildcard certificate subjects
- CP-22019: Test enable/disable_cbt, data_destroy, and snapshot update the necessary fields
- CA-267946: Avoid Db.is_valid_ref RPC call when Ref is NULL
- CP-22019: Add test to check VDI.{clone, copy} update cbt_enabled field
- CP-24132: unit test for usb_scan.py (#3324)
- Revert "Factor out all_vm_operations"
- opam fixes

* Wed Nov 01 2017 Rob Hoes <rob.hoes@citrix.com> - 1.58.0-1
- vGPU migration tech preview
- CA-84019: Call Host.allocate_resources_for_vm for cross-pool migrations
- CA-270642, CA-265691: Copy metrics from snapshot when reverting
- Eliminate internal uses of the VM.last_booted_record field

* Tue Oct 24 2017 Rob Hoes <rob.hoes@citrix.com> - 1.57.0-1
- USB passthrough
- CA-267661: Add RPU rule to update Tools SR PBD.device_config
- CA-268761: Trailing whitespaces are lost by the xapi database
- CA-265413:  Disable passthrough when using MxGPU
- Move Tools SR PBD.device_config to xapi_globs
* Mon Oct 23 2017 Marcello Seri <marcello.seri@citrix.com> - 1.56.0-2
- Add additional scripts and requires needed for USB passthrough

* Fri Oct 20 2017 Rob Hoes <rob.hoes@citrix.com> - 1.56.0-1
- CA-267946: VM.update_allowed_operations: cache some common values when checking operation errors in a loop
- CA-269366: VDI.get_nbd_info: fix returned IPv6 addresses
- Unit test network.add,remove_purpose calls

* Fri Oct 13 2017 Rob Hoes <rob.hoes@citrix.com> - 1.55.0-1
- CBT enhancements

* Thu Oct 12 2017 Rob Hoes <rob.hoes@citrix.com> - 1.54.0-1
- Add build shortcut for VS Code
- CP-24529: Add RPU(Rolling Pool Upgrade) feature flag
- CP-24529: Add Pool_size feature flag
- CP-24802: Add new constraint in Pool.join for the Host not having Pool_size feature
- CP-24647 CA-223754 move periodic scheduler to use mtime clock
- Remove ocaml/.merlin - it's now auto-generated
- xapi-*: update opam files
- Remove unnecessary stdext dependendency from xapi-types
- xapi: do not depend on mustache and xen-api-client

* Thu Oct 05 2017 Rob Hoes <rob.hoes@citrix.com> - 1.53.0-1
- CA-268114: Revert "CA-266936: pciutils: use the file dump in a temp file if possible"

* Wed Oct 04 2017 Rob Hoes <rob.hoes@citrix.com> - 1.52.0-1
- CA-266936: pciutils: use the file dump in a temp file if possible
- CP-24360: Initialise VM.platform['device-model'] values (upstream QEMU)
- Fix storage migration log message: list only similar VDIs instead of all the local ones
- CA-266914: Remove product name from error message
- Revert "CA-223754 move periodic scheduler to a monotonic clock"

* Mon Oct 02 2017 Rob Hoes <rob.hoes@citrix.com> - 1.51.0-1
- CP-24868: Reintroduce VM.set_bios_strings and change to Map(String, String)
- CP-24459: Adding hidden VDI.set_cbt_enabled setter
- Makefile: run tests without buffering

* Mon Sep 25 2017 Christian Lindig <christian.lindig@citrix.com> - 1.50.0-1
- remove REQ-540 code as it is not yet ready

* Fri Sep 22 2017 Rob Hoes <rob.hoes@citrix.com> - 1.49.0-1
- Add IGMP snooping feature.
- Add function VM.set_bios_strings and related stuff
- Use default enum unmarshalling on a per-enum basis
- Port to jbuilder
- CA-88550: Block VM.import during RPU
- CA-249810: Change pool update related log format
- CA-223754: move periodic scheduler to a monotonic clock
- Remove geneva compat code from CLI
- Increase quicktest code coverage

* Tue Sep 12 2017 Rob Hoes <rob.hoes@citrix.com> - 1.48.0-1
- CA-264428: Use --batch when calling gpg
- CA-264331: Remove unused shutdown ack timeout setting

* Mon Sep 04 2017 Rob Hoes <rob.hoes@citrix.com> - 1.47.0-1
- CA-261166: The jsonrpc version of the response should match the one of the request.
  The structure of the error output for v2 should comply with the specs.
- CA-260245: Fix SXM: old host choking on new op

* Wed Aug 23 2017 Rob Hoes <rob.hoes@citrix.com> - 1.46.0-1
- CA-261855: Generate automatically an image map for the API classes.
- Add LICENCE_RESTRICTION to the error whitelist in pool_update.precheck
- CA-263064: Stop logging the body of jsonrpc requests.
- CA-263587: extract error content from update precheck script

* Fri Aug 11 2017 Rob Hoes <rob.hoes@citrix.com> - 1.45.0-1
- Add unit tests for CA-254515
- CA-254515: Check database when updating VDI.snapshot_of
- CA-254515: Update new VDIs after they are created
- Quicktest for import_raw_vdi when no host is available for the SR.
- CA-253959: Modify error message from update precheck script.
- Add support for vdi_data_destroy SMAPIv1 call
- Add VDI.data_destroy SMAPIv2 function
- Add VDI_NO_CBT_METADATA XenAPI error
- Implement VDI.data_destroy XenAPI call
- Add xe vdi-data-destroy CLI command
- datamodel: add list of errors to CBT calls
- Add support for vdi_export_changed_blocks SMAPIv1 call
- Add VDI.export_changed_blocks SMAPIv2 function
- VDI.data_destroy: reset the VDI's content_id
- VDI.export_changed_blocks: lock vdi_to during SMAPIv2 call
- Implement VDI.export_changed_blocks XenAPI call
- Add xe vdi-export-changed-blocks CLI command
- VDI.export_changed_blocks: only require SR of vdi_to
- Test_common.make_pif: correct default value of iPv6 param to empty list
- Implement VDI.get_nbd_info XenAPI call
- Test_vdi_cbt: use OUnit's set comparator
- Test_event: use Test_common.make_session helper

* Wed Aug 02 2017 Rob Hoes <rob.hoes@citrix.com> - 1.44.0-1
- CP-23026 pool join rules until automated testing is available
- CA-259405: Only check pool master's updates on pool join
- CA-259288 provide descriptive reason when raising pool_hosts_not_homogeneous
- CP-23026 CA-258536 update update records at startup
- CA-259405: fix comment about pool-join implementation
- Add other_config field to pool_update
- Pool_patch: remove enforce_homogeneity from other_config when syncing update
- Use Xapi_globs.host_update_dir in pool_update.resync_host
- Added option to generate the api reference in docbook format and provided relevant template.
- Extended README.md and excluded from build output.

* Mon Jul 24 2017 Rob Hoes <rob.hoes@citrix.com> - 1.43.0-1
- datamodel: remove `scan from vdi_operations enum
- CA-246335: Only allow miami-era VM operations during rolling upgrade mode
- VDI.snapshot,clone: test that VDI.cbt_enabled is correctly set
- CA-259579: Introduce ballooning_timeout_before_migration api error
- CA-260262: Only allow VDI operations supported by older releases during RPU

* Wed Jul 12 2017 Rob Hoes <rob.hoes@citrix.com> - 1.42.0-1
- CA-258652/SCTX-2565: Get initial host memory from squeezed
- CA-226886: VDI import: handle exn if SR is unavailable for any host.
- CA-258023: Further API reference improvements.
- Xapi_vdi.update_allowed_operations: consider all VDI ops
- pool_update.introduce: disallow cbt_metadata VDI
- Removal of dead code

* Tue Jul 04 2017 Rob Hoes <rob.hoes@citrix.com> - 1.41.0-1
- CA-244865: Datamodel: errors from copy/paste in (v)gpu-related descriptions
- CP-22381: Removed the last binary from the docs.
- CA-245334: Generate the API version and the date on the cover of the API reference automatically.
- CP-22537: Added script and instructions to build the API reference pdf from the autogenerated markdown with pandoc.
- CP-22381: Increased table column width (in the pdf output).

* Mon Jul 03 2017 Rob Hoes <rob.hoes@citrix.com> - 1.40.0-1
- CA-253933: bugfix - VM cannot reboot when migrating to another SR
- CA-187179: Refine error message of pool auth disable
- CP-23026 mark new field 'enforce_homogeneity' as introduced in rel_honolulu
- Add some CBT unit tests
- Support python 3 in XenAPI.py
- Remove dead code and fix Travis builds

* Fri Jun 23 2017 Rob Hoes <rob.hoes@citrix.com> - 1.39.0-1
- CP-22535: Rewrote latex_backend.ml to generate the API reference in markdown
- Removed binary file; updated instructions

* Wed Jun 21 2017 Rob Hoes <rob.hoes@citrix.com> - 1.38.0-1
- Initial support for Changed Block Tracking (CBT)
- CA-257178: Refine format string for messages
- CA-257178: Refine code style for mail-alarm
- CP-22536: Translated *.tex files to markdown.
- Update lifecycle for PVS classes

* Fri Jun 16 2017 Marcello Seri <marcello.seri@citrix.com> - 1.37.0-1
- Release new version to workaround a build system issue with binary patches

* Fri Jun 16 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.36.0-1
- Enable python's nose test framework
- Explicitly mention python folders in nosetests invocation
- build-env Travis job: fix doc uploading
- Extract nosetests into a separate build instance
- build-env Travis job: fix documentation upload
- deploy.sh: update path of generated json files
- Move all the python dependencies install into the corresponding travis shell script
- CP-19454: Support Chinese and Janpanese mail alert
- CP-19454: Refine mail-alarm code style
- CP-19454: Replace zh-CN & ja-JP language pack with translated file
- CP-19454: Fix syntax error in mail-alarm
- CA-253935: Add sr_io_throughput alert
- CA-253935: Refine code style for mail-alarm
- CP-22525: Add test_mail-alarm.py
- CP-22525: Refine test_mail-alarm.py to cover all EmailTextGenerator
- L10N: CP-22708 Translation Checkins
- L10N: Adjusted the line intends.
- CA-255509: Failures in precheck scripts are not reported correctly.
- Xapi_vdi: clean up snapshot capability check

* Tue Jun 13 2017 Kun Ma <kun.ma@citrix.com> - 1.35.0-2
- CP-19454: Add 3 JSON mail language pack

* Thu Jun 01 2017 Rob Hoes <rob.hoes@citrix.com> - 1.35.0-1
- REQ-42: Support for management interface on a tagged VLAN, including new Pool.management_reconfigure API
- CA-223802/XSO-672: Recognise new xenstore format for guest IP reporting
- Datamodel: deprecate crashdump XenAPI class

* Tue May 23 2017 Rob Hoes <rob.hoes@citrix.com> - 1.34.0-1
- VDI.snapshot: check that SM has this capability
- CA-253489 xe update-upload: test if default SR is valid
- Removed release dundee_plus as it was never released.
- CA-245333: Extended the release order to include the corresponding API version and branding info and use this in the API docs.
- CA-252876: AD group name with parenthesis not work as expect in XenServer 7.0 pool

* Thu May 18 2017 Rob Hoes <rob.hoes@citrix.com> - 1.33.0-1
- smint.ml: Remove unused all_capabilites variable
- CA-205515 i18n: JA/SC: The error message about failed to join a domain is not localized.
- Update xapi_vm_helpers and xapi_xenops for ocaml 4.03+
- Update cli_operations to work with 4.03+

* Fri May 12 2017 Rob Hoes <rob.hoes@citrix.com> - 1.32.0-1
- CA-247695: VM part of snapshot schedule can't be converted into template
- Facilities for unit-test of xenopsd interactions
- CP-21359: Remove the multiplier on update size calculations
- CA-241130: Retrieved recommendations not as expected
- CA-248243: Include the html xenserver flavour of the docs in the build.
- CA-248125: Fix openvswitch-config-update plugin issue.
- CA-249381: Fix schema versions to Current 5.120, Ely 5.108, Falcon 5.120
- XOP-830: Fix the resynchronisation logic on xapi restart
- Update to new Scheduler interface
- Update to newest xcp.updates interface
- CA-248389: Avoid exception INVALID_VALUE in VM import
- CA-243824: Plumb through the errors in pool_update.precheck
- Removed certain example python scripts
- CA-248921: If there is no session in the context, assume it's internal
- Avoid myocamlbuild.ml changing every time you build
- CA-248775: Set the name of VDIs associated with patches/updates
- Update merlin file, add missing libraries and add ocamlbuild _build path
- CA-244657: Disable cancellation for some xapi tasks
- CA-236351: Force shutdown a VM when no suspend VDI is found.
- New pool join rules to reflect ely changes in the updates.
- Bumped API version to 2.7.
- CA-249786: removed build number comparison from pool join rules.
- CA-250143: Stat the mirror _before_ removing it
- CA-242706: call update_getty at xapi startup
- CA-250376: Add protocol option in firewall-port script
- CA-171948: Make add_to_map DB calls idempotent
- CA-171948: Reinstate non-idempotency, with a switch
- CA-249662: Pool_patch handler: If an SR is not specified, use default_SR
- CA-250757: Refresh software version after update been applied
- CA-250748: MTU on pif does not always sync to xapi db
- CA-251251: Use /var/update/applied/uuid mtime for patch apply time
- CA-250858: Fix potential bug in `wlb_reports.ml` when WLB health check report
- End the temporary yum.conf file with a newline
- CA-249668: Raise an API error `tls_connection_failed` on TLS connection failure.
- Storage_access: fix task names to match called op
- opam: update to xs-opam version
- Travis: Add OPAM build method and coverage
- README: add build, coverage, LoC badges
- Remove dead/unused code

* Wed Mar 29 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.31.0-3
- Add dependence on xenopsd-devel

* Mon Mar 27 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.31.0-2
- Generate the API reference.

* Thu Mar 23 2017 Rob Hoes <rob.hoes@citrix.com> - 1.31.0-1
- Move to Oasis build system
- Spring clean: remove unused stuff
- CP-21107: MxGPU: remove `sched` parameter from whitelist file

* Wed Mar 22 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.29.0-2
- Update spec file for oasis-based xapi

* Wed Mar 22 2017 Rob Hoes <rob.hoes@citrix.com> - 1.29.0-1
- CP-21211: Implement unit test for SDN_controller APIs
- CA-247452: Restrict the nearest VDI choice to those of smaller or equal size
- CA-247452: Sort VDIs by sizes before copying them over during SXM
- CA-247694: Revert "CA-229028: Check VDI size is valid in vdi-import"

* Thu Mar 16 2017 Marcello Seri <marcello.seri@citrix.com> - 1.28.0-2
- Add missing Requires for the *-devel libraries

* Thu Mar 16 2017 Rob Hoes <rob.hoes@citrix.com> - 1.28.0-1
- CA-203227: Improve VM shutdown performance for many VDIs
- CA-245811: Fix `assert_vm_supports_quiesce_snapshot` function
- Moved the current api_version related constants from xapi_globs.ml to the datamodel.ml
- SDN controller enhancements
- AMD MxGPU

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 1.27.0-2
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Thu Mar 09 2017 Rob Hoes <rob.hoes@citrix.com> - 1.27.0-1
- Use PPXs
- CA-245389: segregation between updates, and separation of stage/update/commit
- CA-246262: Bash completion performance fix
- CP-20287: Exposed experimental features in the API.

* Wed Mar 01 2017 Rob Hoes <rob.hoes@citrix.com> - 1.26.0-1
- CA-229028: Check VDI size is valid in vdi-import
- Update merlin file to use all subdirectories in 'ocaml/'
- Update maintainers list

* Fri Feb 17 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 1.25.0-2
- CA-243676: Do not restart toolstack services on RPM upgrade

* Wed Feb 15 2017 Rob Hoes <rob.hoes@citrix.com> - 1.25.0-1
- CA-223676: Check physical connectivity for management interface.
- Rename version.ml -> xapi_version.ml to prevent conflicts with newer OCaml
- Initial release of Scheduled Snapshots (VMSS).

* Thu Feb 09 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.24.0-2
- Removed redundant patch

* Wed Feb 08 2017 Rob Hoes <rob.hoes@citrix.com> - 1.24.0-1
- CP-14033: Add the Falcon release to datamodel
- CP-20725: hide `is_default_template` from the public API
- CA-241301: Don't push RRD for VM if it is not running
- CA-241704: switch from 'yum install' to 'yum upgrade'
- Fix test_assert_space_available unit test
- CA-232290: Task.cancel verify permission before forwarding
- CA-229340: Ensure ref is valid before injecting update
- Update version number on API docs PDF
- CA-229351: disable task cancelling at certain points of SXM
- CA-237165: Remove applied update records from Xapi db after PRU.
- xapi-consts: ensure install dir exists
- CA-237993 xe vm-migrate: guess when user wants SXM
- CA-236821: Provide clear error message if GPG key is not imported.
- CA-172901: add python 2.4 retrocompatibility
- CA-172901: make SSL verification optional

* Thu Jan 19 2017 Rob Hoes <rob.hoes@citrix.com> - 1.23.0-1
- opam: add xapi-test-utils OPAM dependency
- CA-236444: xapi reports WLB consult error when host enters
- Add xapi-cli-protocol to the spec file
- Move files around in preparation for oasis
- CA-236863: division by 0 in VGPU-g detection

* Tue Jan 10 2017 Rob Hoes <rob.hoes@citrix.com> - 1.22.0-1
- CA-237415: remove update group from yum by conf file
- CA-223868: deprecate fields that are superseded by RRDs
- Build reorganisation and cleanup

* Mon Dec 19 2016 Rob Hoes <rob.hoes@citrix.com> - 1.21.0-1
- CA-234510: update db before archiving rrd
- CA-234494: introduce default templates field

* Mon Dec 12 2016 Gabor Igloi <gabor.igloi@citrix.com> - 1.20.1-1
- CA-235986: Add Pool_update.version to the CLI
- CA-233580: Allow control domains to start on disabled hosts
- CA-235358: Fix AD users in child domains cannot log in to XenCenter 7
- Remove obsolete and unnecessary html files

* Wed Dec 07 2016 Gabor Igloi <gabor.igloi@citrix.com> - 1.20.0-1
- CA-234876: Ensure xapi starts after time is synced; don't install /etc/init.d/xapi any longer
- CA-233915: Turn post-op assertions that VM is "Running" into warnings
- CA-234875: Remove old patch records after RPU completes
- CA-228680: Split general-purpose assert into 2 separate asserts
- CA-234358: Add version to pool_update
- CA-227062: Remove spurious backtrace; update host/vm/sr selectors info-strings
- CA-233306: Delete the VDI when invoking Pool_update.pool_clean
- CA-233312: Hide VM's nested-virt and nomigrate fields from CLI
- CA-232307: Fix xe pool-dump-database on slave
- Update CREDITS
- CA-230464: Improve error message when not enough memory for PVS cache
- CA-229331: evacuate: Don't report memory issues for unmigratable VMs
- Revert CA-220610: restore old behavior of host.get_vms_which_prevent_evacutation,
  and remove the host.get_vms_which_prevent_evacuation_all API call, which was
  never published in a release.
- CA-231357: Don't remove old pool_patch records until after RPU
- CA-228780: PVS Proxy: Add clear error message for when no PVS servers are defined
- CA-229176: Fix PVS Proxy status cache inconsistency: invalidate during attach
- CA-229070: pool_update: switch to @update group
- CA-226280: Fix the `cancel_fn` call on failed `check_cancelling`
- CA-225070: Add an option to disable HA non-persistently; refine the start/stop order of the attach-static-vdi service
- CA-228756: Provide more error details for precheck and apply
- CA-229347: Pool_update.introduce: dom0 doesn't need free disk space 3 times the size of the update
- CA-228573: Require a content-length on pool database restore HTTP handler
- CA-229031: Improve error handling when importing update keys
- CA-227807: Internal Error on uploading unsigned Dundee hotfix
- CA-228035: Export update-resync-host and deprecate refresh_pack_info
- CA-223461: Add more info to redo_log and block_device_io logging
- CA-228606: For pool update, generate yum.conf with installonlypkgs
- CA-227716: Refine pool update error messages
- CA-226000: Old patches are not removed on Host Upgrade
- CA-228029: Fix update destroy failure in xe-install-supplemental-pack when exception happens
- CA-227821: Remove legacy gpg keys
- CA-227285: Better error when migrating non-resident VM

* Fri Nov 04 2016 Euan Harris <euan.harris@citrix.com> - 1.13.0-1
- Rationalize packaging formats for supplemental packs and hotfixes
- Mark PV-drivers-up-to-date as deprecated
- Mark VDI.parent as deprecated
- CA-220506: Update rbac role for SR.scan API call.
- CA-226028 support vm-start --force for memory limits under nested-virt
- CA-223505 detach a VM's network (PVS) when migrating away from a host
- CA-227721: init-script: flush to log on xapi start
- CA-220275: increase host evacuation timeout during host shutdown
- CA-224335 re-start agetty only when IP addr changes
- CA-226023 When using nested_virt, don't allow changing_dynamic_range op

* Wed Oct 19 2016 Euan Harris <euan.harris@citrix.com> - 1.12.0-1
- CA-224975: PVS-cache: Handle cache VDIs on non-persistent SR
- CP-18521: Added new field reference_label to the VM class.
- CA-224327: Use `https` connection while calling `import/export_raw_vdi` to remote Host.
- CA-224967: Don't remove proxy state from xenstore when OVS rules are removed
- Only update PVS_proxy.state if OVS rules are present
- CA-189725: support new systemd device naming
- CA-224331: Detect PV drivers => vif|vbd hotpluggable
- CA-217533: Make mark_host_as_dead idempotent

* Thu Oct 13 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.11.0-1
- PVS

* Wed Sep 28 2016 Euan Harris <euan.harris@citrix.com> - 1.10.2-1
- CP-18860: Check memory range before VM.start when using nested virt
- CA-222760: Add default list of accepted ciphers into xapi
- CA-220610: Change host.get_vms_which_prevent_evacutation to return a map with unique keys
- CP-18919: Restrict use of VM.set_VCPUs_number_live

* Wed Sep 21 2016 Euan Harris <euan.harris@citrix.com> - 1.10.1-1
- CA-220170: Fix ha-network-peers CLI field showing hosts as "not in database"
- CA-182929: Raise an error if the storage backend type is unknown.
- CA-206623: Close the input end of the pipe when data feeding is complete
- CA-222060: Remove test for removed validation code
- CA-222060: Only validate VCPUs_max against cores_per_socket, not VCPUs_at_startup
- CA-122248: Avoid returning duplicate events in event.from
- CA-122248: Add a test to search for duplicate events in event.from
- Ignore memory and pif update for transient uuids
- CA-203433: Raise an appropriate API error when we can't SXM a suspend image
- CA-215175: Don't ever execute hooks when we only assume failures.
- CA-220506: Update rbac roles for network.attach_for_vm and network.detach_for_vm API calls.

* Wed Sep 14 2016 Euan Harris <euan.harris@citrix.com> - 1.10.0-1
- Use the correct vif device id in set_MTU or fail
- Add force flag to VM.start
- Fix an issue where VM_metrics were assumed to exist
- Protect PIF.scan with a mutex to avoid duplicate PIFs
- Fix xe-toolstack-restart for mpathalert
- Rename mpathalert-daemon.service to mpathalert.service
- Pick up hvm value from xenopsd, report it on CLI
- Improve error messages in logs
- Fix unknown key iscsi_iqn backtrace
- Add 3 new fields to vm_metric: hvm, nested_virt, nomigrate

* Fri Sep 02 2016 Euan Harris <euan.harris@citrix.com> - 1.9.93-1
- Update to 1.9.93

* Fri Aug 19 2016 Euan Harris <euan.harris@citrix.com> - 1.9.92-1
- Update to 1.9.92

* Thu Aug 18 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.9.91-1
- New release

* Fri Jul 22 2016 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.9.90-1
- First transformer package

