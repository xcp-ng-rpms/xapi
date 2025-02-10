%global package_speccommit 7d7c73786298bfc2d15911500057efe48a928750
%global package_srccommit v24.19.2

# This matches the location where xen installs the ocaml libraries
%global _ocamlpath %{_libdir}/ocaml

%if 0%{?xenserver} < 9
%global build_python2 1
%global include_pyc_pyo 1
%else
# There are still some shebangs for python2, we skip this check
%global __brp_mangle_shebangs %nil
%global include_pyc_pyo 0
%endif

# -*- rpm-spec -*-

Summary: xapi - xen toolstack for XCP
Name:    xapi
Version: 24.19.2
Release: 1.10%{?xsrel}%{?dist}
Group:   System/Hypervisor
License: LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:  http://www.xen.org
Source0: xen-api-24.19.2.tar.gz
Source1: xcp-rrdd.service
Source2: xcp-rrdd-sysconfig
Source3: xcp-rrdd-conf
Source4: xcp-rrdd-tmp
Source5: xcp-rrdd-iostat.service
Source6: xcp-rrdd-squeezed.service
Source7: xcp-rrdd-xenpm.service
Source8: xenopsd-xc.service
Source9: xenopsd-simulator.service
Source10: xenopsd-sysconfig
Source11: xenopsd-64-conf
Source12: squeezed.service
Source13: squeezed-sysconfig
Source14: squeezed-conf
Source15: xcp-networkd-sysconfig
Source16: xcp-networkd-network-conf
Source17: message-switch.service
Source18: message-switch-conf
Source19: message-switch-bugtool1.xml
Source20: message-switch-bugtool2.xml
Source21: forkexecd.service
Source22: forkexecd-sysconfig
Source23: xapi-storage-script.service
Source24: xapi-storage-script-sysconfig
Source25: xapi-storage-script-conf.in
Source26: tracing-conf
Source27: pool-recommendations-xapi-conf

%if "%{dist}" == ".xsx"
# Empty for now
%endif

%if "%{dist}" == ".xsu"
Patch1: 0001-Xen-4.19-domctl_create_config.vmtrace_buf_kb.patch
%endif

# XCP-ng patches
# Enables our additional sm drivers
Patch1000: xapi-24.11.0-update-xapi-conf.XCP-ng.patch
# Patch1001: in XCP-ng xs-clipboardd is named xcp-clipboardd
Patch1001: xenopsd-22.20.0-use-xcp-clipboardd.XCP-ng.patch
# Replace this if/when PR https://github.com/xapi-project/xen-api/pull/4188 is finalized
Patch1002: xapi-23.31.0-open-openflow-port.XCP-ng.patch
# Drop this patch when we don't want to support migration from older SDN controller anymore
Patch1003: xapi-24.11.0-update-db-tunnel-protocol-from-other_config.XCP-ng.patch 
# Upstream PR: https://github.com/xapi-project/xen-api/pull/5918
Patch1004: xapi-24.16.0-openvswitch-config-update-fix-python2ism-in-python3.patch
Patch1005: xapi-24.19.2-fix-ipv6-import.XCP-ng.patch
# Backport from 24.20
Patch1006: xapi-24.19.2-update-new-fingerprint-fields-on-DB-upgrade.backport.patch
# Fix fingerprints for CA certificates too
Patch1007: xapi-24.19.2-more-fingerprint-field-updates-fixes.XCP-ng.patch
# To remove with v24.31.0
Patch1008: xapi-24.19.2-ipv6-reset-networking.XCP-ng.patch
Patch1009: xapi-24.19.2-keep-address-type-network-reset.XCP-ng.patch
Patch1010: xapi-24.19.2-keep-ipv6-management-disable.XCP-ng.patch
Patch1011: xapi-24.19.2-ipv6-pool-eject.XCP-ng.patch
Patch1012: xapi-24.19.2-ipv6-virtual-pif.XCP-ng.patch.patch
# To remove once https://github.com/xapi-project/xen-api/pull/6006 is released
Patch1013: xapi-24.19-2-fix-pem-fingerprint-startup.XCP-ng.patch
# To disable renegotiation vulnerabilities
Patch1014: secure_client_initated_renegotiation_false.patch

%{?_cov_buildrequires}
BuildRequires: ocaml-ocamldoc
BuildRequires: pam-devel
BuildRequires: xen-devel
BuildRequires: libffi-devel
BuildRequires: zlib-devel
BuildRequires: git
BuildRequires: gmp-devel
BuildRequires: libuuid-devel
BuildRequires: make

%if 0%{?build_python2}
BuildRequires: python2-devel
%endif

BuildRequires: python3-devel
BuildRequires: xs-opam-repo >= 6.77.0-1
BuildRequires: libnl3-devel
BuildRequires: systemd-devel
BuildRequires: pciutils-devel
BuildRequires: xen-dom0-libs-devel
BuildRequires: xxhash-devel
BuildRequires: sm
BuildRequires: xen-ocaml-devel
BuildRequires: blktap-devel
BuildRequires: openssl-devel

%description
XCP toolstack.

%if 0%{?coverage:1}
%package        cov
Summary: XAPI is built with coverage enabled
%description    cov
XAPI is built with coverage enabled
%files          cov
%endif

%package core
Summary: The xapi toolstack
Group: System/Hypervisor
%if 0%{?coverage:1}
Requires:       %{name}-cov = %{version}-%{release}
%endif
Requires: hwdata
Requires: redhat-lsb-core
Requires: /usr/sbin/ssmtp
Requires: stunnel >= 5.55
Requires: vhd-tool
Requires: libffi
Requires: busybox
Requires: net-tools
Requires: vmss
Requires: python-six
Requires: python3-six
# This is necessary during py2->py3 transition
%if 0%{?xenserver} < 9
Requires: xcp-python-libs
# Requires yum as package manager
Requires: yum-utils >= 1.1.31
%else
Requires: dnf
%endif
Requires: python3-xcp-libs
Requires: python2-pyudev
Requires: python3-pyudev
Requires: gmp
# XCP-ng: remove Requires for proprietary components
# Requires: xapi-storage-plugins >= 2.0.0
# Requires: xapi-clusterd >= 0.64.0
Requires: xxhash-libs
Requires: jemalloc
Requires: zstd
Requires: createrepo_c >= 0.10.0
Requires: tdb-tools >= 1.3.18
Requires: samba-winbind >= 4.10.16
# XCP-ng: remove Requires for proprietary component
# Requires: upgrade-pbis-to-winbind
# XCP-ng: don't require XS's fork of the setup RPM
#Requires: setup >= 2.8.74
Requires: xcp-ng-release-config
Requires: python3-fasteners
Requires: sm
Requires: ipmitool
# firewall-port needs iptables-service to perform
# `service iptables save`
Requires: iptables-services
Requires(post): xs-presets >= 1.3
Requires(preun): xs-presets >= 1.3
Requires(postun): xs-presets >= 1.3
Conflicts: secureboot-certificates < 1.0.0-1
Conflicts: varstored < 1.2.0-1
BuildRequires: systemd
%{?systemd_requires}

# XCP-ng: add missing requires towards nbd
Requires: nbd

%description core
This package contains the xapi toolstack.

%package xe
Summary: The xapi toolstack CLI
Group: System/Hypervisor

%description xe
The command-line interface for controlling XCP hosts.

%package rrd2csv
Summary: A tool to output RRD values in CSV format
Group: System/Hypervisor
Obsoletes: rrd2csv < 21.0.0-1
Obsoletes: xsiostat < 1.0.1-3
Obsoletes: xsifstat < 1.0.1-3

%description rrd2csv
This package contains the rrd2csv tool, useful to expose live RRDD
metrics on standard output, in the CSV format.

%package tests
Summary: Toolstack test programs
Group: System/Hypervisor
Requires: net-tools

%description tests
This package contains a series of simple regression tests.

%package client-devel
Summary: xapi Development Headers and Libraries
Group:   Development/Libraries
Obsoletes: ocaml-xen-api-client < 21.0.0-1
Obsoletes: ocaml-xen-api-client-devel < 21.0.0-1
Requires: xapi-idl-devel = %{version}-%{release}
Requires: xs-opam-repo

%description client-devel
This package contains the xapi development libraries and header files
for building addon tools.

%package datamodel-devel
Summary: xapi Datamodel headers and libraries
Group:   Development/Libraries
Requires: xapi-idl-devel = %{version}-%{release}

%description datamodel-devel
This package contains the internal xapi datamodel as a library suitable
for writing additional code generators.

%package sdk
Summary: xapi Xen-API Software Development Kit
Group:   Development/Libraries
BuildArch: noarch

%description sdk
This package contains Xen-API bindings for C, Csharp, Java, and PowerShell,
generated automatically from the xapi datamodel, and the Python module.

%package doc
Summary: Xen-API documentation
Group:   Development/Documentation

%description doc
This package contains Xen-API documentation in html format.

%package libs-devel
Summary: Development files for
Group:   Development/Libraries
Obsoletes: ocaml-xen-api-libs-transitional-devel < 2.40
Obsoletes: ocaml-xen-api-libs-transitional < 21.0.0-1
Requires:  xs-opam-repo
Requires:  forkexecd-devel = %{version}-%{release}
Requires:  xapi-idl-devel = %{version}-%{release}


%description libs-devel
The xapi-libs-devel package contains libraries and signature files for
developing applications that use xapi-libs.

%package -n xenopsd
Summary:        Simple VM manager
Requires:       message-switch >= 12.21.0
Requires:       xen-dom0-tools >= 4.13.5-10.53
Requires:       xen-dom0-libs >= 4.13.5-10.13

# This dependency is required exclusively to ensure /dev/sm/* disks have
# +r g=disk permissions
Requires:       sm >= 3.0.12-2

Requires:       python3-scapy
Requires:       jemalloc
Requires:       swtpm >= 0.7.3-4
Requires:       swtpm-tools

%description -n xenopsd
Simple VM manager for the xapi toolstack.

%package -n xenopsd-xc
Summary:        Xenopsd using xc
Requires:       xenopsd = %{version}-%{release}
Requires:       forkexecd
Requires:       xen-libs
Requires:       emu-manager
# NVME support requires newer qemu
# Semantic versioning: describe acceptable range of qemu versions
# if a new major version of qemu/qemu.pg is released and xenopsd is still
# compatible then we just have to update this line and bump the minor for xenopsd
Requires:       qemu >= 2:4.2.1-5.0.0
Conflicts:      qemu >= 2:4.2.1-6.0.0
Obsoletes:      ocaml-xenops-tools < 21.0.0-1

%description -n xenopsd-xc
Simple VM manager for Xen using libxc.

%package -n xenopsd-simulator
Summary:        Xenopsd simulator
Requires:       xenopsd = %{version}-%{release}

%description -n xenopsd-simulator
A synthetic VM manager for testing.

%package -n xenopsd-cli
Summary:        CLI for xenopsd, the xapi toolstack domain manager
Requires:       xenopsd = %{version}-%{release}
Obsoletes:      xenops-cli < 21.0.0-1

%description -n xenopsd-cli
Command-line interface for xenopsd, the xapi toolstack domain manager.

%package -n squeezed
Summary:        Memory ballooning daemon for the xapi toolstack

%description -n squeezed
Memory ballooning daemon for the xapi toolstack.

%package -n xcp-rrdd
Summary:        Statistics gathering daemon for the xapi toolstack
Requires(pre):  shadow-utils
%if 0%{?build_python2}
Requires:       python2-future
%endif
Requires:       python3-future

%description -n xcp-rrdd
Statistics gathering daemon for the xapi toolstack.

%package -n xcp-rrdd-devel
Summary:        Development files for xcp-rrdd
Requires:       xcp-rrdd = %{version}-%{release}
Requires:       xs-opam-repo
Requires:       forkexecd-devel%{?_isa} = %{version}-%{release}
Requires:       xapi-idl-devel%{?_isa} = %{version}-%{release}
Requires:       xen-ocaml-devel
Obsoletes:      ocaml-rrd-transport-devel < 21.0.0-1
Obsoletes:      ocaml-rrdd-plugin-devel < 21.0.0-1

%description -n xcp-rrdd-devel
The xcp-rrdd-devel package contains libraries and signature files for
developing applications that use xcp-rrdd.

%package -n rrdd-plugins
Summary:   RRDD metrics plugin
Requires:  jemalloc
Requires:  xen-dom0-tools
Requires:  xapi-rrd2csv

%description -n rrdd-plugins
This packages contains plugins registering to the RRD daemon and exposing various metrics.

%package -n vhd-tool
Summary: Command-line tools for manipulating and streaming .vhd format files

%description -n vhd-tool
Simple command-line tools for manipulating and streaming .vhd format file.

%package -n xcp-networkd
Summary:  Simple host network management service for the xapi toolstack
Requires: ethtool
Requires: libnl3
# XCP-ng: remove Requires to proprietary component
# Requires: pvsproxy
Requires: bridge-utils

%description -n xcp-networkd
Simple host networking management service for the xapi toolstack.

%package -n message-switch
Summary: A store and forward message switch
License: ISC

%description -n message-switch
A store and forward message switch for OCaml.

%package -n message-switch-devel
Summary: Development files for message-switch
License: ISC
Requires: message-switch = %{version}-%{release}
Requires: xs-opam-repo

%description -n message-switch-devel
The message-switch-devel package contains libraries and signature files for
developing applications that use message-switch.

%package idl-devel
Summary:        Development files for xapi IDL
Requires:       xs-opam-repo
Obsoletes:      ocaml-xcp-idl-devel < 1.200.0
Obsoletes:      ocaml-xcp-idl < 1.200.0

%description idl-devel
The xapi-idl-devel package contains libraries and signature files for
developing applications that the XAPI IDL interface.

%package -n forkexecd
Summary:        A subprocess management service
BuildRequires:  xs-opam-repo
BuildRequires:  systemd-devel
Requires:       jemalloc
%{?systemd_requires}
Obsoletes:      xapi-forkexecd <= 1.31.0-2

%description -n forkexecd
A service which starts and manages subprocesses, avoiding the need to manually
fork() and exec() in a multithreaded program.

%package -n forkexecd-devel
Summary:        Development files for xapi-forkexecd
Requires:       forkexecd = %{version}-%{release}
Requires:       xs-opam-repo
Requires:       xapi-idl-devel = %{version}-%{release}
Obsoletes:      xapi-forkexecd-devel <= 1.31.0-2

%description -n forkexecd-devel
The forkexecd-devel package contains libraries and signature files for
developing applications that use forkexecd.

%if 0%{?build_python2}
%package -n python2-xapi-storage
Summary: Xapi storage interface (Python2)
Provides: xapi-storage = %{version}-%{release}
Obsoletes: xapi-storage < %{version}-%{release}
Requires: python2-future
Requires: python-six
BuildRequires: python2-devel
BuildRequires: python2-setuptools

%description -n python2-xapi-storage
Xapi storage interface libraries for python2

%files -n python2-xapi-storage
%defattr(-,root,root,-)
%{python2_sitelib}/xapi/__init__.py*
%{python2_sitelib}/xapi/storage/*
%exclude %{python2_sitelib}/*.egg-info

%endif

%package -n python%{python3_pkgversion}-xapi-storage
Summary: Xapi storage interface (Python3)
Requires: python3-six
BuildRequires: python3-devel
BuildRequires: python3-rpm-macros
BuildRequires: python3-setuptools

%description -n python%{python3_pkgversion}-xapi-storage
Xapi storage interface libraries for %{python3_pkgversion}

%files -n python%{python3_pkgversion}-xapi-storage
%defattr(-,root,root,-)
%{python3_sitelib}/xapi/__init__.py*
%{python3_sitelib}/xapi/storage/*

%package storage-ocaml-plugin-runtime
Summary:        Development files for xapi-storage
Requires:       xapi-storage = %{version}-%{release}

%description storage-ocaml-plugin-runtime
The xapi-storage-ocaml-plugin package contains runtime libraries for OCaml
plugins for xapi-storage.

%package storage-ocaml-plugin-devel
Summary:        Development files for xapi-storage
Requires:       xapi-storage-ocaml-plugin-runtime = %{version}-%{release}
Requires:       xs-opam-repo

%description storage-ocaml-plugin-devel
The xapi-storage-ocaml-plugin-devel package contains libraries and signature files for
developing applications that use xapi-storage.

%package storage-script
Summary: Xapi storage script plugin server
Requires:	jemalloc

%description storage-script
Allows script-based Xapi storage adapters.

%package -n sm-cli
Summary: CLI for xapi toolstack storage managers

%description -n sm-cli
Command-line interface for xapi toolstack storage managers.

%package -n wsproxy
Summary: Websockets proxy for VNC traffic

%description -n wsproxy
Websockets proxy for VNC traffic

%package nbd
Summary: NBD server that exposes XenServer disks

%description nbd
NBD server that exposes XenServer disks

%package -n varstored-guard
Summary: Deprivileged XAPI socket Daemon for EFI variable storage

%description -n varstored-guard
A daemon for implementing a deprivileged XAPI socket for varstored.
It is responsible for giving access only to a specific VM to varstored.

%global ocaml_dir %{_opamroot}/ocaml-system
%global ocaml_libdir %{ocaml_dir}/lib
%global ocaml_docdir %{_prefix}/doc

%if 0%{?build_python2}
%global __python     /usr/bin/python2
%else
%global __python     /usr/bin/python3
%endif

%prep
%autosetup -p1
%{?_cov_prepare}

%build
./configure --xenopsd_libexecdir %{_libexecdir}/xenopsd --qemu_wrapper_dir=%{_libdir}/xen/bin --sbindir=%{_sbindir} --mandir=%{_mandir} --bindir=%{_bindir} --xapi_version=%{version} --prefix %{_prefix} --libdir %{ocaml_libdir}
export OCAMLPATH=%{_ocamlpath}
ulimit -s 16384 && COMPILE_JAVA=no %{?_cov_wrap} %{__make}
%{__make} doc
%{__make} sdk
sed -e "s|@LIBEXECDIR@|%{_libexecdir}|g" %{SOURCE25} > xapi-storage-script.conf

%if 0%{?build_python2}
(cd ocaml/xapi-storage/python && %{py2_build})
%endif

(cd ocaml/xapi-storage/python && %{py3_build})

%check
export OCAMLPATH=%{_ocamlpath}
COMPILE_JAVA=no %{__make} test %{!?build_python2:PY_TEST=NO}
mkdir %{buildroot}/testresults
find . -name 'bisect*.out' -exec cp {} %{buildroot}/testresults/ \;
ls %{buildroot}/testresults/

%install
rm -rf %{buildroot}
%global xapi_storage_path _build/default/ocaml/xapi-storage/python/
export OCAMLPATH=%{_ocamlpath}
DESTDIR=$RPM_BUILD_ROOT %{__make} install %{!?build_python2:BUILD_PY2=NO}

%if 0%{?build_python2}
(cd %{xapi_storage_path} && (%{py2_build}) && (%{py2_install}))
for f in XenAPI XenAPIPlugin inventory; do
    for e in py pyc pyo; do
        echo %{python2_sitelib}/$f.$e
    done
done > core-files
%{__install} -D -m 0644 ocaml/xcp-rrdd/scripts/rrdd/rrdd.py %{buildroot}/%{python2_sitelib}/
%endif

(cd %{xapi_storage_path} && (%{py3_build}) && (%{py3_install}))
for f in XenAPI XenAPIPlugin inventory observer; do
    echo %{python3_sitelib}/$f.py
    echo %{python3_sitelib}/__pycache__/$f.*
done >> core-files
echo "%{python3_sitelib}/xapi/__pycache__/__init__*.pyc" >> core-files
echo "%{python3_sitelib}/xapi_storage*.egg-info" >> core-files

%{__install} -D -m 0644 ocaml/xcp-rrdd/scripts/rrdd/rrdd.py %{buildroot}/%{python3_sitelib}/

ln -s /var/lib/xcp $RPM_BUILD_ROOT/var/xapi
mkdir $RPM_BUILD_ROOT/etc/xapi.conf.d
mkdir $RPM_BUILD_ROOT/etc/xcp

mkdir -p %{buildroot}/etc/xenserver/features.d
echo 0 > %{buildroot}/etc/xenserver/features.d/cluster_health
echo 0 > %{buildroot}/etc/xenserver/features.d/corosync3

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_tmpfilesdir}
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-rrdd.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/xcp-rrdd
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/xcp-rrdd.conf
%{__install} -D -m 0644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/xcp-rrdd.conf
%{__install} -D -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/xcp-rrdd-iostat.service
%{__install} -D -m 0644 %{SOURCE6} %{buildroot}%{_unitdir}/xcp-rrdd-squeezed.service
%{__install} -D -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/xcp-rrdd-xenpm.service

%{__install} -D -m 0644 %{SOURCE8} %{buildroot}%{_unitdir}/xenopsd-xc.service
%{__install} -D -m 0644 %{SOURCE9} %{buildroot}%{_unitdir}/xenopsd-simulator.service
%{__install} -D -m 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/sysconfig/xenopsd
%{__install} -D -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/xenopsd.conf

%{__install} -D -m 0644 %{SOURCE12} %{buildroot}%{_unitdir}/squeezed.service
%{__install} -D -m 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/sysconfig/squeezed
%{__install} -D -m 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/squeezed.conf

%{__install} -D -m 0644 %{SOURCE15} %{buildroot}%{_sysconfdir}/sysconfig/xcp-networkd
%{__install} -D -m 0644 %{SOURCE16} %{buildroot}%{_sysconfdir}/xensource/network.conf

%{__install} -D -m 0644 %{SOURCE17} %{buildroot}%{_unitdir}/message-switch.service
%{__install} -D -m 0644 %{SOURCE18} %{buildroot}%{_sysconfdir}/message-switch.conf

%{__install} -D -m 0644 %{SOURCE19} %{buildroot}%{_sysconfdir}/xensource/bugtool/message-switch.xml
%{__install} -D -m 0644 %{SOURCE20} %{buildroot}%{_sysconfdir}/xensource/bugtool/message-switch/stuff.xml
%{__install} -D -m 0644 %{SOURCE21} %{buildroot}%{_unitdir}/forkexecd.service
%{__install} -D -m 0644 %{SOURCE22} %{buildroot}%{_sysconfdir}/sysconfig/forkexecd

# Set server certificate file gid 204 (certusers)
sed -i -E 's#(ExecStart=.+/xapi-ssl.pem) +-1 #\1 204 #g' %{buildroot}%{_unitdir}/gencert.service

rm %{buildroot}%{_bindir}/gen_lifecycle
rm %{buildroot}/opt/xensource/bin/xe*-metadata
rm %{buildroot}/opt/xensource/libexec/backup-metadata-cron
rm %{buildroot}/opt/xensource/libexec/*-sr-metadata.py*

mkdir -p %{buildroot}%{_libexecdir}/xapi-storage-script/volume
mkdir -p %{buildroot}%{_libexecdir}/xapi-storage-script/datapath
%{__install} -D -m 0644 xapi-storage-script.conf %{buildroot}%{_sysconfdir}/xapi-storage-script.conf
%{__install} -D -m 0644 %{SOURCE23} %{buildroot}%{_unitdir}/xapi-storage-script.service
%{__install} -D -m 0644 %{SOURCE24} %{buildroot}%{_sysconfdir}/sysconfig/xapi-storage-script
rm %{buildroot}%{ocaml_libdir}/xapi-storage-script -rf
rm %{buildroot}%{ocaml_docdir}/xapi-storage-script -rf
%{?_cov_install}

%{__install} -D -m 0644 %{SOURCE26} %{buildroot}%{_sysconfdir}/xapi.conf.d/tracing.conf

# XCP-ng: remove the ptoken and accesstoken yum plugins
rm -f %{buildroot}/etc/yum/pluginconf.d/accesstoken.conf
rm -f %{buildroot}/etc/yum/pluginconf.d/ptoken.conf
rm -f %{buildroot}/usr/lib/yum-plugins/accesstoken.py
rm -f %{buildroot}/usr/lib/yum-plugins/ptoken.py

mkdir -p %{buildroot}%{_sysconfdir}/xapi.pool-recommendations.d
%{__install} -D -m 0644 %{SOURCE27} %{buildroot}%{_sysconfdir}/xapi.pool-recommendations.d/xapi.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n xenopsd
/usr/bin/getent passwd qemu >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    qemu >/dev/null 2>&1 || :
/usr/bin/getent passwd qemu_base >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    -u 65535 \
    qemu_base >/dev/null 2>&1 || :
# add swtpm_base with uid 65536 after vncterm_base uuid (131072), defined in vncterm.spec
/usr/bin/getent passwd swtpm_base >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    -u 196608 \
    swtpm_base >/dev/null 2>&1 || :


%pre -n xcp-rrdd
getent group rrdmetrics >/dev/null || groupadd -r rrdmetrics

%post core
%systemd_post cdrommon@.service
%systemd_post gencert.service
%systemd_post xapi-domains.service
%systemd_post perfmon.service
%systemd_post xapi.service
%systemd_post xapi-wait-init-complete.service
%systemd_post attach-static-vdis.service
%systemd_post save-boot-info.service
%systemd_post mpathalert.service
%systemd_post generate-iscsi-iqn.service
%systemd_post control-domain-params-init.service
%systemd_post network-init.service

# remove old stunnel config file
rm -f /etc/xensource/xapi-ssl.conf

# On upgrade, migrate from the old statefile to the new statefile so that
# services are not rerun.
if [ $1 -gt 1 ] ; then
    grep -q ^success /etc/firstboot.d/state/05-prepare-networking 2>/dev/null && touch /var/lib/misc/ran-network-init || :
    grep -q ^success /etc/firstboot.d/state/40-generate-iscsi-iqn 2>/dev/null && touch /var/lib/misc/ran-generate-iscsi-iqn || :
    grep -q ^success /etc/firstboot.d/state/50-prepare-control-domain-params 2>/dev/null && touch /var/lib/misc/ran-control-domain-params-init || :
fi

# systemd_post does not enable new services on update. Make sure
# recent services are enabled by default

systemctl preset xapi-wait-init-complete || :

# force rsyslog to reload open files to apply the new configuration
systemctl kill -s HUP rsyslog 2> /dev/null || true

%post -n xenopsd-xc
%systemd_post xenopsd-xc.service

%post -n xenopsd-simulator
%systemd_post xenopsd-simulator.service

%post -n squeezed
%systemd_post squeezed.service

%post -n xcp-rrdd
%systemd_post xcp-rrdd.service
%tmpfiles_create %{_tmpfilesdir}/xcp-rrdd.conf

%post -n rrdd-plugins
%systemd_post xcp-rrdd-iostat.service
%systemd_post xcp-rrdd-squeezed.service
%systemd_post xcp-rrdd-xenpm.service

%post -n xcp-networkd
%systemd_post xcp-networkd.service

%post -n message-switch
%systemd_post message-switch.service
if [ $1 -gt 1 ] ; then
  # upgrade from SysV, see http://0pointer.de/public/systemd-man/daemon.html
  # except %triggerun doesn't work since previous package had no systemd,
  # and don't transition in 2 steps
  if /sbin/chkconfig --level 5 message-switch ; then
    /bin/systemctl --no-reload enable message-switch.service >/dev/null 2>&1 || :
    /sbin/chkconfig --del message-switch >/dev/null 2>&1 || :
  else
    # remove broken symlinks that a previous version of the package may have forgotten to remove
    find /etc/rc.d -name "*message-switch" -delete >/dev/null 2>&1 || :
  fi
fi

%post -n forkexecd
%systemd_post forkexecd.service

%post storage-script
%systemd_post xapi-storage-script.service

%post -n wsproxy
%systemd_post wsproxy.service
%systemd_post wsproxy.socket

# systemd_post does not start new units on update. Make sure recent services
# are started.
systemctl start wsproxy.socket >/dev/null 2>&1 || :

%post nbd
%systemd_post xapi-nbd.service
%systemd_post xapi-nbd.path

%post -n varstored-guard
%systemd_post varstored-guard.service

%preun core
%systemd_preun cdrommon@.service
%systemd_preun gencert.service
%systemd_preun xapi-domains.service
%systemd_preun perfmon.service
%systemd_preun xapi.service
%systemd_preun xapi-wait-init-complete.service
%systemd_preun attach-static-vdis.service
%systemd_preun save-boot-info.service
%systemd_preun mpathalert.service
%systemd_preun generate-iscsi-iqn.service
%systemd_preun control-domain-params-init.service
%systemd_preun network-init.service

%preun -n xenopsd-xc
%systemd_preun xenopsd-xc.service

%preun -n xenopsd-simulator
%systemd_preun xenopsd-simulator.service

%preun -n squeezed
%systemd_preun squeezed.service

%preun -n xcp-rrdd
%systemd_preun xcp-rrdd.service

%preun -n rrdd-plugins
%systemd_preun xcp-rrdd-iostat.service
%systemd_preun xcp-rrdd-squeezed.service
%systemd_preun xcp-rrdd-xenpm.service

%preun -n xcp-networkd
%systemd_preun xcp-networkd.service

%preun -n message-switch
%systemd_preun message-switch.service

%preun -n forkexecd
%systemd_preun forkexecd.service

%preun storage-script
%systemd_preun xapi-storage-script.service

%preun -n wsproxy
%systemd_preun wsproxy.service
%systemd_preun wsproxy.socket

%preun nbd
%systemd_preun xapi-nbd.service
%systemd_preun xapi-nbd.path

%preun -n varstored-guard
%systemd_preun varstored-guard.service

%postun core
%systemd_postun cdrommon@.service
%systemd_postun xapi-domains.service
%systemd_postun perfmon.service
%systemd_postun xapi.service
%systemd_postun xapi-wait-init-complete.service
%systemd_postun attach-static-vdis.service
%systemd_postun save-boot-info.service
%systemd_postun mpathalert.service
%systemd_postun generate-iscsi-iqn.service
%systemd_postun control-domain-params-init.service
%systemd_postun network-init.service

%postun -n xenopsd-xc
%systemd_postun xenopsd-xc.service

%postun -n xenopsd-simulator
%systemd_postun_with_restart xenopsd-simulator.service

%postun -n squeezed
%systemd_postun squeezed.service

%postun -n xcp-rrdd
%systemd_postun xcp-rrdd.service

%postun -n rrdd-plugins
%systemd_postun xcp-rrdd-iostat.service
%systemd_postun xcp-rrdd-squeezed.service
%systemd_postun xcp-rrdd-xenpm.service

%postun -n xcp-networkd
%systemd_postun xcp-networkd.service

%postun -n message-switch
%systemd_postun message-switch.service

%postun -n forkexecd
%systemd_postun forkexecd.service

%postun storage-script
%systemd_postun xapi-storage-script.service

%postun -n wsproxy
%systemd_postun wsproxy.service
%systemd_postun wsproxy.socket

%postun nbd
%systemd_postun xapi-nbd.service
%systemd_postun xapi-nbd.path

%postun -n varstored-guard
%systemd_postun varstored-guard.service

# this would be done by %postun of old package, except old package wasn't
# using systemd, without this a systemctl restart message-switch would fail
# after an upgrade
%posttrans -n message-switch
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%files core -f core-files
%defattr(-,root,root,-)
/opt/xensource/bin/xapi
# XCP-ng: using %%config instead of upstream's %%config(noreplace)
# to ensure our defaults are applied
%config /etc/xapi.conf
/etc/logrotate.d/audit
/etc/pam.d/xapi
/etc/cron.d/xapi-tracing-log-trim.cron
/etc/cron.daily/license-check
/etc/cron.daily/certificate-check
/etc/cron.hourly/certificate-refresh
/opt/xensource/libexec/xapi-init
/opt/xensource/libexec/attach-static-vdis
/opt/xensource/libexec/save-boot-info
%config(noreplace) /etc/sysconfig/perfmon
%config(noreplace) /etc/sysconfig/xapi
/etc/xcp
/etc/xenserver/features.d
/etc/xapi.conf.d
/etc/xapi.d/base-path
/etc/xapi.d/plugins/IPMI.py
/etc/xapi.d/plugins/echo
/etc/xapi.d/plugins/extauth-hook
/etc/xapi.d/plugins/extauth-hook-AD.py
/etc/xapi.d/plugins/firewall-port
/etc/xapi.d/plugins/openvswitch-config-update
/etc/xapi.d/plugins/perfmon
/etc/xapi.d/plugins/power-on-host
/etc/xapi.d/plugins/wake-on-lan
/etc/xapi.d/plugins/wlan.py
/etc/xapi.d/plugins/install-supp-pack
/etc/xapi.d/plugins/disk-space
/etc/xapi.d/efi-clone
/etc/xapi.d/extensions
/etc/xapi.d/mail-languages/en-US.json
/etc/xapi.d/mail-languages/zh-CN.json
/etc/xapi.d/mail-languages/ja-JP.json
/etc/logrotate.d/xapi
%config(noreplace) /etc/xensource/db.conf
%config(noreplace) /etc/xensource/db.conf.rio
/etc/xensource/master.d/01-example
/etc/xensource/master.d/03-mpathalert-daemon
%config(noreplace) /etc/xensource/pool.conf
%{_sysconfdir}/systemd/system/stunnel@xapi.service.d/*-stunnel-*.conf
# XCP-ng: we don't need these configuration files that are specific to XS8's update process
#%%config(noreplace) /etc/yum/pluginconf.d/accesstoken.conf
#%%config(noreplace) /etc/yum/pluginconf.d/ptoken.conf
/opt/xensource/bin/update-ca-bundle.sh
/opt/xensource/bin/mpathalert
/opt/xensource/bin/perfmon
/opt/xensource/bin/static-vdis
/opt/xensource/bin/xapi-autostart-vms
/opt/xensource/bin/xapi-db-process
/opt/xensource/bin/xapi-wait-init-complete
/opt/xensource/bin/xe-edit-bootloader
/opt/xensource/bin/xe-get-network-backend
/opt/xensource/bin/xe-mount-iso-sr
/opt/xensource/bin/xe-reset-networking
/opt/xensource/bin/xe-scsi-dev-map
/opt/xensource/bin/xe-toolstack-restart
/opt/xensource/bin/xe-xentrace
/opt/xensource/bin/xe-switch-network-backend
/opt/xensource/bin/xe-enable-all-plugin-metrics
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
/etc/xensource/bugtool/observer.xml
/etc/xensource/bugtool/observer/stuff.xml
/opt/xensource/libexec/list_plugins
/opt/xensource/libexec/sm_diagnostics
/opt/xensource/libexec/xn_diagnostics
/opt/xensource/libexec/thread_diagnostics
/opt/xensource/libexec/block_device_io
/opt/xensource/libexec/cdrommon
/opt/xensource/libexec/alert-certificate-check
/opt/xensource/libexec/control-domain-params-init
/opt/xensource/libexec/daily-license-check
/opt/xensource/libexec/fence
/opt/xensource/libexec/generate-iscsi-iqn
/opt/xensource/libexec/gencert
/opt/xensource/libexec/host-backup
/opt/xensource/libexec/host-bugreport-upload
/opt/xensource/libexec/host-display
/opt/xensource/libexec/host-restore
/opt/xensource/libexec/link-vms-by-sr.py
/opt/xensource/libexec/logs-download
/opt/xensource/libexec/pbis-force-domain-leave
/opt/xensource/libexec/mail-alarm
/opt/xensource/libexec/nbd-firewall-config.sh
/opt/xensource/libexec/nbd_client_manager.py
/opt/xensource/libexec/network-init
/opt/xensource/libexec/print-custom-templates
/opt/xensource/libexec/probe-device-for-file
/opt/xensource/libexec/reset-and-reboot
/opt/xensource/libexec/set-hostname
/opt/xensource/libexec/shell.py
/opt/xensource/libexec/update-mh-info
/opt/xensource/libexec/upload-wrapper
/opt/xensource/libexec/xapi-health-check
/opt/xensource/libexec/xapi-tracing-log-trim.sh
/opt/xensource/libexec/xapi-rolling-upgrade
/opt/xensource/libexec/xha-lc
/opt/xensource/libexec/xe-syslog-reconfigure
/opt/xensource/libexec/usb_reset.py
/opt/xensource/libexec/usb_scan.py
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
# XCP-ng: we don't need these plugins that are specific to XS8's update process
#/usr/lib/yum-plugins/accesstoken.py
#/usr/lib/yum-plugins/ptoken.py
%{_unitdir}/cdrommon@.service
%{_unitdir}/gencert.service
%{_unitdir}/xapi-domains.service
%{_unitdir}/perfmon.service
%{_unitdir}/xapi.service
%{_unitdir}/xapi-wait-init-complete.service
%{_unitdir}/xapi-init-complete.target
%{_unitdir}/attach-static-vdis.service
%{_unitdir}/save-boot-info.service
%{_unitdir}/mpathalert.service
%{_unitdir}/generate-iscsi-iqn.service
%{_unitdir}/control-domain-params-init.service
%{_unitdir}/network-init.service
%config(noreplace) %{_sysconfdir}/xapi.conf.d/tracing.conf
%config(noreplace) %{_sysconfdir}/xapi.pool-recommendations.d/xapi.conf
%{_bindir}/xs-trace

%if 0%{include_pyc_pyo}
/etc/xapi.d/plugins/IPMI.pyo
/etc/xapi.d/plugins/IPMI.pyc
/etc/xapi.d/plugins/extauth-hook-AD.pyo
/etc/xapi.d/plugins/extauth-hook-AD.pyc
/etc/xapi.d/plugins/wlan.pyo
/etc/xapi.d/plugins/wlan.pyc
/opt/xensource/libexec/link-vms-by-sr.pyo
/opt/xensource/libexec/link-vms-by-sr.pyc
/opt/xensource/libexec/nbd_client_manager.pyo
/opt/xensource/libexec/nbd_client_manager.pyc
/opt/xensource/libexec/shell.pyo
/opt/xensource/libexec/shell.pyc
/opt/xensource/libexec/usb_reset.pyo
/opt/xensource/libexec/usb_reset.pyc
/opt/xensource/libexec/usb_scan.pyo
/opt/xensource/libexec/usb_scan.pyc
# XCP-ng: we don't need these plugins that are specific to XS8's update process
#/usr/lib/yum-plugins/accesstoken.pyo
#/usr/lib/yum-plugins/accesstoken.pyc
#/usr/lib/yum-plugins/ptoken.pyo
#/usr/lib/yum-plugins/ptoken.pyc
%endif


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
%{ocaml_libdir}/xen-api-client/*
%exclude %{ocaml_libdir}/xen-api-client/*.cmt
%{ocaml_libdir}/xen-api-client-lwt/*
%exclude %{ocaml_libdir}/xen-api-client-lwt/*.cmt
%{ocaml_libdir}/xen-api-client-async/*
%exclude %{ocaml_libdir}/xen-api-client-async/*.cmt

%files datamodel-devel
%defattr(-,root,root,-)
%{ocaml_libdir}/xapi-datamodel/*
%exclude %{ocaml_libdir}/xapi-datamodel/*.cmt
%exclude %{ocaml_libdir}/xapi-datamodel/*.cmti
%{ocaml_libdir}/xapi-schema/*
%exclude %{ocaml_libdir}/xapi-schema/*.cmt
%exclude %{ocaml_libdir}/xapi-schema/*.cmti

%files rrd2csv
%defattr(-,root,root,-)
/opt/xensource/bin/rrd2csv
/opt/xensource/man/man1/rrd2csv.1

%files doc
%defattr(-,root,root,-)
%{_datarootdir}/xapi/doc/*
%exclude %{ocaml_docdir}/*

%files sdk
%{_datarootdir}/xapi/sdk/*
%exclude %{_datarootdir}/xapi/sdk/*/dune
%if 0%{include_pyc_pyo}
%exclude %{_datarootdir}/xapi/sdk/python/*.pyc
%exclude %{_datarootdir}/xapi/sdk/python/*.pyo
%exclude %{_datarootdir}/xapi/sdk/python/samples/*.pyc
%exclude %{_datarootdir}/xapi/sdk/python/samples/*.pyo
%endif

%files libs-devel
%defattr(-,root,root,-)
%{ocaml_libdir}/clock/*
%exclude %{ocaml_libdir}/clock/*.cmt
%exclude %{ocaml_libdir}/clock/*.cmti

%{ocaml_libdir}/gzip/*
%exclude %{ocaml_libdir}/gzip/*.cmt
%exclude %{ocaml_libdir}/gzip/*.cmti

%{ocaml_libdir}/http-lib/*
%exclude %{ocaml_libdir}/http-lib/*.cmt
%exclude %{ocaml_libdir}/http-lib/*.cmti

%{ocaml_libdir}/xapi-tracing/*
%exclude %{ocaml_libdir}/xapi-tracing/*.cmt
%exclude %{ocaml_libdir}/xapi-tracing/*.cmti

%{ocaml_libdir}/xapi-tracing-export/*
%exclude %{ocaml_libdir}/xapi-tracing-export/*.cmt
%exclude %{ocaml_libdir}/xapi-tracing-export/*.cmti

%{ocaml_libdir}/pciutil/*
%exclude %{ocaml_libdir}/pciutil/*.cmt
%exclude %{ocaml_libdir}/pciutil/*.cmti

%{ocaml_libdir}/sexpr/*
%exclude %{ocaml_libdir}/sexpr/*.cmt
%exclude %{ocaml_libdir}/sexpr/*.cmti

%{ocaml_libdir}/stunnel/*
%exclude %{ocaml_libdir}/stunnel/*.cmt
%exclude %{ocaml_libdir}/stunnel/*.cmti

%{ocaml_libdir}/uuid/*
%exclude %{ocaml_libdir}/uuid/*.cmt
%exclude %{ocaml_libdir}/uuid/*.cmti

%{ocaml_libdir}/xml-light2/*
%exclude %{ocaml_libdir}/xml-light2/*.cmt
%exclude %{ocaml_libdir}/xml-light2/*.cmti

%{ocaml_libdir}/zstd/*
%exclude %{ocaml_libdir}/zstd/*.cmt
%exclude %{ocaml_libdir}/zstd/*.cmti

%{ocaml_libdir}/xapi-compression/*
%exclude %{ocaml_libdir}/xapi-compression/*.cmt
%exclude %{ocaml_libdir}/xapi-compression/*.cmti

%{ocaml_libdir}/xapi-log/*
%exclude %{ocaml_libdir}/xapi-log/*.cmt
%exclude %{ocaml_libdir}/xapi-log/*.cmti

%{ocaml_libdir}/xapi-open-uri/*
%exclude %{ocaml_libdir}/xapi-open-uri/*.cmt
%exclude %{ocaml_libdir}/xapi-open-uri/*.cmti

%{ocaml_libdir}/safe-resources/*
%exclude %{ocaml_libdir}/safe-resources/*.cmt
%exclude %{ocaml_libdir}/safe-resources/*.cmti

%{ocaml_libdir}/cohttp-posix/*
%exclude %{ocaml_libdir}/cohttp-posix/*.cmt
%exclude %{ocaml_libdir}/cohttp-posix/*.cmti

%{ocaml_libdir}/xapi-expiry-alerts/*
%exclude %{ocaml_libdir}/xapi-expiry-alerts/*.cmt
%exclude %{ocaml_libdir}/xapi-expiry-alerts/*.cmti

%{ocaml_libdir}/xapi-inventory/*
%exclude %{ocaml_libdir}/xapi-inventory/*.cmt
%exclude %{ocaml_libdir}/xapi-inventory/*.cmti

%{ocaml_libdir}/xapi-stdext-date/*
%exclude %{ocaml_libdir}/xapi-stdext-date/*.cmt
%exclude %{ocaml_libdir}/xapi-stdext-date/*.cmti

%{ocaml_libdir}/xapi-stdext-encodings/*
%exclude %{ocaml_libdir}/xapi-stdext-encodings/*.cmt
%exclude %{ocaml_libdir}/xapi-stdext-encodings/*.cmti

%{ocaml_libdir}/xapi-stdext-pervasives/*
%exclude %{ocaml_libdir}/xapi-stdext-pervasives/*.cmt
%exclude %{ocaml_libdir}/xapi-stdext-pervasives/*.cmti

%{ocaml_libdir}/xapi-stdext-std/*
%exclude %{ocaml_libdir}/xapi-stdext-std/*.cmt
%exclude %{ocaml_libdir}/xapi-stdext-std/*.cmti

%{ocaml_libdir}/xapi-stdext-threads/*
%exclude %{ocaml_libdir}/xapi-stdext-threads/*.cmt
%exclude %{ocaml_libdir}/xapi-stdext-threads/*.cmti

%{ocaml_libdir}/xapi-stdext-unix/*
%exclude %{ocaml_libdir}/xapi-stdext-unix/*.cmt
%exclude %{ocaml_libdir}/xapi-stdext-unix/*.cmti

%{ocaml_libdir}/xapi-stdext-zerocheck/*
%exclude %{ocaml_libdir}/xapi-stdext-zerocheck/*.cmt
%exclude %{ocaml_libdir}/xapi-stdext-zerocheck/*.cmti

%{ocaml_libdir}/xapi-rrd/*
%exclude %{ocaml_libdir}/xapi-rrd/*.cmt
%exclude %{ocaml_libdir}/xapi-rrd/*.cmti

%files -n xenopsd
%{_sysconfdir}/udev/rules.d/xen-backend.rules
%{_libdir}/xen/bin/qemu-wrapper
%{_libdir}/xen/bin/pygrub-wrapper
%{_libdir}/xen/bin/swtpm-wrapper
%{_libexecdir}/xenopsd/vif
%{_libexecdir}/xenopsd/vif-real
%{_libexecdir}/xenopsd/block
%{_libexecdir}/xenopsd/tap
%{_libexecdir}/xenopsd/qemu-vif-script
%{_libexecdir}/xenopsd/setup-vif-rules
%{_libexecdir}/xenopsd/setup-pvs-proxy-rules
%{_libexecdir}/xenopsd/pvs-proxy-ovs-setup
%{_libexecdir}/xenopsd/common.py
%{_libexecdir}/xenopsd/igmp_query_injector.py
%config(noreplace) %{_sysconfdir}/sysconfig/xenopsd
%config(noreplace) %{_sysconfdir}/xenopsd.conf
%if 0%{include_pyc_pyo}
%{_libexecdir}/xenopsd/common.pyo
%{_libexecdir}/xenopsd/common.pyc
%{_libexecdir}/xenopsd/igmp_query_injector.pyo
%{_libexecdir}/xenopsd/igmp_query_injector.pyc
%endif

%exclude %{ocaml_dir}

%files -n xenopsd-xc
%{_sbindir}/xenopsd-xc
%{_unitdir}/xenopsd-xc.service
%{_mandir}/man1/xenopsd-xc.1.gz
%{_libexecdir}/xenopsd/set-domain-uuid
/opt/xensource/libexec/fence.bin
/opt/xensource/debug/suspend-image-viewer
%{_bindir}/list_domains

%files -n xenopsd-cli
%{_sbindir}/xenops-cli
%{_mandir}/man1/xenops-cli.1.gz

%files -n xenopsd-simulator
%{_sbindir}/xenopsd-simulator
%{_unitdir}/xenopsd-simulator.service
%{_mandir}/man1/xenopsd-simulator.1.gz

%files -n squeezed
%{_sbindir}/squeezed
%{_unitdir}/squeezed.service
%config(noreplace) %{_sysconfdir}/sysconfig/squeezed
%config(noreplace) %{_sysconfdir}/squeezed.conf

%files -n xcp-rrdd
%{_sbindir}/xcp-rrdd
%{_unitdir}/xcp-rrdd.service
%{_bindir}/rrd-cli
%config(noreplace) %{_sysconfdir}/sysconfig/xcp-rrdd
%config(noreplace) %{_sysconfdir}/xcp-rrdd.conf
%{_tmpfilesdir}/xcp-rrdd.conf
%if 0%{?build_python2}
%{python2_sitelib}/rrdd.py*
%endif
%{python3_sitelib}/rrdd.py*
%{python3_sitelib}/__pycache__/rrdd.*.pyc

%files -n xcp-rrdd-devel
%{ocaml_docdir}/rrd-transport/*
%{ocaml_docdir}/rrdd-plugin/*
%{ocaml_libdir}/rrd-transport/*
%{ocaml_libdir}/rrdd-plugin/*
%{_bindir}/rrdreader
%{_bindir}/rrdwriter
%{_bindir}/rrddump

%files -n rrdd-plugins
/etc/logrotate.d/xcp-rrdd-plugins
/etc/sysconfig/xcp-rrdd-plugins
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-iostat
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-squeezed
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-xenpm
/etc/xensource/bugtool/xcp-rrdd-plugins.xml
/etc/xensource/bugtool/xcp-rrdd-plugins/stuff.xml
%{_unitdir}/xcp-rrdd-iostat.service
%{_unitdir}/xcp-rrdd-squeezed.service
%{_unitdir}/xcp-rrdd-xenpm.service

%files -n vhd-tool
%{_bindir}/vhd-tool
/etc/sparse_dd.conf
/usr/libexec/xapi/sparse_dd
/usr/libexec/xapi/get_vhd_vsize
/opt/xensource/libexec/get_nbd_extents.py
/opt/xensource/libexec/python_nbd_client.py
%if 0%{include_pyc_pyo}
/opt/xensource/libexec/get_nbd_extents.pyc
/opt/xensource/libexec/get_nbd_extents.pyo
/opt/xensource/libexec/python_nbd_client.pyc
/opt/xensource/libexec/python_nbd_client.pyo
%endif

%files -n xcp-networkd
%{_sbindir}/xcp-networkd
%{_bindir}/networkd_db
%{_unitdir}/xcp-networkd.service
%{_mandir}/man1/xcp-networkd.1.gz
%config(noreplace) %{_sysconfdir}/sysconfig/xcp-networkd
%config(noreplace) %{_sysconfdir}/xcp-networkd.conf
%config(noreplace) %{_sysconfdir}/xensource/network.conf

%files -n message-switch
%{_unitdir}/message-switch.service
%{_sbindir}/message-switch
%{_sbindir}/message-cli
/usr/bin/gpumon-cli
%config(noreplace) /etc/message-switch.conf
/etc/xensource/bugtool/message-switch/stuff.xml
/etc/xensource/bugtool/message-switch.xml

%files -n message-switch-devel
%doc %{ocaml_docdir}/message-switch/LICENSE
%doc %{ocaml_docdir}/message-switch/README.markdown
%defattr(-,root,root,-)
%{ocaml_docdir}/message-switch-core
%{ocaml_docdir}/message-switch-unix
%{ocaml_docdir}/message-switch-async
%{ocaml_docdir}/message-switch-lwt
%{ocaml_docdir}/message-switch-cli
%{ocaml_docdir}/message-switch
%{ocaml_libdir}/message-switch
%{ocaml_libdir}/message-switch-cli
%{ocaml_libdir}/message-switch-core
%{ocaml_libdir}/message-switch-unix
%{ocaml_libdir}/message-switch-async
%{ocaml_libdir}/message-switch-lwt
%exclude %{ocaml_libdir}/*/*.cmt
%exclude %{ocaml_libdir}/*/*.cmti

%files idl-devel
%{ocaml_docdir}/xapi-idl
%{_bindir}/xcp-idl-debugger
%{ocaml_libdir}/xapi-idl
%{ocaml_libdir}/stublibs/*.so

%files -n forkexecd
%{ocaml_docdir}/xapi-forkexecd/LICENSE
%{_sbindir}/forkexecd
%{_sbindir}/forkexecd-cli
%{_unitdir}/forkexecd.service
%config(noreplace) %{_sysconfdir}/sysconfig/forkexecd

%files -n forkexecd-devel
%{ocaml_libdir}/xapi-forkexecd
%{ocaml_libdir}/forkexec
%{ocaml_docdir}/forkexec
%{ocaml_docdir}/xapi-forkexecd
# part of the main package
%exclude %{ocaml_docdir}/xapi-forkexecd/LICENSE

%files storage-ocaml-plugin-runtime
%defattr(-,root,root,-)
%{ocaml_libdir}/xapi-storage/*
%exclude %{ocaml_libdir}/xapi-storage/*.a
%exclude %{ocaml_libdir}/xapi-storage/*.cmt
%exclude %{ocaml_libdir}/xapi-storage/*.cmx
%exclude %{ocaml_libdir}/xapi-storage/*.cmxa
%exclude %{ocaml_libdir}/xapi-storage/*.ml

%files storage-ocaml-plugin-devel
%defattr(-,root,root,-)
%{ocaml_docdir}/xapi-storage/*
%{ocaml_libdir}/xapi-storage/*
%exclude %{ocaml_libdir}/xapi-storage/*.cma
%exclude %{ocaml_libdir}/xapi-storage/*.cmi
%exclude %{ocaml_libdir}/xapi-storage/*.cmt
%exclude %{ocaml_libdir}/xapi-storage/*.cmxs
%exclude %{ocaml_libdir}/xapi-storage/*.ml

%files storage-script
%{_libexecdir}/xapi-storage-script
%{_sbindir}/xapi-storage-script
%{_mandir}/man8/xapi-storage-script.8*
%{_unitdir}/xapi-storage-script.service
%config(noreplace) %{_sysconfdir}/sysconfig/xapi-storage-script
%config(noreplace) %{_sysconfdir}/xapi-storage-script.conf

%files -n sm-cli
%{_sbindir}/sm-cli

%files -n wsproxy
/opt/xensource/libexec/wsproxy
%{_unitdir}/wsproxy.service
%{_unitdir}/wsproxy.socket

%files nbd
%{_sbindir}/xapi-nbd
%{_unitdir}/xapi-nbd.service
%{_unitdir}/xapi-nbd.path

%files -n varstored-guard
%license LICENSE
%{_sbindir}/varstored-guard
%{_unitdir}/varstored-guard.service
%{_bindir}/xapiguard_cli

%if 0%{?coverage:1}
%package testresults
Summary: Coverage files from unit tests
%description testresults
Coverage files from unit tests

%files testresults
%defattr(-,root,root,-)
/testresults
%endif

%{?_cov_results_package}

%changelog
* Thu Feb 06 2025 Lucas Ravagnier <lucas.ravagnier@vates.tech> - 24.19.2-1.10
- add secure_client_initated_renegotiation_false.patch
  to disable a renegociation in stunnel.

* Thu Oct 10 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.9
- Add xapi-24.19-2-fix-pem-fingerprint-startup.XCP-ng.patch

* Tue Oct 01 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.8
- Add xapi-24.19.2-ipv6-virtual-pif.XCP-ng.patch

* Tue Sep 24 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.7
- Add xapi-24.19.2-ipv6-pool-eject.XCP-ng.patch

* Tue Sep 24 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.6
- Add xapi-24.19.2-keep-ipv6-management-disable.XCP-ng.patch

* Fri Sep 20 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.5
- Add xapi-24.19.2-keep-address-type-network-reset.XCP-ng.patch

* Wed Sep 18 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.4
- Add xapi-24.19.2-ipv6-reset-networking.XCP-ng.patch

* Wed Aug 28 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 24.19.2-1.3
- Add xapi-24.19.2-update-new-fingerprint-fields-on-DB-upgrade.backport.patch, backported from XAPI project
- Add xapi-24.19.2-more-fingerprint-field-updates-fixes.XCP-ng.patch to complement the fix
- Fixes an issue where new fingerprint fields are not populated, which under
  some circumstances makes pool join fail.

* Wed Aug 14 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.2
- Add xapi-24.19.2-fix-ipv6-import.XCP-ng.patch

* Tue Aug 13 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.19.2-1.1
- Rebase on 24.19.2-1
- Drop xapi-24.11.0-sb-state-api.XCP-ng.patch
- Drop xapi-24.11.0-don-t-generate-link-local-address-for-interfaces.patch
- Drop xapi-23.31.0-fix-ipv6-import.XCP-ng.patch
- *** Upstream changelog ***
- * Tue Jul 16 2024 Ming Lu <ming.lu@cloud.com> - 24.19.2-1
- - CA-395626: Fix (server status report generation report)
- * Tue Jul 09 2024 Ming Lu <ming.lu@cloud.com> - 24.19.1-1
- - Fixes: 99c43569a0 ("Transition from exception-raising Unix.getenv to Sys.getenv_opt with")
- * Tue Jul 09 2024 Ming Lu <ming.lu@cloud.com> - 24.19.0-1
- - CP-47304: [Toolstack] - Add data model for anti-affinity group
- - CP-47655: [Toolstack] - Associate/disassociate VM to/from anti-affinity group
- - CA-391880: Update related field 'groups' of VM when destroying VM group.
- - CP-47302: VM start with anti-affinity
- - CA-392177: Keep current group after reverting from snapshot
- - CP-47656 Anti-affinity feature generate alert
- - CP-48570: Load recommendations from config file when Xapi starts
- - CP-48011: Xapi Support anti-affinity feature flag
- - CA-393421: Special VMs cannot be added to VM groups
- - CP-48625: Code refactoring
- - opam: add psq to xapi dependencies
- - CP-49665: Anti-affinity support for host evacuation
- - CP-48752: Add UT for host evacuation with anti-affinity support
- - CP-49953: Remove parse_uri, switch to using Uri module instead
- - doc: remaining API docs
- - doc: add XenAPI release info
- - Printf.kprintf is deprecated, replace with Printf.ksprintf
- - Fix misplaced inline attributes
- - CP-50050 track CBT status for SMAPIv3 SRs
- - CP-49953: Remove parse_uri, switch to using Uri module instead
- - CI: Complete parallel Coveralls uploads: Finish when done
- - CP-49116: Replace fingerprint in certificate DB with sha256 and sha1
- - CA-392887: set_tls_config immediately after enabling clustering
- - CI: Update endcover step to v2 to fix CI (#5763)
- - CA-386173: Update the message of WLB authentication issue
- - Revert "CP-49953: Remove parse_uri, switch to using Uri module instead"
- - Fix a bug noticed by a quicktest run
- - Eliminate unnecessary usage of List.length to check for empty lists
- - Transition from exception-raising Unix.getenv to Sys.getenv_opt with
- - Replace Hashtbl.find with Hashtbl.find_opt in trivial cases
- - Refactor Hashtbl.find out of resources/table.ml
- - Refactor Hashtbl.find out of xenopsd/xc/readln.ml
- - Add a gate for Hashbtl.find
- - CP-50135: Bump datamodel_lifecycle for anti-affinity
- - IH-621: Add IPMI host power on support and remove DRAC
- - opam: generate xapi-forkexecd with dune
- - opam: remove unversioned opam dependencies
- - opam: generate xapi-networkd using dune
- - fe_test: print stacktrace on unit test failure
- - fix(fe_test): make it compatible with fd-send-recv 2.0.2
- - Fix indentation in C code
- * Mon Jul 01 2024 Ming Lu <ming.lu@cloud.com> - 24.18.0-1
- - doc/README.md: Improve the Hugo Quick start guide for an easier start
- - .codecov.yml: Remove scripts (Codecov is confused, we move scripts/ to python3/)
- - CA-394444: Update task cancellation in `message_forwarding.ml`
- - Hugo docs: Add dark mode support, theme variant selector and print
- - Don't generate link-local address for interfaces
- - Make `cluster-stack-version` show up in the CLI
- - Update datamodel lifecycle
- - Removed headers from the templates.
- - Renamed files and reordered table of contents.
- - IH-583 Create standalone implementations of systemd functions
- - Fix failing builds by attaching package to the cram test
- - CA-394883: fix race condition allocating task ids
- - CA-394882: avoid error on tasks that are not ours
- - CA-381119: use JsonRPC V2 for error replies
- - CA-394169: Allow task to have permissions on itself
- - CI: use new version of codecov action
- - Merge .codecov.yml from feature/py3 to drop scripts checks
- - CP-50055 Add Go SDK as a release package in XAPI
- - CI: codecov is unstable, use coveralls
- - CA-394921: Ignore unkown properties during Java SDK deserialisation
- - CP-49446: expose SR health values to Python
- - opam: record correct authorship for stdext packages
- - IH-628: add new package clock for timekeeping
- * Tue Jun 18 2024 Ming Lu <ming.lu@cloud.com> - 24.17.0-1
- - CP-48666: initialize a skeleton project for Go SDK
- - CP-47347: Add mustache template for Enum Types
- - CP-47351: generate Record and Ref Type Golang code for all classes
- - CP-47348: generate Golang code of Enum Type for all classes
- - CP-47362: generate file headers
- - CP-48666: collect api errors
- - CP-47364: generate api messages and errors of Golang code
- - refactor: create an `Alcotest.testable` to check structure of generated JSON is wanted
- - refactor: move `objects` and `session_id` from `Gen_go_helper` to `CommonFunctions`
- - CP-48666: use dune rule to get the destination dir for the generated files
- - CP-48666: generate all enums to a file
- - refactor the way of getting enums
- - CP-48666: refactor the JSON schema checking
- - CP-48666: refactor `render_template` with an optional newline parameter
- - CP-47361: generate mustache template for deserialize and serialize functions
- - CP-47358: Generate convert functions Go code
- - CP-48855: update templates (APIErrors, APIMessages, Record)
- - CP-48855: adjust generated json for templates changed
- - CP-48855: add templates for option and APIVersions
- - CP-48855: render options
- - CP-47355, CP-47360: generate mustache template for xapi data module class messages
- - CP-47354: Generate messages functions Golang code for all classes
- - CP-47354: add unit tests for `func_name_suffix` and `string_of_ty_with_enums`
- - CP-48855: render APIVersion
- - CP-48855: fix go lint var-naming warnings
- - fix `StringOfTyWithEnumsTest` after merged
- - CP-48855: it should be only one empty line at end of Go file
- - CP-47356: expose `published_release_for_param` and `compare_versions` for usage of other modules
- - CP-47358: Add unit tests for generating convert functions
- - CP-47355, CP-47360: generate mustache template for xapi data module class messages
- - CP-47354: Generate messages functions Golang code for all classes
- - CP-47354: add unit tests for `func_name_suffix` and `string_of_ty_with_enums`
- - CP-48855: update templates (APIErrors, APIMessages, Record)
- - CP-48855: adjust generated json for templates changed
- - CP-48855: add templates for option and APIVersions
- - CP-48855: render options
- - CP-48855: render APIVersion
- - CP-48855: remove go lint var-naming warnings
- - CP-47356: Support backwards capability for Go SDK
- - CP-47361: generate mustache template for deserialize and serialize functions
- - CP-47358: Generate convert functions Go code
- - CP-47358: Add unit tests for generating convert functions
- - CP-47354: Generate messages functions Golang code for all classes
- - CP-47354: add unit tests for `func_name_suffix` and `string_of_ty_with_enums`
- - CP-48855: render options
- - CP-48855: render APIVersion
- - CP-47357: Add a Go JSON-RPC client file
- - CP-47357: fix review issues
- - CP-47367 Add type checking for generated SDK Go files
- - CP-49350: fix variable naming in Go SDK
- - Set up Github Action for go SDK component test (#5588)
- - CA-391381: Avoid errors for Partial Callables in observer.py
- - xapi-tracing: bind its test to the package
- - opam: generate xapi-tracing with dune
- - opam: generate xapi-tracing-export with dune
- - opam: generate rrdd-plugin with dune
- - opam: generate xapi-rrd-transport-utils with dune
- - opam: generate xapi-rrdd with dune
- - opam: drop xapi-rrd-transport
- - opam: drop xen-api-sdk
- - Revert "CP-47660 define anti-affinity feature"
- - Remove CVM and relevant test cases (#5655)
- - opam: Fix metadata
- - opam: de-templatise message-switch-core
- - ocaml: remove unused bindings
- - dune: enforce version +3
- - Add `VM.set_uefi_mode` API call
- - Go SDK: Misc fixes for on-going component tests (#5661)
- - Add `VM.get_secureboot_readiness` API call
- - Add `Pool.get_guest_secureboot_readiness` API call
- - CP-49446: Update SR health to include new constructors
- - doc: copy design documents from xapi-project.github.io
- - doc: add info table to design docs
- - doc: style design doc index
- - CP-47928: Add component test for Go SDK
- - CP-49647 use URI for create_misc
- - CP-49647 use URI for dbsync_master
- - CP-49647 use URI for export.ml
- - CP-49647 use URI for import.ml
- - CP-49647 use URI for importexport.ml
- - CP-49647 use URI for rrd_proxy.ml
- - CP-49647 use URI for sm_fs_ops.ml
- - CP-49647 use URI for xapi_message.ml
- - CP-49647 use URI for xapi_xenops.ml
- - CP-49647 use URI for xapi_vm_migrate.ml
- - CP-49647 use URI for xapi_host.ml
- - CP-49647 use URI for cli_util.ml
- - CP-49647 use URI for http.ml
- - CP-49647 use URI for cli_operations
- - CP-45235: Support for `xe-cli` to transmit `traceparent`
- - doc: add design review links (historical)
- - doc: RDP design: fix list nesting
- - CP-48995: Instrument `XenAPI.py` to submit traceparent
- - Update datamodel_lifecycle.ml
- - CP-49768: Update GO SDK README file (#5671)
- - CP-49249: Implement SMAPIv3 CBT Forwarding
- - CA-393866: Add support for Infinity in Java SDK parser
- - CA-393507: Default cluster_stack value
- - Remove fix_firewall.sh
- - CA-393119: Don't use HTTPS for localhost migrations
- - CP-49828: Remove iovirt script
- - CP-49129: Add unit test for parallel parsing.
- - CP-49129: Make unit test run on alcotest.
- - CP-49129: Replace `ocamlyacc` with `menhir`
- - CP-49129: Drop global lock around sexpr parsing
- - CP-49045: replace all uses of ocamlyacc with menhir which is thread-safe
- - CP-49129: Update `quality-gate.sh` for `ocamlyacc`
- - Link just qcheck-core, not qcheck
- - Define qcheck-core dependency in opam packages
- - Makefile: fix compatibility with the dash shell
- - CP-49858: Fix phrasing in readme
- - CP-49858: Add licence text on top of Go source files
- - CP-49858: Unit test: licence template variable
- - CP-49858: Remove template variables 'first' and 'is_session_id'
- - CP-49858: Unit test: Update for changes on template variables
- - rpm: remove `sexprpp` from public_name
- - sexpr: add tests to the package
- - xapi-rrdd: change tests to reduce amount of logs produced
- - rrd-transport: generate opam metadata using dune
- - http-lib: generate opam metadata using dune
- - wsproxy: test with alcotest instead of ounit
- - vhd-format-lwt: run tests using alcotest
- - xen-api-client: run tests with alcotest
- - xapi-sdk: add empty packge to be able to run tests for it
- - CI: pin packages
- - CP-49647 use URI for newcli.ml
- - CP-49677 implement Http.Url using URI
- - Update quality-gate.sh
- * Mon Jun 10 2024 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 24.16.0-3
- - Bump release and rebuild
- - Remove vm_anti_affinity tag and dependency on m2crypto

* Wed Aug 07 2024 Yann Dirson <yann.dirson@vates.tech> - 24.16.0-1.3
- Fix openvswitch-config-update not fully ported to python3

* Fri Jul 05 2024 Samuel Verschelde <stormi-xcp@ylix.fr> - 24.16.0-1.2
- Require python2-pyudev instead of python-pyudev
- It's best to require by the actual package name to avoid ambiguities,
  and we switched from python-pyudev to python2-pyudev in our repos

* Fri Jun 21 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.16.0-1.1
- Rebase on 24.16.0-1
- Drop xapi-24.11.0-disable-fileserver-option.XCP-ng.patch
- Rebase changelog on upstream changelog
- *** Former XCP-ng 8.3 changelog ***
- * Wed Jun 19 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.14.0-1.1
- - Rebase on 24.14.0-1
- - Drop xapi-23.3.0-filter-link-local-address-ipv6.XCP-ng.patch
- - Drop xapi-23.31.0-fix-ipv6-get-primary-address.XCP-ng.patch
- - Drop xapi-23.31.0-use-lib-guess-content-type.XCP-ng.patch
- - Drop xapi-23.31.0-xapi-service-depends-on-systemd-tmpfiles-setup.patch
- - Drop xapi-24.11.0-pci-passthrough.XCP-ng.patch
- * Fri May 31 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.11.0-1.5
- - Add xapi-24.11.0-sb-state-api.XCP-ng.patch
- * Thu May 16 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.11.0-1.4
- - Add xapi-24.11.0-disable-fileserver-option.XCP-ng.patch
- * Mon Apr 22 2024 Benjamin Reis <benjamin.reis@vates.tech> - 24.11.0-1.3
- - Add xapi-24.11.0-pci-passthrough.XCP-ng.patch
- * Thu Apr 18 2024 Damien Thenot <damien.thenot@vates.tech> - 24.11.0-1.2
- - Add largeblock to sm-plugins in xapi.conf
- * Wed Apr 03 2024 Benjamin Reis <benjamin.reis@vates.tech> - 23.31.0-1.7
- - Add xapi-23.31.0-use-lib-guess-content-type.XCP-ng.patch
- * Mon Feb 26 2024 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 23.31.0-1.6
- - Add xapi-23.31.0-xapi-service-depends-on-systemd-tmpfiles-setup.patches
- * Wed Feb 14 2024 Benjamin Reis <benjamin.reis@vates.tech> - 23.31.0-1.5
- - Add xapi-23.31.0-fix-ipv6-get-primary-address.XCP-ng.patch
- * Wed Feb 14 2024 Yann Dirson <yann.dirson@vates.tech> - 23.31.0-1.4
- - Rebuild with xs-opam-repo-6.74.0-1.2
- * Thu Feb 08 2024 Benjamin Reis <benjamin.reis@vates.tech> - 23.31.0-1.3
- - Add xapi-23.31.0-fix-ipv6-import.XCP-ng.patch
- * Tue Dec 12 2023 Benjamin Reis <benjamin.reis@vates.tech> - 23.25.0-1.6
- - Add xapi-23.25.0-extend-uefi-cert-api.patch
- - Update xapi-23.25.0-update-xapi-conf.XCP-ng.patch
- * Wed Oct 25 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 23.25.0-1.4
- - Set override-uefi-certs=true in xapi.conf
- - Update xapi-23.25.0-update-xapi-conf.XCP-ng.patch
- * Fri Oct 20 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 23.25.0-1.3
- - Don't require XS's fork of the setup RPM
- - We chose to revert to CentOS' version, as we don't share XenServer's view
-  regarding where to do changes to add users and groups, and we don't need
-  the added users and groups they put there yet.
- * Thu Oct 05 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 23.25.0-1.2
- - Add missing Requires towards nbd
- * Wed Sep 27 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 23.25.0-1.1
- - Update to 23.25.0-1
- * Wed Sep 20 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 23.24.0-1.1
- - Update to 23.24.0-1
- - Remove patches merged upstream.
- - Rework xapi-23.24.0-update-xapi-conf.XCP-ng.patch
- - Rework xapi-23.24.0-update-db-tunnel-protocol-from-other_config.XCP-ng.patch
- * Mon Aug 28 2023 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 23.3.0-1.9
- - Add xapi-23.3.0-Add-vdi_update-filter-to-some-tests.backport.patch
- * Wed Aug 23 2023 Guillaume Thouvenin <guillaume.thouvenin@vates.tech> - 23.3.0-1.8
- - Add xapi-23.3.0-Allow-a-user-to-select-on-which-SR-to-run-quicktest.backport.patch
- * Mon Jul 31 2023 Benjamin Reis <benjamin.reis@vates.fr> - 23.3.0-1.7
- - Drop `ext4` from `sm-plugins` in `xapi.conf`
- * Fri Jul 21 2023 Benjamin Reis <benjamin.reis@vates.fr> - 23.3.0-1.6
- - Rebuild for xs-opam-repo-6.66.0-1.2.xcpng8.3
- - Add xapi-23.3.0-filter-link-local-address-ipv6.XCP-ng.patch
- * Thu May 04 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 23.3.0-1.5
- - Rebuild for blktap-3.53.0-1.xcpng8.3 and sm-3.0.3-1.1.xcpng8.3
- * Mon Apr 24 2023 Benjamin Reis <benjamin.reis@vates.fr> - 23.3.0-1.4
- - Remove `/etc/xapi.conf.d` files, patch `xapi.conf` instead
- * Thu Mar 16 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 23.3.0-1.3
- - Rebuild for xs-opam-repo-6.66.0-1.1
- * Mon Mar 06 2023 Benjamin Reis <benjamin.reis@vates.fr> - 23.3.0-1.2
- - Update xapi-23.3.0-update-xapi-conf.XCP-ng.patch to re-enable HTTP (prerequisite for HTTP to HTTPS redirect)
- * Wed Jan 18 2023 Samuel Verschelde <stormi-xcp@ylix.fr> - 22.34.0-2.1
- - Update to 22.34.0-2
- - Drop xapi-22.20.0-redirect-fileserver-https.backport.patch, included in 22.34
- * Tue Dec 20 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 22.32.0-1.1
- - Update to 22.32.0-1
- * Thu Dec 08 2022 Benjamin Reis <benjamin.reis@vates.fr> - 22.31.0-1.1
- - Rebase on latest XS 8.3 prerelease updates
- - Drop two patches merged upstream
- * Thu Dec 01 2022 Benjamin Reis <benjamin.reis@vates.fr> - 22.20.0-1.2
- - Add xapi-22.20.0-redirect-fileserver-https.backport.patch
- * Wed Aug 31 2022 Samuel Verschelde <stormi-xcp@ylix.fr> - 22.20.0-1.1
- - Rebase on CH 8.3 Preview
- - Remove dependency to non-free packages again
- - Remove dependency to new non-free package pvsproxy
- - Remove patches merged upstream
- - Keep other patches still necessary.
- - Rediff xapi-22.20.0-fix-quicktest-default-sr-param.backport.patch
- - Add patch xenopsd-22.20.0-use-xcp-clipboardd.XCP-ng.patch, migrated from retired repo xenopsd
- - Rediff xenopsd-22.20.0-use-xcp-clipboardd.XCP-ng.patch and adapt paths
- - Remove ptoken.py and accesstoken.py yum plugins and their configuration
- - Add xapi-22.20.0-xenospd-dont-run-cancel-utils-test-as-unit-test.backport.patch to fix tests in koji

* Thu Jun 06 2024 Ming Lu <ming.lu@cloud.com> - 24.16.0-1
- CA-393507: Default cluster_stack value

* Thu May 23 2024 Ming Lu <ming.lu@cloud.com> - 24.15.0-1
- Rewrite fail function to support format and argument
- Use fail instead of failwith if possible
- Compute exe variable just once
- Fix file descriptor leak in case safe_close_and_exec fails
- Use /proc/self instead of /proc/%d and pid if possible
- CP-48195: Instrument client side of `forkexecd`
- CP-48195: Comment out `warn`.
- CA-392453: Misc fixes to Java SDK
- IH-568, fix(dune): avoid "module unavailable" errors when running dune build @check
- IH-568, fix (dune utop): conflicting module names with compiler libraries
- IH-568, fix (dune): allow all packages to be pinned
- tracing: add missing locks on read
- tracing: replace global ref with Atomic
- CP-48195: Set `Tracing.observe` default to `false`
- CP-48969: Reduce amount of logspam created by iostat
- opam: update dependencies from the code
- idl: bump datamodel_lifecycle
- CA-389319: Wait and retry for GET_UPDATES_IN_PROGRESS
- CA-392163 on start failure, clear a VM's resource allocations
- CP-48195: Add unit tests for `tracing` library.
- CP-48195: Remove code duplication.
- CP-48195: Tracing -- Move `create`\`set`\`destroy`\...
- API docs in Hugo
- xenopsd/scripts: Make pygrub wrapper use the libexec path
- CP-48027: Corosync upgrade add `cluster_stack_version` datamodel change
- CP-48027: Unittest file change for cluster_interface
- CP-48027: Add FIST point to allow Corosync2 cluster
- CP-48027: Add feature flag for corosync3
- Add option to disable fileserver in XAPI conf
- CA-392930: Fixed exception handling which prevents the user from reviewing certificates in PS 5.1 and connecting to the server.
- Added Debug profiles to the Powershell project.
- Avoids  calling Unix.readlink twice
- CA-392836,CA-392847: Lost the power state on suspended VM import
- CP-49029: Instrument `xapi_session.ml`  with tracing
- CP-49635: Add FIST point for corosync upgrade
- CP-49429 add IPv6 support for winbind/KDC
- CP-49429 store KDC in xapi as URI

* Tue Apr 30 2024 Rob Hoes <rob.hoes@citrix.com> - 24.14.0-1
- CP-46576: Add standard http attributes
- CP-47660 define anti-affinity feature
- Detect automatically whether we are on cygwin.
- Use templates to generate all the C files. CA-387885 (do not call internal headers from the public ones).
- Removed erroneously ported recipe.
- CP-47033: Protocol_{lwt,async}: process requests concurrently (optional)
- CP-47033: Make message switch concurrent processing optional
- CP-47033: Add test for concurrent message switch server
- Remove mention of `dotnet-packages` in `sdk-gen`'s README
- CP-48768: Update Folder Structure section in PS SDK's READMEs
- CA-391485: Avoid InterpolationSyntaxError by turning off interpolation
- opam: add xapi-log to message-switch-core dependencies
- Remove _t suffix for syslog_stdout_t type
- CA-389929: xenopsd: fix Xen version comparison. 4.17 is > 4.2, not lower!
- Add test for lock implementation in message_switch
- Check elapsed time for timeout test
- CP-47991: add CBT fields to the volume struct
- CP-46576: Add standard network attributes
- ocaml/idl: generate enum{_to_string,__all} functions
- test: add tests for allowed VM operations
- ocaml/xapi: use generated enum list instead of hand-maintained ones
- Added github workflow to build and release the C SDK.
- xenopsd: add mli to cli/xn and remove unused code
- CP-48195: Split tracing library
- CP-48195: Improvements to `tracing_export`
- CP-48195: Add `with_tracing` helper function
- PCI passthrough API
- IH-553: Optimize Sexpr.escape
- IH-553: Sexpr.escape should be a noop when nothing to escape
- IH-553: Optimise SExpr.unescape
- ci: remove warnings about outdated node versions
- pyproject.toml update settings for pytest etc for running CI locally
- pyproject.toml: Migrate pytype_reporter from scripts to python3
- ci: do not comment on PRs after merging
- ci: ignore pylint and pyflakes checks
- test_observer.py: Add setUp() and tearDown() of mock modules
- observer.py: Update error handling
- ci: install observer.py dependencies
- opam: delete xapi-stdext package
- opam: fix xapi-squeezed metadata
- opam: create package xapi-tracing-export
- datamodel_lifecycle: bump
- CA-391859: Failed to stop varstord-guard
- Exposed methods to fetch the methods available in the API.
- The github workflow artifacts for C contained unnecessary files.
- CI: update to Ubuntu 22.04
- ci(nopin): pinning is very slow and not necessary
- ci(opam-dune-cache): cache dune builds from opam
- ci(norm): we have enough space now
- ci: separate workflows
- Update README with different build instructions
- ci: trim dune cache
- Removed header because it does not look good on github.
- Install xapi-tracing-export library
- CA-392163 clear scheduled assignments on startup
- tests: Allow the alcotest_suite to run
- CA-371529 XSI-1329 remove license check for has-vendor-device
- CA-371529 remote VCustom IDL data type
- CA-371529 expunge create_from_record_without_checking_licence ...
- CA-371529 Update quality-gate.sh
- CA-371529 document changes in datamodel

* Mon Apr 15 2024 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 24.13.0-2
- Bump release and rebuild

* Tue Apr 09 2024 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 24.13.0-1
- Cleanup some unused code in forkexecd
- Fix vm_lifecycle quicktest to use specified SR
- message-switch: Print more complete time info in diagnostics
- CA-390570: Py3 socket.sendto needs bytes instead of a string
- CP-46179 Deterministic UUID for Back-Up VDI
- CP-48385: Enhancements for xapi-guard cache
- CA-378317 fix EBADF in waitpid_nohang
- CA-384483: Can't export VDI to VHD file with base VDI
- fileserver: use library to guess served files' mimetype
- CA-388624: Fix C SDK build on Fedora39
- Minor forkexecd test changes
- CA-390988: Prevent varstored-guard from shutting down while domains run
- CP-46851: add parameter to skip device types on get_export_metadata

* Mon Mar 18 2024 Rob Hoes <rob.hoes@citrix.com> - 24.12.0-1
- xenopsd: fix config to match install location (#5444)
- CP-47754: Do not report errors attempting to read PCI vendor:product
- CP-47431: Replace patched `Newtonsoft.Json.CH` with `Newtonsoft.Json` in C# SDK
- Add `.gitignore` to C# SDK source
- Use correct naming in `FriendlyErrorNames.resx`
- Generate `FriendlyErrorNames.Designer.cs` with templates
- Add 'threads_per_core' in 'Host.cpu_info'
- Filter out link IPv6 when migrating VMs
- Xapi service depends on systemd-tmpfiles-setup
- CP-47431: Use NuGet references in PowerShell SDK project
- Add reusable workflow for generating and building all SDKs
- Remove unused logic in `gen_powershell_binding.ml`
- Store trace_log_dir in XS_EXPORTER_BUGTOOL_ENDPOINT of the observer.conf
- Set traceparent trace flag to 01
- Add service.name attribute as a default observer attribute.
- Add the default_attributes to Dom0ObserverConfig Observers
- Create a new python3 directory for python3-only scripts
- fix: typo in doc
- Update xapi-idl unittest data for cluster interface
- CP-45496: Xapi writes host name/uuid to corosync.conf
- Add feature flag
- Replace use of `sdksanity` with reusable workflow for testing SDKs
- Build and package C# and PowerShell SDKs when creating a release
- Add and use `cleanup-xapi-environment` composite action
- Misc changes to SDK actions
- Use consistent artefact naming for SDK binaries
- CP-46151: Productise the observer.py.
- CP-46157: Add unit test for `observed_components_of`
- opam: add hex to xapi dependencies
- CP-45888: Java SDK updates
- Split the API reference markdown into smaller files and use templates to generate it.
- CA-389496: Avoid configuration conflicts for rotating xapi logs
- CA-389840: Bug in parsing output of 'xen-livepatch list'
- CP-48430 Update the running_domains metrics to count the not paused state domains
- fix typos: priviledges -> privileges
- CA-390109: Use `$PROFILE` path to store and read known cert list
- Fix typo in `XenServerPowerShell.csproj`
- Github CI updates

* Thu Feb 29 2024 Rob Hoes <rob.hoes@citrix.com> - 24.11.0-1
- rrd_updates: output JSON in the same structure as XML
- Exposed GFS2_CAPACITY in the known message types (for the purpose of providing user friendlier messages on the client side).
- CA-389206: Revert incompatible CLI protocol changes for update calls
- CA-383867: xapi-guard cache

* Thu Feb 15 2024 Rob Hoes <rob.hoes@citrix.com> - 24.10.0-1
- Improvements to the handling of update guidance:
- CP-45565: Add new guidance fields to API and CLI
- CP-45568: Do not enable host if its mandatory host guidance is pending
- CP-45566: [1/4] Change to use new guidance format in updateinfo.xml
- CP-45566: [2/4] Update evaluating guidances from new data structures
- CP-45566: [3/4] Fixup handling pending mandatory guidances
- CP-45566: [4/4] Update unit tests
- CP-46747: Expose 'title' field in updateinfo.xml to HTTP /updates
- CP-45567: Set recommended and full pending guidance lists
- CP-45567: Unit tests for livepatch failures
- CP-45567: Add safety check in host.apply_updates
- CP-45567: Set pending RestartVM for all VMs in the pool
- CA-387034: RestartVM is added to pending guidances of shutdown VMs
- CA-387033: Update xapi error document
- CP-43875: Record the repository hash on the host object when updating
- CP-45569: Add API Host.emergency_clear_mandatory_guidance
- CA-387201: Pool.last_sync_date not reset if the user changes the update channel
- CP-45570: Clear host update guidance
- CP-45570: Clear VM update guidance
- CP-45572,CP-45573: Split 'check_task_status' function out
- CP-45572,CP-45573: Split 'do_http_get' function out
- CP-44324: Block "host.enable" during "host.apply_updates"
- CA-388107: Make sure VM is running when starting restart_device_models
- CA-388351: Always apply livepatches even if host will reboot
- CP-45573: Add 'xe host-updates-show-available' CLI
- CP-45572: Print update guidance in xe host-apply-updates
- CP-45572,CP-45573: Refine to use 'command_in_task' more
- CP-46946: Bumped API version to 2.21 for update guidance improvement
- CP-47012: change pending guidance in old xapi to recommended ones in new xapi
- CA-388699: No async support on VM.restart_device_models
- CP-47509: Expose RequestHeaders and ResponseHeaders in C# SDK.
- Add Nile release

* Mon Feb 12 2024 Rob Hoes <rob.hoes@citrix.com> - 24.5.0-1
- Import xapi-project/stdext
- CA-372059: refactor the type of host in `squeeze.ml`
- CA-372059: delete the unused code
- CA-372059: use `Opt.value` instead of `match` and use `find_opt` to find a domain
- CP-46939: Add config options to disable http and https endpoints
- GitHub CI: Enable Codecov for Python, add pytype and other CI checks
- CA-372059: add an interface for squeeze.ml
- CA-382640: open SHM with os.open to allow for RW/Creat
- CP-46377: Splitting `xapi_observer.ml` in separete files
- CP-46477: Add helper function `is_component_enabled`
- CP-46377: Add env vars `TRACEPARENT` and `OBSERVER_CONFIG_DIR` to `sm_exec` calls
- CP-46377: Define default env var path in `forkhelpers.ml`
- CP-46377: Improve maintainabilty of `Dom0ObserverConfig`
- CP-46377: Refactor `env_vars_of_observer`
- Python2 os.fdopen() does not take keyword arguments, doh!
- xapi-rrd: attach tests to package
- add helper function for checking platform field
- Xen-4.15+: CDF_NESTED_VIRT
- Xen 4.15+: X86_MSR_RELAXED
- Xen 4.16+: CDF_VPMU
- Xen-4.16+: support max_grant_version field
- Xen-4.17+: cpupool_id
- [maintenance]: fix formatting after Xen-4.17 merge
- ci: delete needless files from base image
- fix(ci): use $TMPDIR instead of hardcoding /tmp in ocaml/libs/vhd
- fix(ci): use /mnt for temporary files and dune cache
- CA-388437: fix bond status reporting
- datamodel_lifecycle: update cluster forum introduction versions
- CA-388295: Revert the python3 changes for perfmon and hfx_filename
- Refactor cluster_health flag checking
- ci: remove action lint
- CP-46155: Call smapi scripts via observer.py when smapi observer is enabled
- Add support for Reverting changes to pytype_reporter.py
- Update API doc for cluster_host
- CP-46324: Send alert when a host leaves/joins the cluster
- rrdd.py: Python3: Fix crash on failure contacting xcp-rrdd
- CI: Unit-Test the crash-fix for rrdd.API.wait_until_next_reading()
- Actually get the traceparent from debuginfo instead of trace_id
- CA-385323: do not try to connect to xapi when creating sockets
- CP-46631: Improved list of span attributes.
- CP-46631: Remove code duplication
- CP:46157: Add `observer_experimental_components` flag
- xapi-guard: separate base types to its own module
- doc: Add some information about xapi-guard
- CA-388625: fix build of the Xen-API Java SDK
- build: add sdk-build-java Makefile target
- Make clear which drivers list we are getting

* Wed Jan 31 2024 Andrew Cooper <andrew.cooper3@citrix.com> - 24.4.0-2
- Rebuild against Xen 4.17

* Tue Jan 30 2024 Rob Hoes <rob.hoes@citrix.com> - 24.4.0-1
- CA-388180 Correcting Domain CPU Usage Values
- CP-46200 CP-45741 pass -std-vga to QEMU in the case of compute GPU
- Added unit in the description of PIF_metrics.speed and bumped last_known_schema_hash.
- xapi.conf: fix setting name for custom UEFI certs
- CA-388318: usb_reset.py: fixed byte issue

* Thu Jan 25 2024 Rob Hoes <rob.hoes@citrix.com> - 24.3.0-1
- xenopsd: avoid log message about vmdesc
- CA-387456 serialise Pool.eject
- fix(test): kill child process on test failure too
- fix(test): use SO_REUSEADDR to rebind port when run in a loop
- test: reduce sleep time
- CA-387588: test(forkexecd): fix off by one in test resulting in MSG_CTRUNC
- build: set a timeout for the tests
- CP-46264 deprecate host.bios_strings[hp-rombios] entry
- Refine the description and units of 'running_vcpus' and 'running_domains'
- Update datamodel_lifecycle
- Update API doc for cluster_host
- CA-387560 add support for more systemd execution types
- fixup! CA-387560 add support for more systemd execution types
- fix(ci): remove 1024 fd limit for now
- [maintenance]: enable generate_opam_files in dune-project
- CA-386920 destroy VTPM at the end of a migration directly (#5379)
- CA-387560 swtpm-wrapper: create PID file after socket
- CP-45970 remove qemu_trad_image.py
- CP-47043: Port usb_reset.py to python3
- Add API fields for quorum info from clusterd
- CP-46323: Expose quorum and cluster membership through the API
- CP-46374: Add a minimal observer.py
- CA-387698: datamodel: eliminate next_release
- Revert "Add mutex for concurrent processing of messages"
- CA-388064: Revert "Protocol_{lwt,async}: process requests concurrently"
- Only start cluster watcher if cluster_health feature enabled

* Tue Jan 16 2024 Rob Hoes <rob.hoes@citrix.com> - 24.2.1-1
- Revert "update mail-alarm and usb_scan to python3"
- CP-46238: Conditionally apply patch on xen-upstream only

* Tue Jan 16 2024 Rob Hoes <rob.hoes@citrix.com> - 24.2.0-1
- CP-45979 update link-vms-by-sr.py to python3
- Fixed markdown links (brackets=>parentheses).
- update mail-alarm and usb_scan to python3
- Allow passing extra headers into the HTTP calls (useful for CP-33676). Renamed a couple of local parameters.
- format with black
- refactory doexec with xcp.cmd
- CP-46122: Support PAX/POSIX tar on import
- CP-47075 Toolstack: Dumping VM RRDD Data to an Accessible JSON File for Regular User
- CP-45985: Update hfx_filename from python2 to python3
- CP-45985: Update perfmon to python3
- CP-45985: Update static-vdis to python3
- CP-45985: Update xe-scsi-dev-map to python3
- CP-45985: Remove unnecessary "list()" in loop
- CP-45985: Add some unit tests for perfmon/static-vdis
- CA-382035: Verify commandline items for service process in "pid"
- CA-387699: Fix Protocol_async.with_lock bug spotted by Vincent

* Wed Jan 10 2024 Rob Hoes <rob.hoes@citrix.com> - 24.1.0-1
- CP-46804: Add function to get master's external certificate thumbprint
- CP-46806: Add master's cert thumbprint to header when host_is_slave
- fix(NUMA): 'default' is a keyword in some SDK languages
- build: add command to check that the C# SDK compiles
- build: add SDK sanity test to CI

* Wed Jan 10 2024 Rob Hoes <rob.hoes@citrix.com> - 24.0.0-1
- CP-45974: Porting examples to python3
- update print-custom-templates to python3
- CA-386865: External auth plugin logs are not saved
- CA-386866: Invalid cross-device link during extauth configure update
- CA-385278: Add interface for flush spans and exit the export thread
- CP-45981: Update xenopsd from python2 to python3
- CP-46379: Set correct traceparent for `storage_smapiv1*.ml` functions
- ci(main): add a make install smoketest
- CP-46378: Propagate `dbg` to `Sm_exec.exec_xmlrpc`
- Rename 'override_uefi_certs' with 'allow_custom_uefi_certs'
- Introduce new methods for custom uefi certs
- Do not break symlink when no custom certificates are set
- Do not fail when fullpath is given to extract certificates
- Check for used UEFI certificates when updating vm platform
- Always set pool.uefi_certificates
- CP-46917 wait for DEMU "running" before unpausing
- CP-46917 improve error handling
- CP-47046 optimise rule emitter for xenopsd PVS Proxy setup
- Protocol_{lwt,async}: process requests concurrently
- Add mutex for concurrent processing of messages
- CP-46379: Propagate `dbg` to `sr_*` functions in `sm.ml`
- CP-44533 Add running vCPU and running domain of host into rrdd
- CA-384537 simplify reporting internal error (1/2)
- CA-384537 simplify reporting internal error (2/2)
- CA-384537 support NBD for CD device
- CP-46149: Execute observer db_fn before the forwarders.
- CP-46149: Add W3CBaggage module
- CP-46149: Create Dom0ObserverConfig and SMObserverConfig
- CP-46149: Use EnvRecord to format the env variables
- Avoid using a hardcoded value for Tracing Bugtool
- CA-385065 VM import with VTPM, don't block on power state
- OIL: introduce internal_error(fmt) for error reporting
- CP-44174: Add cpu_usage and memory_internal_free alarms for dom0 VM
- CA-386457: fix environment variable loading of `$PERFMON_FLAGS` in perfmon.service
- CP-46379: `Sm.vdi_generate_config` missing `dbg`
- CP-46378: Propagate `traceparent` from `Sm.register`
- CP-47153 add task list to bugtool
- CP-38020: always initialize NUMA information on startup
- CP-38020: drop numa-placement-strict
- CP-38020: add HOST.set_numa_affinity_policy
- CP-38020: introduce Host.numa_affinity_policy
- CP-38020: add CLI interface for NUMA policy host field
- doc(NUMA): move large comment to separate Hugo doc and update design
- doc(NUMA): Dom0 and IONUMA are out of scope

* Tue Dec 19 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.32.0-1
- CP-46677: Decrease the cardinality of "Export of VM" span name.
- CP-46677: Remove repeated code when creating a new span.
- CP-46677: Improve function performance
- Add VM migration walkthrough
- Remove unused code for getting dom0 memory
- CP-46379: Pass unchaged dbg to underlying function.
- CA-384457: Add special case for End_of_file to sparse_dd_wrapper
- Move squeezed docs from xapi-project.github.io
- Moving Event handling docs from xapi-project.github.io
- Add CLI architecture doc
- Add storage docs
- Add xcp-rrdd docs
- Add redo-log doc
- Update generated cluster test_data
- Update doc on how to update generated test data
- CP-44531 Toolstack: Add Dom0 CPU usage, total and free memory into rrdd
- CP-46085: Add quorum info to `xcli diagnostics dbg`
- CP-46379: Refactor 'with_dbg' to handle exceptions.
- CP-46379: Instrument 'storage_smapiv1.ml' to create spans.
- CA-386552 XSI-1534 Failed to disable pool HA after missing HA statefile
- Make sure observer exporter is only created once
- CA-386582: Always create exporting thread for observers
- CA-386676: Start clusterd observer when it is already enabled
- CP-46140 PVS IPv6 accept both IPv4, IPv6 for PVS Server
- CP-46140 add pvs-setup, replacing setup-pvs-proxy-rules
- CP-46379: Propagate 'traceparent' to 'Sm.*' functions
- Add an overview of how XAPI handles a migration request
- maintenance: reformat using ocamlformat 0.26.1
- maintenance: ignore latest reformat commit in git blames

* Mon Dec 04 2023 Rob Hoes <rob.hoes@citrix.com> - 23.31.0-1
- maintenance: update opam metadata from xs-opam
- CP-45847: Allow any value of trace flag for traceparent
- CA-384936 attach static VDIs for redo-log (#5235)
- CP-43578: Raise Error in tracing export when HTTP error occurs (#5230)
- CA-385080: Finish trace locally for forwarded tasks
- Add space between header name and value (#5238)
- CP-45921: Make yum commands nonessential
- CA-378591: Clear span tables when all observers are disabled
- CP-46004: Finish eventgen span to remove spans table clutter
- Add span table lengths to export span to help catch future issues.
- Add tracing for xe calls in the CLI server
- Update datamodel lifecycle
- CP-45978 update /etc/xapi.d/plugins/power-on-host
- CP-45978 update /etc/xapi.d/plugins/disk-space
- CA-365486: repository-domain-name-allowlist could accept a full hostname
- using xcp.cmd instead of popen
- CA-384537 add logging to quemu_media_change
- CA-384537 simplify qemu_media_change
- CP-46168: Some py2->py3 update for xapi startup
- Update DRAC.py for replacing subprocess.popen
- CP-45981: Update xenopsd from python2 to python3
- Revert "CA-379472 increase startup timeout for block_device_io"
- CA-384148 enable logging for redo_log_alert
- CA-384148 remove lock in Redo_log.startup
- CA-385315: document the certificates' fingerprints hash algorithm
- formatting with black
- using the shared lib xcp.cmd instead of subprocess.popen
- CP-45977: Update scripts/extensions from python2 to python3
- CP-42559: Add RBAC info to C# SDK XML docs
- CP-42559: Add RBAC info to Java SDK docs
- CP-42559: Add RBAC info to C SDK docs
- CP-42559: Hide internal roles from SDK docs
- Remove special handling for `get_all_records` messages in C# SDK
- xe pif-list: include host-uuid (#5263)
- xe pif-list: fix displaying of MAC
- CP-45978 update /etc/xapi.d/plugins to python3 for xs9
- format with black
- ci: create final releases
- ci: Simplify release workflow
- ci: set up configure appropriately on release
- ci: Avoid unnecessary workaround
- Advanced changes for python3 syntax:
- Improves Code Readability
- Change type of observer components to use variant
- Enhance debug message in tracing module
- Expose `flush_spans` from tracing.ml
- Refactor typeCombinator as a single module
- Add xapi-clusterd as an observer component
- CP-45469: Distributed tracing for xapi-clusterd
- Add xenopsd docs from old site
- Add live-migration diagram for xenopsd
- Remove old xenopsd docs from ocaml/xenopsd/doc
- Adjust quality gate for List.hd from 320 to 318
- Simplify scanning /sys/block/<dev>/ stats for iostat
- CA-365059: Clear source pool messages after migrating VM
- Revert "CP-45981: Update xenopsd from python2 to python3"

* Fri Nov 10 2023 Rob Hoes <rob.hoes@citrix.com> - 23.30.0-1
- Use .ndjson extension for tracing files to denote newline-delimited JSON
- CP-41844: Add xs-trace, an executable to submit trace files to an endpoint
- CP-41844: Add support for compressed files to xs-trace
- CP-41844: Add unit tests to xs-trace
- Replace duplicate functions rmrf and rmtree with rm_rec from Xapi_stdext_unix.Unixext
- CP-41844: Address PR comments and fix xs-trace tests by ensuring server is ready
- xapi-types/ref: add pretty-printer
- xapi-types/ref: optimize of_string for real references
- CP-45571: Add VM.restart_device_model function (API/CLI)
- CP-45741 VCS support, adjust args for qemu, demu
- CA-380551: bump minimum HA SR size to 4GiB
- CA-380551: xha_statefile: factor out checking for a VDI of given size or available free space
- CP-44561: When setting attributes on an Observer, preserve defaults
- CP-43901: Block pool member startup if it has a higher xapi version
- Update datamodel lifecycle
- CP-45304: Remove UUID from span name system.isAlive:<UUID>
- CP-46045 define VTPM feature
- CA-380551: HA: assert that the HA SR is big enough for BOTH the statefile AND the redo log
- [maintenance]: mark warning 5: ignored partial application as an error in release mode
- Add timeout to gpumon client
- CP-27910: expose json flag for /vm_rrd in the datamodel
- CA-384967: Fixup xcp-networkd service name
- CA-384979 replace XenMotion with storage live migration (#5237)
- CA-384882: Revert "CA-365059: Clear source pool messages after migrating VM"

* Tue Oct 31 2023 Rob Hoes <rob.hoes@citrix.com> - 23.29.0-1
- CA-375396: Ignore removed fields when redoing writes

* Mon Oct 30 2023 Rob Hoes <rob.hoes@citrix.com> - 23.28.0-1
- Only count VDIs on tested SRs
- CA-371002: Reformat checking template with match/with
- CA-371002: Do a usual import when a default template cannot be found
- Remove old and unused script
- CA-381044: Raise error when pool.set_update_sync_enabled is called with true and empty repos
- Choose size of batch VM evacuation
- xapi.conf: match the default value for override-uefi-certs
- CP-40123: encode the dumped JSON in rrdd as utf-8
- CP-43652: Remove tracing debug lines generated by xenopsd
- CA-383987: Ensure tracing request Host header is correct by not using a fixed host name
- Fix suspend-image-viewer binary
- CP-44367 - Allow SDK Consumers to create a custom implementation for JsonRpcClient
- CA-383987: Only include valid Hosts and Ports in tracing Host header
- CA-365059: Clear source pool messages after migrating VM
- CP-45938: Fixup xs9 failure due to python2 stuff
- XSI-1457: Limit number of sectors to coalesce

* Mon Oct 16 2023 Rob Hoes <rob.hoes@citrix.com> - 23.27.0-1
- Python's XenAPI: Update metadata
- CA-382596: Updated initialization script to work with PS 7 paths on Windows, and PS paths on Linux.
- CP-45579: Restored support for building the PowerShell module against .NET Framework 4.5 or above.
- Add some more documents from xapi-project.github.io
- Do not attempt to start snapshots or templates
- jemalloc: avoid bottlenecks with C threads
- [maintenance]: commit lifecycle changes
- CP-43755: Pam: avoid sleep(1) call when multithreaded
- CP-43755: Split internal and external auth locks
- CP-43755: Locking_helpers: introduce Semaphore
- CP-43755: xapi_session: switch to using Semaphore instead of Mutex
- CP-43755: Datamodel_pool: introduce local_auth_max_threads and ext_auth_max_threads
- CP-43755: Increase default max threads for PAM from 1 to 8
- fix(dune): gen_lifecycle depends on git describe output, which is outside of the normal source and build dependencies
- CP-43755: commit lifecycle changes
- CP-44320 scaffolding for NVidia Virtual Compute Service (VCS)

* Wed Oct 11 2023 Rob Hoes <rob.hoes@citrix.com> - 23.26.0-1
- Install suspend_image_viewer
- CA-379459 protect Redo_log.startup, shutdown with a lock
- CA-379459 use database lock, add logging
- Updated the PowerShell Readme.
- CP-45006: Define volume.compose API for SMAPIv3.
- forkexecd: handle invalid rpc messages more gracefully
- maintenance: relax message-switch's bounds on mtime
- CP-44271: Remove python build/install from source code
- CP-44271: Conditionally run python test
- Initial hugo config
- Hugo theme basics
- Docs: initial content
- Rename suspend_image_image_viewer -> suspend-image-viewer
- Updated docs links.
- CP-45175: Enable the OVMF debugging port by default
- [maintenance]: use full cmdline for vhd unit test runner
- fix(runtest): clean up after unit test
- Fix indentation issues in rrdd.py before py3
- CP-45338: futurize rrdd.py
- Publish new Hugo-based docs
- CA-381047: Add observer capability to bugtool
- CP-44563: Add compress_file function and compress tracing files with zstd when compress_tracing_files flag set
- CP-45214: Fix tracing HTTP request not working with Jaegers FQDN by flushing instead of closing the sending stream
- Do not fetch random SR in empty list
- CA-383491: Run pygrub in deprivileged mode when invoked from XAPI (upstreamed patch from 23.25.0-2)

* Thu Sep 28 2023 Alejandro Vallejo <alejandro.vallejo@cloud.com> - 23.25.0-2
- CA-383491: Addresses XSA-443 - CVE-2023-34325
- Run pygrub in depriv mode to protect against priv escalation

* Thu Aug 31 2023 Rob Hoes <rob.hoes@citrix.com> - 23.25.0-1
- CP-43977: Fallback un-recognized guidance as RebootHost
- xapi-aux: log error when reading ip type in inventory
- xapi-aux: filter out all link-local addresses
- CA-378966: Prepare ip monitor watcher to read more lines
- CA-378966: Detect state network interface changes
- network_monitor_thread: reuse named parameters
- xxhash(maintenance): add dependency to ctype stubs
- maintenance: use ounit2 instead of ounit
- maintenance: prepare mtime usage for 2.0
- CA-381856: preserve host.last_software_update on pool join
- CP-44988: remove API: host.apply_recommended_guidances
- fixup: update lifecycle for "host.apply_recommended_guidances"
- Move helpers to determine the client of a call from Context to Http_svr
- Improve logging at start of HTTP handler
- CA-381587: log when HTTP Basic auth is used, and by who
- CP-33044 replace gpumon shutdown with NVML detach/attach
- CP-42949: Ensure storage RRDs are created without tapdev in kernel
- Install python3 variant of xapi-storage alongside python2

* Fri Aug 18 2023 Rob Hoes <rob.hoes@citrix.com> - 23.24.0-1
- CA-379459 make shutdown mutex per redo_log
- CA-381133: Set pending_guidances based on recommended guidance
- CA-381133: Make {host;VM}.recommended_guidances internal-only
- CA-381133: Remove usage of host|VM.recommended_guidances
- CA-381133: Remove now-unused recommended_guidances fields
- Change argument of resort_guidances

* Tue Aug 15 2023 Rob Hoes <rob.hoes@citrix.com> - 23.23.0-1
- CA-381503: bump qemu filesize limit

* Tue Aug 15 2023 Rob Hoes <rob.hoes@citrix.com> - 23.22.0-1
- Removed class which became obsolete after the removal of the Proxy_* classes.
- Corrections to the unmarshalling of raw API hashtables.
- Removed code generating methods and parameters for XML RPC.
- Fixed a couple of code smells. Renamed internal method to reflect removal of proxy classes.
- Added message override (preserving it for the cases where DMC has been switched off via a feature flag).
- Further corrections to Marshalling so the Powershell module can create API objects from hashtables.
- CA-379112 make PBD.plug wait for scan results
- CA-379112 add logging
- CA-379112 update comments in message_forwarding.ml
- CA-380789: Not get power_state from snapshots with suspend VDIs
- Revert "CA-380580: cross-pool migration: no CPU checks for halted VMs"
- Revert "Cross-pool live migration: move CPU check to the target host"
- Revert "Add VM_metrics to metadata export"
- Revert "Add VM_metrics to metadata import"
- CA-380581: Remove lock on downloading updates from remote repos
- CA-379459 protect redo_log.shutdown with a lock

* Thu Aug 03 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.21.0-1
- Allow a user to select on which SR to run quicktest
- Added messages raised by v6 and SM.
- CA-380368: Replaced &lt; ad &gt; with < and >. Improved the type description.
- CA-380389: Version of deprecation/removal for repository.up_to_date not documented correctly
- Add option to redirect stderr to stdout to execute_command_get_output*
- CA-380178: xenopsd: Fix vTPM manufacture logging
- CA-380178: Increase swtpm startup timeout
- Add `vdi_update` filter to some tests
- CA-379472 log more block_device_io messages to info
- CA-379472 increase startup timeout for block_device_io
- CA-379112 log details of insufficient SR size

* Wed Aug 02 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.20.0-1
- CA-375992 remove stale swtpm chroots after boot
- CA-379472 more redo_log debugging
- CA-379350: Use up-to-date vTPM UUIDs when creating device models
- maintenance: make code easier to follow with aesthetic changes

* Thu Jul 27 2023 Rob Hoes <rob.hoes@citrix.com> - 23.19.0-1
- CA-379472 add debugging to redo_log
- Fix logging of CPU pool-level changes
- CA-380580: cross-pool migration: no CPU checks for halted VMs

* Thu Jul 20 2023 Rob Hoes <rob.hoes@citrix.com> - 23.18.0-1
- CP-42016: Add parameter "--newest-only" to "reposync" command
- CP-42014: Add last_update_sync to pool datamodel
- CP-42013: Do not apply recommended guidances automatically
- CA-376144: handle host.apply_recommended_guidances first on pool coordinator
- CA-375147: UPDATES_REQUIRE_SYNC when toolstack restarted on coordinator
- CP-42810: Periodic update sync
- CP-40204, CA-366396: Add "host.latest_synced_updates_applied", remove "repository.up_to_date"
- CA-376145: Reset pool.last_update_sync on pool coordinator change
- CA-378757: remove "EvacuateHost" from recommended guidance
- CP-43545: expose `issued` and `severity` from updateinfo
- CA-378778: Calculate host guidance correctly
- CA-380043: VM recommended guidances is not set correctly

* Thu Jul 20 2023 Rob Hoes <rob.hoes@citrix.com> - 23.17.0-1
- CP-43942 Remove "Portable SR" pseudo-feature
- opam: update metadata from xs-opam
- xapi_pgpu: make update_pgpus less scary
- vhd: use supported ocaml runtime function names
- xapi_guest_agent: use infix function for path concatenation
- maintenance(xapi_message): don't log scary messages
- Add VM_metrics to metadata export
- Add VM_metrics to metadata import
- opam: sync with latest metadata
- ci: update main workflow to setup-ocaml v2
- Cross-pool live migration: move CPU check to the target host
- Document parameters in Stunnel_cache API
- ci: try to reuse dune cache as much as possible
- CP-27910: factor out reposnse behaviour from host rrd handler
- CP-27910: allow exporting vm rrds and unarchives in json
- CP-27910: set content type headers for rrd endpoints
- maintenance(http-lib): Disallow invalid values in accept datatype
- http-lib: port tests to alcotest
- http-lib(fix): Prefer more specific mimetypes in Accept
- http-lib(feature): Make API more ergonomic
- IH-393: Use Accept header in xcp-rrdd endpoints
- http-lib: make all tests belong to the package
- CA-379928: enable more logging for redo_log_usage
- [maintenance]: reformat redolog_usage following logging change
- CA-377945: toolstack restart: ensure xapi is stopped first, started last
- Offload VM CPU Policy checks to Xen

* Mon Jul 17 2023 Edwin Török <edwin.torok@cloud.com> - 23.16.2-2
- Bump release and rebuild

* Wed Jul 12 2023 Rob Hoes <rob.hoes@citrix.com> - 23.16.2-1
- CA-379929: move json dump out of the rrdd plugin directory
- xcp-rrdd: remove hardcoded version on http requests
- Revert "CA-375992: clean up previous sandbox when creating one"

* Tue Jul 11 2023 Rob Hoes <rob.hoes@citrix.com> - 23.16.1-1
- Install cohttp-posix

* Tue Jul 11 2023 Rob Hoes <rob.hoes@citrix.com> - 23.16.0-1
- CA-373074 Added contents of update_getty script to run after Gencert is started
- CP-43551: Dump host_rrd latest data to /dev/shm/metrics/host-dss
- CA-378837 log results from Host.get_vms_which_prevent_evacuation
- Disable Python 2.7 on Github CI
- CP-40214: **/*.py: raise (AnyException()): Remove optional parentheses
- CA-379173 handle race condition in stunnel_cache
- CP-40214: ocaml/xapi-storage/python/xapi/**.py: modernize -f except,print
- Add HTTP Strict Transport Security header
- CP-43574: Add host load data source
- CP-40214: ocaml/xapi-storage/python/examples/**.py: Update except
- .gitignore: Ignore the *.bak backup files of the Python modernize tool
- CP-40214: xapi-storage/python/xapi/storage/api/volume.py: use long()
- Make tracing library independent of xapi-idl
- Add a debuginfo library
- Context: use Debuginfo library
- Task_server: use Tracing type and Debuginfo
- Tracing debuginfo: use newline separator for XML-RPC to work
- VM.migrate_send: properly pass on tracing data
- Storage_mux: wrap all calls with Debug.with_thread_associated
- Set up tracing and logging for SXM operations
- Set up logging and tracing for SMAPIv1
- scripts/plugins/extauth-hook-AD.py: Skip init logging on import
- CP-43565: xapi-expiry-alerts: a new library to generate expiry alerts
- CP-43777: Install xapi-expiry-alerts and ezxenstore
- ci: Break long line in yaml
- Add cpuid library
- Introduce functions in CPU feature sets in xenopsd
- xenopsd: change type of reported CPU feature-sets to an abstract type
- xapi: switch CPU feature sets to the abstract type and don't interpret them
- Remove CPUID tests from xapi and add to xenopsd
- Update quality gate
- CA-378931: usb_reset: Fix mount call parameters
- CA-375992: clean up previous sandbox when creating one
- CP-42019: Update wording for expiry message
- CA-379472 add debugging to redo_log

* Mon Jun 19 2023 Rob Hoes <rob.hoes@citrix.com> - 23.15.0-1
- xenops_sandbox: separate chroot instantiation from fs creation
- xenops_sandbox: expose less of chroot module
- xenops_sandbox: fix mistake in guard's parameter name
- xapi-idl: rename varstore interfaces
- xapi-guard: do not use a static version
- git: ignore another formatting commit for blames
- xapiguard_cli: run its tests as part of varstored package
- Tidy up class members in the file.
- Removed cyclical assignment. Reordered assignments.
- CP-43400: Expose ServerCertificateValidationCallback in the Session.
- Deprecated the Session constructors requesting the 'timeout' parameter. Added Property to set this instead.
- CA-354436: pool.is_slave took a long time to respond
- Update lifecycle
- CA-378222: assert_sr_can_host_statefile has to take available space into consideration
- CA-378229: flush database immediately on redo log enable
- [maintenance]: drop redundant 'true' and factor out anonymous function
- [maintenance]: use phantom type parameter to enforce RO operation on redo logs
- [maintenance]: simplify Redo_log.flush_db_exn
- [maintenance]: split Redo_log.enable on whether it is RO or not
- [maintenance]: redo_log hide redo log type
- [maintenance]: drop internal functions from interface
- CA-378304: check max_file_size limit after writing to tracing file
- CA-378035: set nbd client timeout to 60 seconds
- CA-378323: prevent find writing to stderr if /var/log/dt not present
- CA-378455: Ensure TPM contents are base64-encoded on migration
- maintenance (suspend_image_viewer): avoid duplication

* Fri Jun 09 2023 Rob Hoes <rob.hoes@citrix.com> - 23.14.0-1
- CP-41837: Create tracing library
- CP-41839 Added TracerProvider modules to tracing
- CP-41840: Add function to convert span to zipkin json
- CP-41841: Export trace json files to http
- CP-41841: Export trace json files to dom0 log endpoints
- CP-42362: Only export finished spans and implement span garbage collector
- CP-42361: Use XenAPI configuration list in TraceProvider to switch between HTTP/dom0 log export
- CP-42441 Added SpanKind to Spans
- CP-41841 Added conversion between Spans and W3C Traceparent headers
- CP-42441: Capture exceptions from failed operations in span tag
- CP-42609 Service name is set dynamically depending on the service
- CP-42607 Created set, create, destroy functions for TracerProviders
- CP-42854 Add Unit Tests for Tracing Library
- CP-41842 Created Observer class with IDL functions to manage Open Telemetry providers
- CP-41842 Added CLI for Observer commands
- CP-41842 Added initialisation of Tracing library for Xapi
- CP-41842 Added Tracing Library calls to Xapi_observer to link to the library
- CP-41842 Added Attribute validator in library and in xapi_observer
- Instrument tracing in Xapi
- CP-41841 Added traceparent header to http_svr
- CP-41841 Populate traceparent header in rpc and retreive it in context.ml
- Nested tasks in startup sequence
- Trace xenopsd operations
- Xenopsd: nest parallel tasks
- Xenopsd: always use task for import_metadata
- Trace SM ops and link from xenopsd
- CP-42606 Add Management interface to Xenopsd
- CP-42608 Added mechanism to manage components in other Daemons
- CP-42608 Added set_components to register and unregister changed components
- Fix errors in message forwarding
- CP-41843: Add /var/log/dt to bugreport
- Link up xapi/xenopsd tracing for live migration
- xenopsd: include traceparent header in requests to a remote xenopsd
- xenopsd: add received traceparent header to task
- Remove unused module definitions
- CP-42553: Periodically delete old files and files beyond a size limit
- Add error identifier to attributes to mark a span as having an error
- Add more endpoint valdiation for URLs
- Added tracing to rpc calls using make_remote_rpc
- Remove filters and processors from TracerProvider and rename tags to attributes
- Remove service_name as a TracerProvider and Span field and set it as a library level constant
-  Added SpanLink to spans
- Added SpanEvent to spans
- Use w3c format to serialise spans going into xenopsd to avoid bloat
- Moved Attribute fields on Spans and TracerProviders to being a StringMap
- Updating Zipkin to export events (annotations) and to include remoteEndpoint
- Fixing Quality gate
- CP-42825: Add XAPI Alcotest unit tests
- CP-42553 Write spans in files up to 1mb then flush to logs
- Trace Export operations in the library
- Add Attributes to Tracing in the library
- Batch all Traces in one export call to improve perfomrance
- CP-42999: Return new "preview" in return of v6 "get_version"
- CA-377824 fix FD leak in xenopsd
- CP-43518: tap-ctl stats: treat `tap` key as optional in returned object

* Thu Jun 08 2023 Rob Hoes <rob.hoes@citrix.com> - 23.13.0-2
- Bump release and rebuild

* Wed Jun 07 2023 Rob Hoes <rob.hoes@citrix.com> - 23.13.0-1
- xenopsd: use HVM memory model for PVH guest not using shim
- maintenance: small simplifications and reformattings
- squeezed: Be aware of PVH domains
- CP-42739: Bump Java SDK to JDK 11 (LTS)
- opam: move vhd-format metadata to root directory
- [maintenance]: delete xen-gnt-unix dependency
- [maintenance]: avoid building bytecode versions of executables
- libs/vhd: run make format
- squeezed: fix link to architectural drawing
- CA-376879: VLAN PIF created in pool.join is shown as disconnected (#5026)
- CP-40775 remove VTPM check from VM.clone
- CP-40775 remove VTPM check from VM cross-pool migration
- CP-40775 remove VTPM check from VM.checkpoint
- CP-40775 update quality gate
- CP-40775 remove VTPM check VTPM.create wrt HA
- CA-376864: prefer use of NBD path for static VDIs on SMAPIv1
- redo-log: bump default size to 4GiB
- xapi-guard: initialize Logs
- xapi-guard: do not use a static version
- xapi-guard: refactor serve_forever_lwt
- xapiguard_cli: install
- xenopsd: plumb through vtpm uuid to suspend/restore
- swtpm-wrapper: do not spawn additional logger
- swtpm-wrapper: be explicit on when to manufacture a new vTPM
- swtpm-wrapper: unix+http scheme support
- xapi-guard: add minimal REST interface for swtpm
- CP-42726: Create socket whenever swtpm starts up
- swtpm_guard: spawn with correct gid
- xenopsd: drop reading/writing of vTPM state through the file
- vTPM smoke test
- CP-40775 remove assert_ha_vtpms_compatible
- CP-40775 remove assert_ha_vtpms_compatible - update quality gate

* Tue Jun 06 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.12.0-2
- Bump release and rebuild

* Thu May 25 2023 Rob Hoes <rob.hoes@citrix.com> - 23.12.0-1
- Check if user if root before continuing with test
- CA-377169 block VM.checkpoint of running VM with VTPM
- Update quality-gate
- ocaml-vhd: fix unit tests
- ocaml-vhd: Cstruct.len -> Cstruct.length
- ocaml-vhd: Split off function for VHD creation from Raw_input.vhd
- ocaml-vhd: Add Hybrid_raw_input to VHD
- vhd-tool: Remove unnecessary values from match
- vhd-tool: Remove unnecessary parameter from write_stream
- vhd-tool: Extend documentation in impl.ml
- vhd-tool: fix progress bar
- Make NBD disconnect robust to the device being gone
- CP-43131: Make gvt-g support configurable
- CA-333441, CA-377454 create /var/lock/sm/iscsiadm
- CP-31856: Option to use NBD to attach disks to the control domain
- CP-33338: call vhd-tool with source-format nbdhybrid for NBD sources
- Install rrdd.py into the build output
- Make session errors look less scary in the logs
- Update rrdd to send v2 protocol data
- CA-377456 unblock cross-pool migration with VTPM when halted
- Set PIF's IPv6 Gateway when in DHCP/Autconf
- CP-42182 Set Makefile to install rrd-cli
- xapi-rrdd: test rrd_cli
- editorconfig: correct setting for Makefile is tab, not tabs
- database: document values of exceptions
- maintennce: avoid future warnings
- maintenance: add reformat commit to ignored revs
- CP-42533: vhd-tool: add hybrid NBD-to-VHD exporter
- CP-42533: vhd-tool: add nbdhybrid as a supported source format
- CP-42533: vhd-tool: wire up nbdhybrid to vhd
- CP-43387: Fix VDI delta copy with NBD datapath connection
- CP-42064: Move NbdClient module from Xapi_vbd to Attach_helpers
- CP-42064: Fix storage migration for NBD-backed storage

* Tue May 09 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.11.0-1
- CA-376297: Test that mirage-crypto accepts all valid RSA keys
- CP-42642: Support share server certificate file to group users
- CP-42835: Allow changing DNS servers when HA or clustering enabled
- CA-375358: Parse output of yum upgrade to get RPMs to be updated/installed
- Add comments for RPM version comparison functions
- CA-375358: Add redundancy in getting latest updates/installations
- xapi_blob: don't verify connection when sending between pools
- ocamlformat: reformat using ocamlformat 0.22.4
- ci: publish XenAPI releases to PyPI
- ci: reduce code run with permissions to release to PyPI
- xapi-cli: Have a consistent interface for vtpms's vm
- Move writing init complete to the end of startup sequence
- CA-374989: Avoid using get_record on cross-pool migration
- `rrdd-plugin`: do not write payload if page count is 0
- CA-376894 update VM allowed ops after deleting VTPM
- Fix a few auto formatting differences
- [maintenance]: varstored-guard depends on alcotest-lwt for tests
- [maintenance]: remove xapi-types to http-svr dependency
- [maintenance]: xapi-guard: drop inotify dependency
- [maintenance]: xapi-guard: make unit tests run on Mac OS
- [maintenance]: allow building some libraries on macOS
- [maintenance]: repeat test errors at the end
- [maintenance]: xen-api-client: avoid name clash on Util module
- xen-api-client: add http+unix URI
- xen-api-client-lwt: introduce a SessionCache
- [maintenance]: update xen-api-client-lwt examples to use the SessionCache
- [maintenance]: tweak xen-api-client-lwt examples
- maintenance: add undeclared dune dependencies
- CP-40528 VTPM snapshot, revert, clone
- CA-376993 disable test_clustering (revert this!)
- ci: do not attempt to install xapi-database
- Revert "CA-376993 disable test_clustering (revert this!)"
- spec: specify SPDX licenses
- spec: changes in library files packaged

* Wed Apr 19 2023 Rob Hoes <rob.hoes@citrix.com> - 23.10.0-1
- Xen libraries are are now taken straight from the xen package instead of through xs-opam
- Import ezxenstore into the xen-api repo
- CP-39863 add allowed VTPM ops for VMs
- CP-42455 Revert disable DMC
- CA-376319: Ensure that nbd_client_manager cannot block forever.
- CA-376326: rrdd_proxy: compare the localhost uuid with a uuid instead of a ref
- CA-376326: rrdd: return 404 instead of just failing
- ezxenstore: make tests exclusive to it
- CA-376294: Extract hostname from FQDN
- CA-376294: Update log message about compressed netbios name
- CP-39935 catch and log unexpected exceptions during import
- CA-376448: explicitly validate refs in PVS_cache_storage.create

* Fri Mar 24 2023 Rob Hoes <rob.hoes@citrix.com> - 23.9.0-2
- Bump release and rebuild

* Fri Mar 24 2023 Rob Hoes <rob.hoes@citrix.com> - 23.9.0-1
- CA-343683 Added lock to disk writing in Networkd to avoid writing to disk with incomplete configuration details
- ci: nosetests are only located in scripts
- python: port tests to pytest
- ci: setup python tests in the yml definition
- CA-375705: fix total order on Ref.compare
- CA-375705: unit test for total order on Ref.compare
- CP-39935 implement VTPM export
- CP-39935 Implement VTPM import
- CP-39935 Update quality-gate.sh for VTPM
- CP-39935 improve full restore
- xapi_vtpm: do not reuse name for get_contents
- CP-41574: Add telemetry configuration data
- CP-41574: Expose repository proxy password access to API
- CP-41574: Update DB schema
- CP-41574: Updated datamodel_lifecycle.ml for new added fields
- CA-375359 improve "pool_total_session_count" RRD description
- CP-30367: xenopsd: add support for PVH
- CP-30367: XAPI: allow PV and PVH kernels in /var/lib/xcp/guest too
- CA-375359 & CP-42286: Rename `sessions per second` to `sessions/s`
- CP-41796 enable HTTPS migration by default
- CP-41796 prevent changes to https_only in CC_PREPARATIONS=true

* Wed Mar 08 2023 Rob Hoes <rob.hoes@citrix.com> - 23.8.0-1
- CA-375427: Make DP.destroy idempotent again
- CA-364049: Tell external auth plugins to use python3
- CA-375634: Move probe-device-for-file to Python 3

* Fri Mar 03 2023 Rob Hoes <rob.hoes@citrix.com> - 23.7.0-1
- CP-40847: synchronize read-only uefi-certificates field for both host & pool

* Thu Mar 02 2023 Rob Hoes <rob.hoes@citrix.com> - 23.6.0-1
- [maintenance] Makefile: add a rule to write out a compile_flags.txt
- CA-375274: xenctrlext: fix wrong number of arguments to interface_open and unshadow
- CA-375273: xenctrlext: fix race conditions
- [maintenance] direct_copy_stubs.c: uerror is available in caml/unixsupport.h
- [maintenance] vhd-tool/direct_copy_stubs: fix setting of O_DIRECT flag
- [maintenance] add .editorconfig: use spaces instead of tabs in C files
- CA-375106: tuntap_stubs.c: raise Unix.error instead of failwith
- CA-375276: xenctrlext_stubs.c: xc_get_last_error is not thread safe, use just errno which is
- [maintenance] xa_auth_stubs.c: move free inside the blocking section
- CA-375280: xe-toolstack-restart: stop and start all services at once
- python/XenAPI: Replace import six.moves with stdlib imports
- Allow to use a CIDR for VIFs IPv4 and IPv6 allowed IPs
- CP-41730: Limit ldap query timeout for subject information
- python/setup.cfg: Fix deprecated dash-separated key
- python: Use xapi's versioning scheme for XenAPI package
- ci: use official gh cli for release workflow
- CP-40388: Rename SMAPIv3 feature VDI_ATTACH_READONLY
- CP-40388: define VDI_ACTIVATE_READONLY in Smint
- CP-40388: store SR feature table upon mux registration
- CP-40388: store attach mode (rw/ro) with datapath in mux
- CP-40388: Add VDI.activate_readonly to the storage interface
- CP-41675: add new field override_uefi_certs to xapi.conf
- CP-41675: xapi-start behaves according to field override-uefi-certs in xapi.conf
- CP-41672: wipe the contents of the pool.uefi_certificates during upgrade
- CP-40847: CP-42007: make pool.uefi-certificates field read-only
- CP-41675: fix idempotent behaviour of Helpers.FileSys.rmrf
- CP-42007: platform:secureboot=auto means platform:secureboot=true always
- CP-42007: separate error msg from exception generation

* Fri Feb 17 2023 Rob Hoes <rob.hoes@citrix.com> - 23.5.0-1
- ci: fix docs upload of xapi-storage
- CP-42173: xenctrlext: stop using xentoolog bindings
- Remove log spam about leaked VDI locks at startup
- Fix storage_smapiv1_wrapper log name
- Storage mux: filter out duplicates in SR.list
- CA-375256: Fix storage initialisation on xapi startup

* Fri Feb 10 2023 Christian Lindig <christian.lindig@citrix.com> - 23.4.0-2
- CP-40650 Remove vtpm feature restriction (i.e., enable feature)

* Fri Feb 10 2023 Rob Hoes <rob.hoes@citrix.com> - 23.4.0-1
- Reorganise the storage API layer in xapi and xapi-storage-script

* Wed Feb 08 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.3.0-1
- CA-374989: add default values for removed fields
- CA-374989: Revert "CP-40357: Purge all removed fields from the database and clients"
- CA-374989: Bump datamodel version

* Thu Feb 02 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.2.0-1
- Stop generating classes for the XmlRpcProxy.
- CP-33338: write physical-device-path to xenstore for nbd devices
- maintenance: commit calculated changes for datamodel_lifecycle
- CP-39806: use updated C function names for ocaml 4.14
- CP-40065: Delete VTPM contents when VM is deleted
- CP-40065: Add VTPMs to the database garbage collector
- CP-41812: Add total_sessions_count RRD
- CP-41818: Branding and copyright updates for the SDK

* Mon Jan 30 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.1.0-2
- Bump release and rebuild

* Mon Jan 30 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.1.0-1
- CA-374872: error when `BOND_MEMBERS` is not in `management.conf`

* Fri Jan 27 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 23.0.0-1
- xcp-rrdd: add interface for rrdd_server
- CA-374274: Provide more information when datasource is not found
- CA-362358: Filter out new files when refreshing directory of certificates
- Filter out new.pem in cert_distrib
- Support bond at firstboot
- CP-41444 Added actions_after_softreboot field to VM for Xenopsd soft_reboot
- xenopsd: use uuid instead of deprecated uuidm functions
- message-switch: conform to new APIs in jst libs
- xapi-storage-script: conform to new APIs in jst libs
- xen-api-client: conform to new APIs in jst libs
- stream_vdi, import: conform to new APIs in tar
- gencert: conform to new APIs in x509
- xapi-guard, xen-api-client: conform to new APIs in conduit
- message-switch, vhd-tool: drop io-page-unix
- nbd: change ocaml-nbd usage
- session_check: add action name in the error returned
- datamodel_lifecycle: update latest APIs

* Thu Jan 26 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 22.37.0-1
- CA-374238: prevent copying of removed fields when reverting snapshots

* Mon Jan 23 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 22.36.0-1
- Makefile: install and uninstall xapi-schema using dune
- install xapi-schema libraries as part of xapi-datamodel-devel

* Thu Jan 19 2023 Pau Ruiz Safont <pau.ruizsafont@cloud.com> - 22.35.0-1
- CP-40357: Enable computation of correct API lifecycles
- CP-40357: Patch invalid lifecycles
- CP-40357: Statically parse all the datamodel lifecycles
- CP-40357: separate schema modules into xapi-schema package
- database / idl: reduce code complexity
- CP-40357: Change comment on failure to load db row
- CP-40357: Avoid loading removed fields into the database
- xapi_version: extract "git_id" from version
- CP-40357: Remove oss_deprecation_since:None
- CP-40357: Integrate state into the datamodel's lifecycle
- CP-40357: Purge all removed fields from the database and clients
- CP-40357 (idl/json): Only show latest entity change in a release
- CP-41450: The SDK sample code has moved to a different repo.
- Stop installing internal headers. Create dll symlink for cygwin.
- opam: synchronize opam metadata with xs-opam
- xapi-storage{,-script}: explicitely use python2 instead of python
- Add new bias_enabled field to pool datamodel
- Make bias against scheduling vms on pool master configurable
- Switch from Xenctrl.hvm_check_pvdriver to Xenctrl.hvm_param_get
- Corrected repo link in the README.
- ci: avoid github API deprecation warnings
- xenctrlext_stubs: fix xfm_open parameter mismatch
- CP-40946 Make ATTACH_READONLY consistent with other features
- CA-373776 Added unhandled exception handler to nbd to log errors instead of the messages being printed to the host console
- CP-41366: Rename Citrix Hypervisor to XenServer
- Fix extra `/` in https redirection
- CA-373785: Deny HTTP requests on website_https_only
- maintenance: use generated datamodel_lifecycle

* Tue Dec 13 2022 Rob Hoes <rob.hoes@citrix.com> - 22.34.0-2
- Bump release and rebuild

* Mon Dec 12 2022 Rob Hoes <rob.hoes@citrix.com> - 22.34.0-1
- Update lifecycle for pool.migration_compression
- CA-373551: register for host events rather than task in events_from_xapi

* Thu Dec 08 2022 Rob Hoes <rob.hoes@citrix.com> - 22.33.0-1
- CP-40404: Add C# NuGet specs in its csproj
- CP-40404: Move C# SDK samples to .NET 6.0
- CP-41213: swtpm-wrapper should not fiddle with cgroups
- CP-40404: Do not specify assembly info in `AssemblyInfo.cs`
- CP-40404: Build C# SDK to .NET Framework 4.5
- CA-372785 make with-vdi more robust
- CP-40404: Replace deprecated module manifest member with `RootModule`
- Fix missing `Reference` value in PS SDK cmdlets output
- Modify Xenctrlext to use its own libxc handle
- CP-40404: Do not specify PS SDK assembly info in `AssemblyInfo.cs`
- CP-40404: Update Powershell and C# SDK READMEs
- CP-41348: Convert swtpm-wrapper to Python 3
- Redirect fileserver towards https
- CA-371790: Restrict the permissions on pool tokens
- Xenctrl: drop interface_close
- CP-41279: add migration_compression pool option

* Fri Nov 18 2022 Rob Hoes <rob.hoes@citrix.com> - 22.32.0-1
- CA-342527: Remove unnecessary list traversals on rbac.check
- xapi/rbac: Remove the non-"efficient" code path
- xapi/rbac_audit: do not audit rrd_updates
- CA-371780: Reduce cost of merge_new_dss
- rbac_audit: refactor module
- CA-372128: DB performance optimisations
- CA-140252: fix flag handling
- CP-40190: vTPM - Fix xenopsd to indicate correct state file format to swtpm-wrapper.
- CP-40747: Add certificate checking options to sparse_dd and vhd-tool
- CP-33044 define attach/detach IDL calls for gpumon
- CA-371780: Port xcp-rrdd tests to alcotest
- CA-371780: Reduce overheads in update_rrdds
- CP-40823 Edited Vdi.t in xapi/storage_impl.ml to record vm
- CP-40823 Created tests to the modules in storage_impl
- CP-41028: enable certificate checking for storage migrations
- CP-40190: Prevent SWTPM from filling dom0 root partition
- xenopsd: define uncaught-exception handler
- CA-369444: Ensure xenopsd still starts if VM state upgrade fails
- CA-371419: Always log exceptions when responding with 500 Internal Error
- CA-369690: Prioritize loglines when backing up RRDs
- CA-369690: Reduce logging produced by xmlrpc_client
- Debug: remember previous log names per thread in a stack
- Do not log out session in xapi events loop to re-register VMs
- Enable HTTPS for storage migration on the source

* Thu Nov 17 2022 Christian Lindig <christian.lindig@citrix.com> - 22.31.0-2
- CP-33044 install gpumon-cli

* Tue Nov 01 2022 Rob Hoes <rob.hoes@citrix.com> - 22.31.0-1
- CA-370575: [XSI-1310] Driver disks / supp packs applied at host
- CA-370947 increase robustness of with-vdi script
- CA-364194: Add a comment on static-vdis for a timeout enhancement
- CA-364194: add timeout parameter to script callers in xapi
- CA-364194: Allow creation of statefiles to time out
- CA-370578 use subsystemId in NVidia GPU matching
- maintenance: explicitely declare direct dependencies
- ci: add xapi-log and xapi-open-uri
- idl/json_backend: Process unreleased versioned releases
- ocaml/idl: make gen_lifecycle compatible with gitless spec building
- idl/json_backend: order releases from latest to oldest
- CA-370082: Block multiple definitions of certificate-chain in xe cli
- maintenance: avoid traversing lists twice when reading cli params
- exit with error if add_vswitch_port fails
- Revert `uuidx` rename in `gen_powershell_binding.ml`
- xapi-idl: make storage-test be part of a package
- opam: update metadata
- xenopsd/dbgring: don't mention xenmmap dependency
- CA-371759: check certificates in xsh
- CP-40490: Require --force parameter to destroy VTPMs
- xapi-cli-server/cli_ops: reuse --force message
- xapi: group import error and cause into the same line
- CP-39134: xapi-guard: do not hardcode rpc function - allow for unit testing
- CP-39134: xapi-guard: separate code into own library for testability
- CP-39134: basic unit test for xapi-guard
- CP-39134: xapi-guard: add unit tests for bad values
- CP-39134: varstore-guard: use inotify to wait for the apperance of the socket
- Maintenance: xapi-guard: use Lwt.Syntax instead of Lwt.Infix
- CP-39134: add shutdown unit test
- CP-39134: quality gate fixups
- xapi-guard/test: Count file descriptors
- CP-41033: install XenAPI to Python 3
- CP-41033: update XenAPIPlugin for Python3
- idl/ocaml_backend: do not generate empty docstrings
- idl/gen_server: Remove custom functions
- CA-352073: gen_server: Serialize lists in [ ... ] form
- CA-352073: Prepare to reuse defaults unmarshalling code
- CA-352073: Ensure all serialized calls can pass rbac checks
- CP-41033: further updates to XenAPIPlugin for Python3

* Wed Oct 12 2022 Rob Hoes <rob.hoes@citrix.com> - 22.30.0-1
- CP-40402: Move C# and Powershell SDK Generation to .NET
- opam: Update Alpine deps for xapi
- CP-40754: Sync host.https_only fields on startup
- CA-370140: shut down swtpm after qemu
- CP-40755: Allow memory+storage+vGPU migrate to use HTTPS only
- Update JSON backend for modern xapi releases
- CA-368579: Mitigations against DoS attacks by unauthenticated clients
  (now upstream, replacing patch queue)

* Wed Oct 12 2022 Rob Hoes <rob.hoes@citrix.com> - 22.29.0-1
- CP-40753 host.set_https_only updates firewall using firewall_port_config_script helper
- CP-40753 Added change to the firewall-port script to modify the RH-Firewall-1-INPUT chain
- Update Makefile (un)install targets

* Wed Oct 12 2022 Rob Hoes <rob.hoes@citrix.com> - 22.28.0-1
- Revert "Add a fallback system for auth files belonging to RPMs"
- Rename Uuid module to Uuidx
- Move good_ciphersuites from Xcp_consts to Constants
- Move logging lib from xapi-idl to its own package
- Move Open_uri from xapi-idl to its own package
- Add HTTPS support to open-uri
- idl: update datamodel_lifecycle after tag
- xenopsd/xc: Print all information in Service_failed exceptions
- CP-39744: simplify vm_platform.sanity_check parameters
- CP-39744: Block BIOS VMs with vTPM attached from booting
- CP-40775: share function raising not done for vtpm exceptions
- CA-370858: disallow VM exports with VTPMs attached

* Wed Oct 12 2022 Rob Hoes <rob.hoes@citrix.com> - 22.27.0-1
- Add a fallback system for auth files belonging to RPMs
- CA-370084: Test pem with DOS line endings
- Update lifecycle for VTPM datamodel
- xapi-cli-server: change vm record to show "vtpms"
- CA-370731: remove obsoleted copies of ca certs in the db
- CA-370731: Allow pool to recover from duplicate ca certs
- CP-33973 disable DMC; fix unit test
- CP-40767 CP-40429 Migration Compression - define Zstd.Fast, more
- CP-40749 Added https_only field
- CP-40750 Added set_https_only function
- CP-40751 Added and implemented Pool.set_https_only
- CP-40752 Added CLI functionality for a pool level getter and setter
- configure.ml: inject version number here
- xapi-xenopsd.opam: declare zstd as dependency
- maintenance: Remove obsolete version-gathering methods

* Fri Oct 07 2022 Rob Hoes <rob.hoes@citrix.com> - 22.26.0-2
- CA-368579: Mitigations against DoS attacks by unauthenticated clients

* Fri Sep 09 2022 Rob Hoes <rob.hoes@citrix.com> - 22.26.0-1
- Introduce vTPM

* Mon Aug 22 2022 Rob Hoes <rob.hoes@citrix.com> - 22.25.0-1
- XenAPI.py: Simplify and fix UDSTransport implementation
- CP-40375: Allow cert clients to perform VM.shutdown and VM.start_on
- CP-37225: Added unmarshalling code for Ocaml's Set(Set string) for C.
- Fix quicktest's -default-sr parameter
- CP-40392 compress vGPU migration stream
- CA-369599: ignore invalid references on eject
- maintenance: factor out Ref.to_option and Helpers.ignore_invalid_ref

* Mon Aug 08 2022 Pau Ruiz Safont <pau.safont@citrix.com> - 22.24.0-2
- Bump release and rebuild

* Fri Jul 29 2022 Rob Hoes <rob.hoes@citrix.com> - 22.24.0-1
- CP-39894: move xenopsd's daemon modules from device to service
- xenopsd/xc/service: add licensing header
- CP-39894: move all varstored starting code to service module
- CP-39894: move vgpu starting code to service module
- CP-39894: Replace is_pidfile and pid_path with pid_location
- CP-39894: tweak Service.Qemu interface
- CP-39894: Use pid_location for file and xenstore cleanups
- CA-366479: Remove Qemu's pidfile on domain shutdown
- Factor out Throttle module
- Update datamodel_lifecycle.ml only when changed
- ci: generate releases from tags, upload XenAPI python lib
- CHCLOUD-717: Spawn a thread to run xe-toolstack-restart
- CP-40155 Parallelize Host.evacuate
- CP-37091: Updated samples and fixed some code issues in the Java SDK.
- CP-37225: Added unmarshalling code for Ocaml's Set(Set string) for C# and PS.
- Removed dependency on 3rd party libraries from the PS module project.
- CP-37091: Fixed some code issues in the PowerShell SDK.
- CA-368910: Allow destruction of PVS_cache_storage if SR is already gone
- CA-368437 remove duplicate keys from SM.features
- CA-368806: Workaround pbis get wedged
- CP-40175: Strip metadata of non-applicable livepatches
- CA-347473: Minor memory leak from unloaded Xen livepatches (#4762)
- CA-367236 replace Ezjsonm with Yojson

* Wed Jul 06 2022 Rob Hoes <rob.hoes@citrix.com> - 22.23.0-1
- CP-40027 VM migration introduce /services/xenops/migrate-mem
- CP-39640/CP-39157 Add stream compression for VM migration
- Add matching Synchronisation point 1-mem ACK log on receiver
- Allow VBD.plug to dom0 again

* Tue Jul 05 2022 Pau Ruiz Safont <pau.safont@citrix.com> - 22.22.0-1
- CA-365946: Block VIF and VBD hotplug into dom0
- Update datamodel lifecycle
- CP-39805: Adapt xenopsd's cli to new cmdliner
- CP-39805: Adapt rrd tools to new cmdliner interface
- CP-39805: Adapt xapi-storage-cli to new cmdliner
- CP-39805: Adapt vhd-tool to new cmdliner
- CP-39805: Adapt xcp_service to new cmdliner interface
- CP-39805: Adapt xapi-guard to new cmdliner
- CP-39805: Adapt message-switch to new cmdliner
- CP-39805: Adapt xapi-gzip to new cmdliner
- CP-39805: Adapt nbd to new cmdliner
- CP-39805: Adapt idl clis to new cmdliner and rpclib
- CP-39805: Adapt xcp_service to new cmdliner
- CP-39805: Adapt xapi-idl binaries to new cmdliner
- CP-39805: Adapt xapi-storage(-script) to new cmdliner
- maintenance: consolidate idl's cli client argument parsing
- CP-39805: update tests to be compatible with rpclib +8.1.2
- xapi-idl: clients now better report cli errors
- maintenance: make gzip rules compatible with the dune cache

* Mon Jun 27 2022 Rob Hoes <rob.hoes@citrix.com> - 22.21.0-1
- xenopsd/xc: do not log error when querying for migrability
- CP-39996: Generate and push docs to xapi-storage
- CP-39806: remove code without a stable formatting
- CP-39806: avoid opening Threadext modules
- CA-365604: Support external user ssh into dom0 with name in unicode
- CA-367979: Bugfix - Wrong format of livepatch in returned updateinfo
- CA-368069: Got wrong kernel base build_id
- CP-39877: define activate_readonly method for SMAPIv3
- Remove unused xenopsd/Makefile and qemu-dm-wrapper
- CA-367979: Bugfix - Add RebootHost guidance wrongly when a livepatch failed
- CA-367979: Bugfix - Add new unit test for livepatch failure case
- CA-367979: Return changed guidance from host.apply_updates
- CA-367979: Bugfix - Remove RebootHostOnLivePatchFailure after a completion of update
- Refine unit test of eval_guidance_for_one_update

* Wed Jun 08 2022 Rob Hoes <rob.hoes@citrix.com> - 22.20.0-1
- CA-367738: Short-circuit auth of HTTP requests without auth header
- CA-365905 (XSI-1215): Create a temporary file in the target download folder (...)
- CA-355432: Fixed generation of method overloads.
- CP-39884: generalise interface to gzip/zstd-like tools
- CP-37091: Do not use a loop for only one iteration.
- CP-36245: Refine merge_livepatches function
- CP-32574: Apply livepatches
- CP-38583: add Host.last_software_update field with data/time
- maintenance: make xapi-xenops-tests more granular
- maintenance: move tests for platformdata together
- Use file type for is_raw_image()
- XenAPI.py: define how to build package in pyproject.toml
- xapi: avoid spawning processes
- Added Repository Update Unit Tests

* Wed May 18 2022 Rob Hoes <rob.hoes@citrix.com> - 22.19.0-1
- libs/uuid: run tests only in the uuid package
- CP-39805: Avoid deprecated bindings in mtime
- Datamodel: replace some recent rel_next entries
- CA-366801: xsh: fix XAPI blob sync and EBADF
- CP-38688 introduce Message.destroy_many() API/CLI call
- Upgrade VM runtime state when xenopsd restarts
- CA-367120: Missing net new RPMs in picking up metadata from updateinfo
- CA-367120: Add un-installed packages into accumulative update list
- CA-367120: Add debug logs for outputs of YUM/RPM command lines
- CP-38688 make Message.destroy_many() async, too
- XSI-1246/CA-367232: Daily license re-apply fails is HA is enabled
- Filter input dns when reconfiguring a pif IP(v6)
- CA-366309: ignore HA when checking update readiness

* Tue May 10 2022 Christian Lindig <christian.lindig@citrix.com> - 22.18.0-2
- CP-39640 add zstd dependency for suspend/migration stream compression

* Wed Apr 27 2022 Rob Hoes <rob.hoes@citrix.com> - 22.18.0-1
- CA-366014: pass -dm qemu to UEFI qemu too
- CP-39551: avoid warnings in xapi
- Don't use --force in gzip decompress
- CP-34028: Replace Uuidm with Uuid wherever possible
- CP-32574: Life-patch support part 1
- CA-366098: Raise internal xenopsd error on task timeout

* Wed Apr 20 2022 Rob Hoes <rob.hoes@citrix.com> - 22.17.0-1
- Add binary xapi_gzip for testing Xapi_compression
- CA-366430: do not wipe PK.auth/dbx.auth

* Tue Apr 19 2022 Rob Hoes <rob.hoes@citrix.com> - 22.16.0-1
- CA-366428: Add temporary feature 'Internal_repo_access' to allow update in mix mode
- Add `9pfs` backend to vbds
- Sync varstore certificates in XAPI with those on disks
- CP-39551: avoid warnings
- Fixes regarding DNS management in IPv6
- ci: fix testing of xapi-xenstored in newer opam's sandboxes

* Wed Apr 13 2022 Rob Hoes <rob.hoes@citrix.com> - 22.15.0-1
- CA-364138 XSI-1217: fix FD leak, Unix.EMFILE
- CA-365900: Clean up remanent stunnel client proxy
- CA-359978: Flush IP addresses when switching from static to DHCP
- CA-355588: users in pool admin group which contains # can not ssh into dom0
- CP-35846: Restrict access to internal yum repo server (members only)

* Fri Apr 01 2022 Rob Hoes <rob.hoes@citrix.com> - 22.14.0-1
- CA-363700: update xenopsd platformdata if rtc-timeoffset changes
- CA-365474: Synchronize trust roots at startup
- Make Xapi_compression.compress more polymorphic

* Mon Mar 28 2022 Rob Hoes <rob.hoes@citrix.com> - 22.13.0-1
- CA-365130: print exception on backup failure
- CA-365130: Print the name of signals in FE exceptions
- CA-365121: pool join: require common xapi versions
- CA-364021: reload certificates offered after emergency-reset-server-certificate
- CA-365438: Retrieve updateinfo.xml.gz file path from repomd
- CA-365438: Retrieve group file path from repomd
- CA-365516: CLI: protect cmdtable population with mutex
- CP-33973: disable DMC
- Fix and extend bugtool plugins

* Wed Mar 23 2022 Rob Hoes <rob.hoes@citrix.com> - 22.12.0-2
- Add dependency on pvsproxy to xcp-networkd

* Tue Mar 15 2022 Rob Hoes <rob.hoes@citrix.com> - 22.12.0-1
- CA-364630: Add [post|put]_services_xenops to client auth permission list
- CA-364450: Fix YUM repo config for repo metadata checking
- CP-39209: Add new field 'gpgkey_name' in repository object
- CA-364138: log when about to stop varstored and varstore-guard
- CA-365279: Client-cert auth: use CAfile
- CP-39375: Remove RPM gpgcheck in reposync
- CA-365112: Permit pool admin username with space to ssh login
- Fist point of cert exchange: keep all operations
- maintenance(ocaml): remove warnings
- maintenance: avoid using Cstruct.len
- maintenance: replace Lwt_unix.yield usages
- maintenance: dedicate a test binary for repository test_repository_helpers
- maintenance: remove most usages of Re.Str

* Thu Mar 03 2022 Rob Hoes <rob.hoes@citrix.com> - 22.11.0-1
- CP-38450: Add pool.set_wlb_enabled permission for client auth
- REQ-403 add cert checking for clusterd

* Mon Feb 28 2022 Rob Hoes <rob.hoes@citrix.com> - 22.10.0-1
- CA-363903: Winbind does not rotate keytab file
- CA-363903: Enable UPN format in hcp_users
- CA-363903: Rotate machine password on Closest KDC
- CA-362704: Hide proxy_username and proxy_password for repo proxy
- CA-362704: Remove credential related info from remote repository conf file

* Mon Feb 21 2022 Rob Hoes <rob.hoes@citrix.com> - 22.9.0-1
- CP-39031 keep more xapi version details for Host.software_versions
- CP-38462: Recognise ethtool-advertise on PIFs
- CP-38763: Enforce kerberos protocol talking with DC

* Tue Feb 15 2022 Rob Hoes <rob.hoes@citrix.com> - 22.8.0-2
- Bump release and rebuild with OCaml 4.13.1 compiler.

* Mon Feb 14 2022 Rob Hoes <rob.hoes@citrix.com> - 22.8.0-1
- CP-38610: Automatically record the versions of new datamodel elements
- Update lifecycles for existing API elements
- Update version comparison for numbered versions
- Replace rel_next with actual versions
- CA-363633: Always take the generation-id directly from xapi

* Wed Feb 09 2022 Rob Hoes <rob.hoes@citrix.com> - 22.7.0-1
- xenopsd: explicitly clean VM state if VM_restore failed during VM_receive_memory
- CA-363207: SSH access failing when using AD groups with spaces in name
- XSI-791/CA-343760: Make reboot equal to shutdown+start for CPUID changes
- CA-362924: Fix typo when syncing repository fails
- XSI-1175 make message limit configurable
- Maintenance: reformat with new ocamlformat version
- CA-363391: fix wake-on-lan script
- Use Filename to concat varstore dir and file
- CA-363154: Use repoquery to get available updates
- CA-363154: Remove usage of 'yum list updates'
- CA-363154: Ignore errors in repo update
- CA-363154: Use repoquery to get installed packages

* Thu Feb 03 2022 Rob Hoes <rob.hoes@citrix.com> - 22.6.0-1
- CA-361209: When using WoL find the remote physical PIF
- CA-361209: add vlan references to PIF's cli records
- REQ-403 Enable TLS verification by default
- REQ-403 make cron job for cert rotation conditional
- Fixes to prepare for OCaml upgrade

* Wed Jan 26 2022 Rob Hoes <rob.hoes@citrix.com> - 22.5.0-1
- CP-38850 add xapi.conf option for cert-expiration-days
- nbd: include the test binary into xapi-nbd package
- ocaml/tests: workaround opam's sandbox on db upgrade test
- use TMPDIR on tests if possible
- CP-38892: add role.is_internal field
- Update API version; record yangtze schema version

* Tue Jan 11 2022 Rob Hoes <rob.hoes@citrix.com> - 22.4.0-1
- Merge varstored-guard

* Mon Jan 10 2022 Rob Hoes <rob.hoes@citrix.com> - 22.3.0-1
- Merge sm-cli

* Mon Jan 10 2022 Rob Hoes <rob.hoes@citrix.com> - 22.2.0-1
- Merge xapi-nbd

* Mon Jan 10 2022 Rob Hoes <rob.hoes@citrix.com> - 22.1.0-1
- Merge wsproxy

* Mon Jan 10 2022 Rob Hoes <rob.hoes@citrix.com> - 22.0.0-1
- fix (http-svr): allow : in passwords when using basic auth
- maintenance (http-svr): simplify base64.decode usage

* Fri Dec 17 2021 Rob Hoes <rob.hoes@citrix.com> - 21.4.0-1
- xapi/import: report duplicate mac seeds on import as such
- Add `ignore_vdis` to `VM.snapshot` method
- Fix description of configure_repository_proxy
- CP-38759: Add pool.disable_repository_proxy
- CP-38701: Restrict client-cert role
- CA-361988 execute cluster host_resync always locally

* Fri Dec 10 2021 Edwin Török <edvin.torok@citrix.com> - 21.3.0-3
- Add coverity macros

* Tue Dec 07 2021 Edwin Török <edvin.torok@citrix.com> - 21.3.0-2
- CP-38218: obsolete xsi{f,o}stat by installing xapi-rrd2csv

* Fri Dec 03 2021 Rob Hoes <rob.hoes@citrix.com> - 21.3.0-1
- add setter for `Task.result` & `Task.error_info`
- Use stunnel proxy to access internal YUM repo
- Enable to set a `Task`'s `resident_on` field.
- CA-361151: Ldap does not work for cross domain 1-way trust
- CA-361151: remove 'winbind offline logon = Yes'
- CA-361221: utf8_recode: use Uutf.{Buffer.add_utf_8,String.fold_utf_8} instead of Uutf.{encode,decoder}
- CA-361221: utf8_recode: avoid allocations if string is all utf8
- CA-361220: Do not leak xsclient thread
- CA-361220: xenopsd: introduce TASK.destroy_on_finish
- CA-361220: xenopsd: avoid space leak in VM.import_metadata_async
- CP-35957: Update datamodel_pool for pool.configure_repository_proxy
- CP-35957: Add repository proxy configurations in syncing

* Thu Nov 25 2021 Rob Hoes <rob.hoes@citrix.com> - 21.2.0-2
- Bump release and rebuild

* Thu Nov 25 2021 Rob Hoes <rob.hoes@citrix.com> - 21.2.0-1
- Introduce session.client_cert field
- CA-360754: exclude client-cert sessions from revalidation
- CA-360951: Failed to lookup workgroup from domain as DNS cache

* Wed Nov 24 2021 Edwin Török <edvin.torok@citrix.com> - 21.1.0-2
- Bump release and rebuild

* Tue Nov 23 2021 Rob Hoes <rob.hoes@citrix.com> - 21.1.0-1
- Fix typo in message name
- CA-360997: Don't reject imports if the host's major version is larger

* Fri Nov 19 2021 Rob Hoes <rob.hoes@citrix.com> - 21.0.0-1
- Import message-switch, xcp-idl, xapi-storage, xapi-storage-script


* Tue Nov 16 2021 Rob Hoes <rob.hoes@citrix.com> - 1.331.0-1
- CA-359869: Make Sysfs.list robust against disappearing devices
- CA-360634: Change the allowed role of host.apply_updates to pool operator
- CA-360485: Fix SR-IOV capability detection
- CA-359714: update-precheck: fix uninitialised variable
- CA-360577: Add RBAC checking for client cert HTTPs requests

* Wed Nov 10 2021 Rob Hoes <rob.hoes@citrix.com> - 1.330.0-3
- Bump release and rebuild

* Mon Nov 08 2021 Christian Lindig <christian.lindig@citrix.com> - 1.330.0-1
- CA-359975: set the IP in /etc/issue on first boot
- Copied README from last draft, and actually signning the commit this time
- Making comment start with an uppercase
- CP-38309 make TLS more explicit in clusterd interface

* Wed Oct 27 2021 Edwin Török <edvin.torok@citrix.com> - 1.329.0-1
- vhd-tool: stress test compatibility with python3
- vhd-tool: Adapt stress-test to alcotest 1.0
- CP-38046: Add token in pool.sync_updates to support repository client authentication

* Thu Oct 21 2021 Rob Hoes <rob.hoes@citrix.com> - 1.328.0-1
- Merge xcp-networkd

* Thu Oct 21 2021 Rob Hoes <rob.hoes@citrix.com> - 1.327.0-1
- CA-356541 migration debug msg: ensure host is defined
- Replace ETCDIR by ETCXENDIR everywhere in scripts/

* Tue Oct 19 2021 Rob Hoes <rob.hoes@citrix.com> - 1.326.0-1
- Merge xenopsd and squeezed

* Wed Oct 13 2021 Rob Hoes <rob.hoes@citrix.com> - 1.325.0-1
- stunnel/gencert services: use Wants rather than Requires

* Wed Oct 13 2021 Rob Hoes <rob.hoes@citrix.com> - 1.324.0-1
- CHCLOUD-109: Remove checking on 'description' field in updateinfo
- CA-357075: Handle error from get_cluster_config call during RPU
- CA-359835: Enable 'Updates' feature in rolling pool update

* Mon Oct 11 2021 Rob Hoes <rob.hoes@citrix.com> - 1.323.0-1
- Maintenance: remove warnings
- CA-359214: Only restart stunnel if the config file has changed

* Fri Oct 01 2021 Rob Hoes <rob.hoes@citrix.com> - 1.322.0-1
- XenAPI.Session: raise exception on attempted forwarding of python magic methods
- CA-358904 REQ-403  cross pool migration must not use cert checking
- CA-356358: enable clustering daemon before attempting RPC call to fetch pems
- CA-358326 log cron job for cert refresh in syslog
- Remove old-style xva import code (finally)
- xe: remove prefix-match workaround
- CA-357785: Stop metrics binaries from logging to stdout
- maintenance: remove option to daemonize metric collectors
- CA-359226 add fist point to backdate new certs during testing

* Wed Sep 22 2021 Rob Hoes <rob.hoes@citrix.com> - 1.321.0-1
- Merge tapctl and vhd-tool
- Upgrade to dune 2.0

* Tue Sep 21 2021 Rob Hoes <rob.hoes@citrix.com> - 1.320.0-1
- CA-358904 REQ-403  cross pool migration must not use cert checking
- CA-359076: avoid DB calls when starting management server
- CP-38206: Merge xen-api-libs-transitional

* Fri Sep 17 2021 Rob Hoes <rob.hoes@citrix.com> - 1.319.0-1
- CA-358898: handle IPv6 state when management disabled

* Thu Sep 16 2021 Rob Hoes <rob.hoes@citrix.com> - 1.318.0-1
- CP-35393: Introduce client_certificate_auth
- CP-34726: Use a separate service and port for the client cert auth
- CP-34727: configure unix socket for client certificate auth
- CP-36249: Reconfigure management server when en/disabling client certificate auth
- CP-37692: Introduce RBAC role for client-auth sessions
- Use port 443 for client certificate auth (again)
- Duplicate cipher options in stunnel SNI service
- Change role for repository-related calls to pool-operator
- CP-37598: Add feature flag to restrict updates from a repository
- Fix missing xenopsd diagnostics from bugtools
- Fix handling of web-dir parameter
- CA-356959: Decide user account locked out by lockoutTime
- CA-358568: Password expired could not show on XenCenter
- CA-358816: Updated subject name in DC does not get updated in pam

* Mon Sep 13 2021 Rob Hoes <rob.hoes@citrix.com> - 1.317.0-4
- CA-358445: move %pre section to xcp-rrdd subpackage

* Mon Sep 06 2021 Rob Hoes <rob.hoes@citrix.com> - 1.317.0-3
- CA-358445: add rrdmetrics group (missing in xcp-rrdd merge)

* Fri Sep 03 2021 Rob Hoes <rob.hoes@citrix.com> - 1.317.0-2
- Bump release and rebuild

* Thu Sep 02 2021 Rob Hoes <rob.hoes@citrix.com> - 1.317.0-1
- CP-37370 add certificate-refresh to cron.daily
- CP-37370 revert this for release: use cron.hourly

* Wed Sep 01 2021 Rob Hoes <rob.hoes@citrix.com> - 1.316.0-1
- Specsavers: merge xcp-rrdd
- CP-37590: Replaced negative language within `FriendlyErrorNames.resx`
- CP-37590: Replaced negative language within `datamodel_errors.ml`
- CP-37590: Remove useless override in C# SDK generation
- Amend typos in errors datamodel
- Undo TLS verification change from v1.315.0, which was incomplete

* Thu Aug 26 2021 Christian Lindig <christian.lindig@citrix.com> - 1.315.0-1
- Enable TLS verification by default

* Wed Aug 25 2021 Christian Lindig <christian.lindig@citrix.com> - 1.314.0-1
- CA-357025 enable TLS cert checking for pool and WLB together

* Wed Aug 25 2021 Christian Lindig <christian.lindig@citrix.com> - 1.313.0-1
- Add datamodel option to log Db.X.destroy calls
- CA-356441: reload-or-restart sshd to apply sshd configuration
- REQ-403 CA-356724 unix time serial number to xapi-pool-tls.pem
- Stunnel.reload: wait 5s by default
- CA-355657 wait before serving refrehed SSL cert
- Fix issue #4491: USB device reset for Privileged VMs
  (with PCI device attached) is not working due to bad argument '-r'
- CP-36863: Expose local YUM repository only on TLS interface
- CA-357151 REQ-403 add joiner's ca certs to db
- CA-357151 REQ-403 consistent output about ca certs
- CA-356854 REQ-403 ejected hosts come back with verification enabled
- REQ-403 revert me! FIRSTBOOT_ENABLE_TLS_VERIFICATION=false
- CP-37866 add Host.tls_verification_enabled field
- CA-354374: Update pool_cpuinfo and pool_features after
  the ejected host having been destroyed
- CP-37898: Make winbind encryption types configurable
- CA-357417 REQ-403 ensure valid cert alerts are not deleted

* Mon Aug 09 2021 Edwin Török <edvin.torok@citrix.com> - 1.312.0-4
- Re-enable upgrade-pbis-to-winbind

* Mon Aug 02 2021 Rob Hoes <rob.hoes@citrix.com> - 1.312.0-3
- Temporarily revert upgrade-pbis-to-winbind requirement

* Thu Jul 29 2021 Rob Hoes <rob.hoes@citrix.com> - 1.312.0-1
- Merge winbind feature branch
- REQ-403 change type of cert generated during cert refresh

* Thu Jul 29 2021 Rob Hoes <rob.hoes@citrix.com> - 1.311.0-1
- CP-37571 REQ-403 add fist to Cert_distrib.exchange_certificates_in_pool

* Thu Jul 29 2021 Rob Hoes <rob.hoes@citrix.com> - 1.310.0-1
- REQ-403: failed_login_alert_freq
- Add explicit package to dune tests
- REQ-403 concurrency fixes pt 4
- Revert "REQ-403 concurrency fixes pt 4"
- maintenance: add copyright to cert_distrib files
- REQ-403 use pool ops rather than cert distrib mutex
- REQ-403 replace exchange_certificates_on_join lock
- REQ-403 remove exchange_certificates_among_all_members lock
- REQ-403 replace exchange_ca_certificates_with_joiner lock
- REQ-403 replace copy_primary_host_certs lock
- REQ-403 pool ejectees should remove trusted ca certs
- ci: run format on future feature and lcm branches
- configure: work around read-only /tmp found in opam's 2.1.0
- CA-356977 REQ-403 fix broken external auth for Host.reset_server_certificate

* Mon Jul 19 2021 Rob Hoes <rob.hoes@citrix.com> - 1.309.1-1
- Revert "Remove unused function"
- qualitygate: expect 1 instance of "=="

* Mon Jul 19 2021 Rob Hoes <rob.hoes@citrix.com> - 1.309.0-1
- Import xen-api client
- CP-36098 don't refresh certs if any host offline
- quality-gate: error if somebody used physical equality
- REQ-403 define how to generate cluster certificates
- REQ-403 give cluster daemon pem information
- CP-36097 REQ-403 write_pem API impl
- CP-36097 REQ-403 cluster must have a pem file before enabling tls verification
- CP-36097 REQ-403 cluster pems never expire
- CP-36097 REQ-403 use result monad rather than exceptions in selfcert
- CP-36097 REQ-403: maybe restart cluster daemon on cert refresh

* Thu Jul 08 2021 Christian Lindig <christian.lindig@citrix.com> - 1.308.0-1
- CA-355629 use hostname for CN in host cert

* Mon Jul 05 2021 Rob Hoes <rob.hoes@citrix.com> - 1.307.0-1
- CP-36098 introduce host-refresh-server-certificates
- CP-36098 add path argument to Gencertlib.Lib.install_server_certificate
- CP-36098 new API: host.refresh-host-certficate
- CP-36098 introduce pool op cert_refresh
- CA-355657 XSI-1037 reduce load during bugtool
- Maintenance: fix unixpwd warnings about loosing const qualifier
- Maintenance: fix indent in unixpwd
- CA-341715: control-domain-params-init: skip on upgrade
- CA-355625 reload Stunnel instead of restart after cert change
- CA-355625 remove dead code
- CA-341715: fix control-domain-params-init
- REQ-403 copy_primary_host_certs API call
- REQ-403 am i missing certs thread
- REQ-403 only exchange certs between primary and joiner during pool.join
- REQ-403 best effort distribution of joiner's pool certs to all hosts
- REQ-403 check for missing certs only when db connection established

* Fri Jun 25 2021 Edwin Török <edvin.torok@citrix.com> - 1.306.0-1
- REQ-403 update_ca_bundle lock
- Only add XAPI message for VM when migration is live and intrapool

* Thu Jun 24 2021 Edwin Török <edvin.torok@citrix.com> - 1.305.0-1
- Remove unnecessary scope restriction Result
- CA-354414 perform best effort Pool.eject cleanups
- REQ-403 cert_distrib lock
- CA-355571: Include accumulative updates for updates description and guidances
- CA-355571: Refine precedence between guidances
- CA-355571: Unit Tests: Include accumulative updates for updates description and guidances
- CA-355571: Unit Tests: Refine precedence between guidances
- Add more messages to a VM lifecycle

* Fri Jun 11 2021 Rob Hoes <rob.hoes@citrix.com> - 1.304.0-1
- CA-354260 REQ-403: check certs haven't expired before installing them
- CA-354834 log ref, uuid when adding CA cert
- Fix update-ca-bundle.sh hangling of deleted certs
- CP-37014 verify TLS-based RPC before enabling it
- CA-354834 log ref, uuid when adding CA cert
- CA-355179: Support epoch in RPM
- CA-355179: Support epoch in RPM: Update unit tests
- CA-355179: Support epoch in RPM: Add unit tests
- CA-355180: Improve parsing output of 'yum list updates'
- Added missing release date and restored as yet unreleased versions in the API docs.
- Build the doc-json target as part of the install target. Restructured output.
- Remove pool.slave_network_report
- Audit log: extend suppression to calls with _ separators
- CP-36178: Add basic precheck function for updates
- Removed rel_honolulu as it contained no API changes. Updated last_known_schema_hash.
- fixup! CA-355179: Support epoch in RPM
- Fix SDK build

* Thu May 27 2021 Rob Hoes <rob.hoes@citrix.com> - 1.303.0-1
- CA-354689 don't fail if host cert to be removed doesn't exist
- Maintenance: reformat code
- xapi_pool_helpers: refactor call_fn_on_hosts
- C# SDK: Fixes to generated code:
- CP-35955: Datamodel: Add pending_guidances for host
- CP-35955: Datamodel: Add pending_guidances for VM
- CP-35955: Bump up last_known_schema_hash
- CP-35955: Add absolute guidances in pending_guidances
- CP-35955: Clean up pending guidances
- CA-355039: Support single guidance from one update in updateinfo.xml
- Adapt xe-reset-networking for IPv6

* Thu May 20 2021 Rob Hoes <rob.hoes@citrix.com> - 1.302.0-1
- CP-35348 cover alerts for internal and CA certificates
- xapi-cli-protocol: make unit-tests runnable
- fix: cli protocol tests cannot depend on xapi-cli-server
- xe-enable-ipv6 edits net.ipv6.conf.{ all | default }.disable_ipv6
- Maintenance: replace deprecated Listext.assoc
- Set IPv6 parameters in check_network_reset
- cert_distrib: refactor go method
- CP-36866: Generalize code for certificate distribution
- CP-36866: block pool join when ca certificates might conflict
- CP-36866: Distribute CA certificates on join

* Mon May 17 2021 Rob Hoes <rob.hoes@citrix.com> - 1.301.0-1
- Centaurus repository APIs: merge from feature/centaurus/master-1


* Mon May 10 2021 Rob Hoes <rob.hoes@citrix.com> - 1.300.0-1
- CP-35523: Always accept requests from the unix socket

* Fri May 07 2021 Rob Hoes <rob.hoes@citrix.com> - 1.299.0-1
- CP-35523: Block access to the website on port 80

* Thu May 06 2021 Rob Hoes <rob.hoes@citrix.com> - 1.298.0-1
- CP-36744: Allow users to reenable tls cert checking
- CA-329462 Cluster.create should clean up if it fails
- ci: quality-gate shell script
- CA-353388: Control debug level by debug_stunnel env variable
- CP-36658 remove certs of host when it is ejected
- CA-349123: Tweak previous hotplug fix
- CA-353553 add API error for when NVidia GPU is misconfigured
- CA-353747 accept RSA and EC private key headers in PEM
- CA-353747 add negative test case
- CP-34467: Exchange certificate when a hosts joins a pool
- CP-34467: simplify certificate distribution

* Tue Apr 27 2021 Rob Hoes <rob.hoes@citrix.com> - 1.297.0-1
- CP-34467: Pre-join checks for TLS verification
- CA-353309: Create correct filters for uninstalling ca certs
- CP-34467: Avoid Not_found error when getting remote pool
- CP-36750: Block enabling TLS verification on pool ops
- Enable to choose a migration network in `VM.pool_migrate`:
- CA-349123: Fix metadata race in VBD/VIF plug

* Thu Apr 22 2021 Rob Hoes <rob.hoes@citrix.com> - 1.296.0-1
- REQ-403: Display expiry for certificates on the cli
- CA-341715: Sync certificates after bringing up mgmnt IF
- CP-36690 at startup, sync host certs with DB
- CP-36690 fix update_certificates at startup

* Wed Apr 14 2021 Rob Hoes <rob.hoes@citrix.com> - 1.295.0-2
- Bump release and rebuild

* Wed Apr 14 2021 Rob Hoes <rob.hoes@citrix.com> - 1.295.0-1
- CP-36509 update db for xapi_ssl.pem on startup if changed
- CP-36509 simplify cert decoding
- CP-36509 add MLI for certificates_sync module
- fixup! CP-36509 simplify cert decoding
- CP-36099 REQ-403 add type:host_internal to cert db schema
- CP-36099 REQ-403 add host_internal cert type to db utils
- CP-36099 REQ-403 only produce alerts for `host certs
- fixup! CP-36509 simplify cert decoding
- REQ-403 file system helpers
- REQ-403 declare cert related files/folders in xapi_globs
- CP-36510 REQ-403 distribute certs during Pool.enable_tls_verification
- CA-353011: Clean up certificates from unknown hosts
- CP-34469 on pool eject, remove host certificates
- XSI-995 handle case where pci doesn't exist in VM.power_state_reset

* Thu Apr 01 2021 Rob Hoes <rob.hoes@citrix.com> - 1.294.0-1
- CP-36100 extend update-ca-bundle to handle pool certs
- maintenance: reformat
- REQ-403: remove deprecated host cert (un)install calls
- CA-36099 REQ-403 add name and type to certificate db record
- CP-36099 REQ-403 comment about cert locations
- REQ-403 CP-36099 remove / add certs to db when un / installing them
- REQ-403 CP-36099 initialize rng
- CP-36100-3 Use explicit config for TLS Stunnel verification
- CP-36100-3 set TLS verification default at Xapi startup
- CP-36100-3 verify VNC connections as a pool-level connection
- CP-36100-3 change name of Stunnel.verification_config
- CP-36100-3 make ~verify_cert:None more explicit
- CP-36100-3 count verify_cert:None in Makefile
- CP-36100-3 persist TLS emergency flag
- README file was left out of the package.
- CP-36100: format code around rrdd commands

* Fri Mar 26 2021 Rob Hoes <rob.hoes@citrix.com> - 1.293.0-2
- Bump release and rebuild

* Fri Mar 12 2021 Rob Hoes <rob.hoes@citrix.com> - 1.293.0-1
- Merge xen-api-sdk repo to 'ocaml/sdk-gen/' from commit 'e278e5de021b0f354d2a98810cf77ad3a1b7de40'
- CP-36113: Added targets for compiling the SDK generator and generating the SDK source code.
- Keep the java library and samples version in sync.
- Added the xen-api-sdk package to the tests.
- Auto-formatted files.

* Wed Mar 10 2021 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.292.0-2
- CP-36113: Merged the SDK into xapi.

* Mon Mar 08 2021 Rob Hoes <rob.hoes@citrix.com> - 1.292.0-1
- Initialise Mirage RNG on startup

* Fri Mar 05 2021 Rob Hoes <rob.hoes@citrix.com> - 1.291.0-1
- CP-36096: Generate two certificates at startup
- CP-36096: serve the new certificate for xapi:pool clients
- CA-352329: Revert original formatting of lists in xapi-cli-server
- xapi-cli-server: Consolidate formatting on comma-separated lists
- xapi-cli-server: consolidate formatting of semicolon-separated lists

* Tue Mar 02 2021 Rob Hoes <rob.hoes@citrix.com> - 1.290.0-1
- When creating bonds, use primary_member's primary_address_type
- When creating tunnels, use transport_PIF's primary_address_type
- When creating vlans, use tagged_PIF's primary_address_type
- make format
- When creating sriov networks, use physical_ref's primary_address_type
- CA-352111: Do not output on cronjobs unless there's an error
- xapi-cli-server: clean up imports and comments
- xapi-cli-server: be consistent when showing list of references
- xapi-cli-server: be consistent when showing lists
- REQ-403 CP-33822 add IP address as SAN in self-signed certs
- CP-36096: Move helper_hostname to xapi_aux
- CP-36096: Move functions that collect hostnames and ip to xapi-aux
- CP-36096: Hostnames for certificates are gathered consistently
- CP-36096: Allow any number of IPs in SAN
- CP-36096: Move format conversion of mgmt IP to the edge
- CP-36096: generate x509 extensions when the issuer is
- CP-33822: Use Unix.gethostname instead the hostname binary
- maintenance: restrict the usage of read_localhost_info
- Replace gethostbyname by getaddrinfo to support IPv6
- CA-265116 rename and deprecate Pool cert functions
- CA-265116 rename and deprecate Host cert funtions
- CA-265116 use new names for cert functions
- REQ-403 CP-34468 add Host.reset_server_certificate
- REQ-403 add module to split PEM files
- REQ-403 use Pem.parse_file
- REQ-403 introduce path to CA certificates
- REQ-403 CP-33822 enable_tls_verification
- REQ-403 CP-34461 emergency disable tls verification
- REQ-403 CP-34461 tls verification health check
- CP-34942: Update pem library for angstrom 0.14.0+
- REQ-403 CP-35584 deprecate wlb_verify_cert
- CP-35761: Add feature flag for TLS certificate checking
- REQ-403: add logging to cert related handlers
- CA-351391: Make certificate alerts ignore CA certs
- REQ-403 bump schema version
- CP-34643: Reduce usage of Listext
- maintenance: avoid warnings for unused names
- CP-32669: Remove vendored PCI library

* Tue Feb 23 2021 Rob Hoes <rob.hoes@citrix.com> - 1.289.0-1
- CP-36094 add SNI to stunnel server config
- Revert "CA-342527: Avoid traversing lists when possible"
- CP-34472 expose User-Agent from a context
- CP-34472 throw the correct error on auth failure
- CP-34472 ensure auth error is thrown correctly
- CP-34472 add ability to record login failures
- CP-34472 actually record login failures
- CP-34472 generate failed login alerts
- REQ-403 CP-34472 include IP address in login fail alerts
- REQ-403 CP-34472 use UTC in failed login alerts

* Tue Feb 16 2021 Rob Hoes <rob.hoes@citrix.com> - 1.288.0-1
- CA-342527: remove argument logging of VMPP messages
- CA-342527: Avoid traversing lists when possible
- xapi: remove unused json module
- maintenance: detect schema updates which are missing version bumps
- ci: count usages of List.hd
- Remove usage of List.hd in gencert

* Fri Feb 05 2021 Rob Hoes <rob.hoes@citrix.com> - 1.287.0-2
- Bump release and rebuild

* Tue Jan 26 2021 Rob Hoes <rob.hoes@citrix.com> - 1.287.0-1
- Support IPv6 in vncproxy
- ci: check whether code in PRs is formatted
- XSI-804 ensure HVM boot params consistent
- maintenance: default hvm boot policy constant
- CA-351323 XSI-828 fix snapshot metadata lookup

* Tue Jan 26 2021 Rob Hoes <rob.hoes@citrix.com> - 1.286.0-1
- CA-343646: generate certificate alerts
- CA-343646: Avoid using API when no alerts are going to be modified
- maintenance: format code with ocamlformat
- Allow migration on IPv6-only host

* Wed Jan 06 2021 Rob Hoes <rob.hoes@citrix.com> - 1.285.0-2
- Bump release and rebuild

* Mon Jan 04 2021 Christian Lindig <christian.lindig@citrix.com> - 1.285.0-1
- CP-34602: test get_server_localtime and message.get_since
- Add ipv6 addresses to this_is_my_address
- Wrap IPv6 addresses when creating URLs
- Continue fixing console location in IPv6
- CP-34643: Replace deprecated usages of pervasiveext

* Wed Dec 16 2020 Christian Lindig <christian.lindig@citrix.com> - 1.284.0-1
- CA-350253: cli_operations: use `set []` when clearing if available
- CA-320523: records: implement setting of the map for `xenstore-data`

* Wed Dec 02 2020 Christian Lindig <christian.lindig@citrix.com> - 1.283.0-1
- CP-34942: update dmidecode parser for angstrom 0.14
- CA-348700: Block VDI.copy if on-boot=reset

* Fri Nov 27 2020 Christian Lindig <christian.lindig@citrix.com> - 1.282.0-1
- Fix IPv6 console location

* Fri Nov 20 2020 Christian Lindig <christian.lindig@citrix.com> - 1.281.0-1
- ci: unpin packages on cleanup

* Wed Nov 18 2020 Edwin Török <edvin.torok@citrix.com> - 1.280.0-3
- Re-enabled automatic ocaml dependency generator

* Wed Nov 18 2020 Edwin Török <edvin.torok@citrix.com> - 1.280.0-2
- CA-349027: be explicit about the choice of sendmail implementation

* Thu Nov 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.280.0-1
- CA-332779: Update power_state first in force_state_reset_keep_current_ops
- CA-332779: Avoid VM.remove in maybe_cleanup_vm
- CA-347560: Call VM.import_metadata_async for MD updates

* Tue Nov 10 2020 Christian Lindig <christian.lindig@citrix.com> - 1.279.0-1
- CP-35021 VM.suspend - assert support for NVidia cards
- CP-35021 introduce new API error for vGPU suspend

* Thu Nov 05 2020 Christian Lindig <christian.lindig@citrix.com> - 1.278.0-1
- CA-347543 use /usr/bin/pool_secret_wrapper only if CC

* Thu Oct 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.277.0-1
- CP-35210: log why a private key or certificates failed to validate
- CP-32138: rely on systemd to have wsproxy available
- maintenance: update github actions dependency
- maintenance: Schedule weekly run for 1.249-lcm
- ci: do not cache unversioned packages, update versiones ones
- CA-347611 Revert "CA-332779: Update power_state first in
    force_state_reset_keep_current_operations"
- CA-347611 Revert "CA-332779: Avoid VM.remove in maybe_cleanup_vm"

* Thu Oct 22 2020 Christian Lindig <christian.lindig@citrix.com> - 1.276.0-1
- CA-332779: Update power_state first in
    force_state_reset_keep_current_operations
- CA-332779: Avoid VM.remove in maybe_cleanup_vm
- CP-35026 tell stunnel to provide inet address info
- CP-35026 utils for extracting IP addresses
- CP-35026 add client field to Context.t
- CP-35026 pass client info to the debug module
- maintenance: format

* Wed Oct 21 2020 Christian Lindig <christian.lindig@citrix.com> - 1.275.0-1
- CA-333441 - restarting ISCSI daemon after setting initiator IQN
- CA-333441: Do not fail the startup sequence if the iSCSI initiator
    cannot be set
- maintenance: allow tests to run in a sandbox
- fix: update ocamlformat metadata to work with 0.15.0
- maintenance: format code with ocamlformat

* Thu Oct 15 2020 Christian Lindig <christian.lindig@citrix.com> - 1.274.0-1
- fix: correctly show add_to_sm_config to logs

* Mon Oct 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.273.0-1
- Revert "CA-333441 - restarting ISCSI daemon after setting initiator IQN"

* Thu Oct 08 2020 Christian Lindig <christian.lindig@citrix.com> - 1.272.0-1
- CP-34942: update for rpclib 7 compatibility
- CP-34942: adapt to message-switch usage of result
- CP-34942: update for rpclib 8 compatibility
- CA-333441 - restarting ISCSI daemon after setting initiator IQN
- opam: add jobs for build and tests for all packages

* Mon Oct 05 2020 Christian Lindig <christian.lindig@citrix.com> - 1.271.0-1
- CA-333441 - restarting ISCSI daemon after setting initiator IQN
- Delete unimplemented HTTP action definitions
- Remove misleading comment on expose_get_all_messages_for
- CA-262525: add missing parameters to HTTP actions
- Add 2 new methods to the `Host` object

* Wed Sep 16 2020 Christian Lindig <christian.lindig@citrix.com> - 1.270.0-1
- Branding for the Stockholm release.
- CA-332605 Fixed Bad error message for vcpu/cores-per-socket
- maintenance: make call_script interface cleaner
- maintenance: reintroduce missing PSR unit tests
- maintenance: remove @ list concats in suite_alcotest
- maintenance: remove reference to unused file
- maintenance: Remove travis CI
- maintenance: remove unused pool op valid assert from mli
- define rel_next
- REQ-819 CA-34357 add PSR feature flag
- REQ-819 CA-34873 remove genptoken & genptoken.service
- REQ-819 CP-33774 PSR orchestration
- REQ-819 CP-33777 expose code to generate ptoken as a library
- REQ-819 CP-33777 real implementation
- REQ-819 CP-33777 store list of pool secrets rather than only one
- REQ-819 CP-33780 add pool secret rotation fistpoints
- REQ-819 CP-34357 add designate_new_master to pool operations
- REQ-819 CP-34357 block PSR if any pool operations are in progress
- REQ-819 CP-34379 don't proceed with rotation if PSR state is inconsistent
- REQ-819 CP-34873 generate pool secrets optionally via script
- REQ-819 CP-34936 don't log result from pool_secret_wrapper
- REQ-819 make PSR and HA mutually exclusive
- REQ-819 rel_next -> rel_stockholm_psr

* Wed Sep 16 2020 Ben Anson <ben.anson@citrix.com> - 1.269.0-2
- REQ-819 CP-34873: remove genptoken services

* Mon Sep 14 2020 Christian Lindig <christian.lindig@citrix.com> - 1.269.0-1
- CA-344268: Fix timing issue in PBIS available check
- CA-265116 clarify doc for CA Cert Revoc. Lists
- CP-33823 replace generate_ssl_cert with OCaml code for more control

* Mon Sep 14 2020 Christian Lindig <christian.lindig@citrix.com> - 1.268.0-1
- CA-322708 - VM must not be allowed to start during storage migration

* Tue Sep 08 2020 Christian Lindig <christian.lindig@citrix.com> - 1.267.0-1
- XSI-795 CA-343951 fix Nvidia version parsing

* Wed Sep 02 2020 Christian Lindig <christian.lindig@citrix.com> - 1.266.0-1
- CA-343769 get CC_PREPARATIONS from xs-inventory
- Do not lose backtrace in RBAC

* Fri Aug 28 2020 Christian Lindig <christian.lindig@citrix.com> - 1.265.0-1
- XSO-974: add full lifecycle to VM.last_booted_record
- maintenance: formatting
- maintenance: remove occurences of !=
- maintenance: remove occurences of ' == '
- maintenance: ensure all fistpoints work as expected
- Remove duplicate line from xapi.service
- CP-33121: open listext from its own library
- CP-33121: open xstringext from its own library
- CP-33121: open unixext from its own library
- CP-33121: open threadtext from its own library
- CP-33121: open pervasiveext from its own library
- CP-33121: open date from its own library
- CP-33121: Remove all open Stdext
- CP-33121: Stop depending on stdext

* Mon Aug 17 2020 Christian Lindig <christian.lindig@citrix.com> - 1.264.0-1
- CA-341155: Fix console refresh when starting management server
- Remove Xapi_mgmt_iface.rebind
- CA-342171 fix get_server_localtime
- CA-343230 improve bewildering HTTP 403 error
- CA-343230 assert (rather than assume) that update VBDs are attached
- xapi_mgmt_iface: restructure
- xapi_mgmt_iface: hide himn_addr ref from the interface
- Remove Xapi_network.detach call from Xapi_vlan.destroy
- Clear the HIMN state if the network is detached
- CA-342551: Avoid replacing certificate alerts

* Wed Aug 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.263.0-1
- Improve HA parameter derived from timeout (#4169)
- CA-343117: host-backup: Include /boot/efi in the tarball

* Thu Jul 30 2020 Christian Lindig <christian.lindig@citrix.com> - 1.262.0-1
- CA-319021 fixed resident_on field update issue
- maintenance: make format
- maintenance: do not link to system OCaml when using opam

* Fri Jul 24 2020 Christian Lindig <christian.lindig@citrix.com> - 1.261.0-1
- merger rrd2cvs into xapi
- CP-34439: ensure rrd2csv compiles alongside xapi
- CP-34439: tidy rrd2csv after merging into xapi

* Tue Jul 21 2020 Christian Lindig <christian.lindig@citrix.com> - 1.260.0-1
- CA-338596: Upload files limit should deal with the dot style
- CA-338608: Limit xe client to download files specified in the args
- opam: update dependencies
- ci: add github actions

* Fri Jul 17 2020 Rob Hoes <rob.hoes@citrix.com> - 1.259.0-2
- Remove the patches, which have now been upstreamed.

* Thu Jul 16 2020 Christian Lindig <christian.lindig@citrix.com> - 1.259.0-1
- CP-33121: Remove unused dependency on stdext's fun module

* Fri Jul 10 2020 Christian Lindig <christian.lindig@citrix.com> - 1.258.0-1
- Increase sharing of strings in database
- maintenance: remove Listext
- CA-341988 don't take basename of empty update key

* Fri Jul 03 2020 Christian Lindig <christian.lindig@citrix.com> - 1.257.0-1
- CA-341149: Ensure a wait happen when the heartbeat connection fails
- XSO-974: correctly reflect datamodel changes in stockholm
- pci: fix tests for all distributions

* Tue Jun 30 2020 Christian Lindig <christian.lindig@citrix.com> - 1.256.0-1
- Branding for the Stockholm release

* Sun Jun 28 2020 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.255.0-2
- Removed patch with branding for the Stockholm release as it has moved to the repo.

* Fri Jun 26 2020 Christian Lindig <christian.lindig@citrix.com> - 1.255.0-1
- capitalise 'PEM' in English translations of certificate error messages

* Thu Jun 18 2020 Christian Lindig <christian.lindig@citrix.com> - 1.254.0-1
- CA-340148: Format code with ocamlformat
- Fix use of close_in/out on Unixfd.with_connection
- CA-340776: disconnect from stunnel cleanly
- CA-340776: move stunnel disconnection to the end where it was
- maintenance: bump schema version
- CA-335033 avoid idle connections during VDI copy

* Tue Jun 16 2020 Christian Lindig <christian.lindig@citrix.com> - 1.253.0-1
- maintenance: move tar_helpers to xapi_aux
- maintenance: format code with ocamlformat

* Tue Jun 16 2020 Christian Lindig <christian.lindig@citrix.com> - 1.252.0-1
- fix pool config parsing

* Mon Jun 15 2020 Christian Lindig <christian.lindig@citrix.com> - 1.251.0-1
- CP-33121: remove stdext's hashtbl only usages
- CP-33121: Remove stdext's range usages
- CP-33121: remove stdext usages in xapi_vm_helpers
- CP-33121: Remove stdext's usages from xapi_xenops
- opam: add fedora depexts
- maintenance: remove compilation warnings
- CP-33121: remove stdext usages from xapi
- CP-33121: remove stdext's usages from xapi-cli-server
- maintenance: use label to remove warning
- maintenance: add direct dependencies to dune files
- CP-33121: remove stdext's usages from xapi-aux
- maintenance: add missing transitive dependencies to dune files
- maintenance: drop stringext dependency
- mainteance: reduce reliaance on sexplib
- adding sriov_configuration_mode `manual, Net.Sriov.enable return
    Manual_successful and respective handling

* Fri Jun 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.250.0-1
- Revert "Revert "CA-334811 assign xapi version automatically""
- Enable to create a VM in `Suspended` state with a `suspend_VDI` set
- Allow migrate_send during RPU
- Fix use of close_in/out on Unixfd.with_connection
- CA-340776: disconnect from stunnel cleanly
- maintenance: removed deprecated UTC assertion
- restructed Tar to remove warnings
- Open VxLAN port of VxLAN tunnels:

* Mon Jun 01 2020 Christian Lindig <christian.lindig@citrix.com> - 1.249.0-1
- maintenance: improve IMPORT_INCOMPATIBLE_VERSION error message
- maintenance: fix build with workspaces
- CA-337546: update to new Stunnel_cache API with Safe_resources support
- CA-337546: enable runtime warnings
- Revert "CA-334811 assign xapi version automatically"

* Fri May 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.248.0-1
- Format extauth_plugin_ADpbis
- maintenance: improve logging when loading db backup fails
- CA-334811 assign xapi version automatically
- CA-338602: lwsmd daemon should not be running when AD is not configured
- CA-338602: Enable nsswitch during bootup if host is authed with AD
- CA-337867: Expose 'scheduled_to_be_resident_on' to XAPI event
- CA-339526 make gc_compact call public
- CA-339329 firstboot scripts shouldn't sync DB when ugprading
- CA-339656 use HOME when generating SSL certificate
- CA-339656 print generate_ssl_cert output neatly
- CA-339656 add generate_ssl_cert to essential executables
- CA-338565: Improve error message for uploading file exceeds the limit.
- CA-337867: Expose 'VM.scheduled_to_be_resident_on' field (take 2)

* Tue May 19 2020 Christian Lindig <christian.lindig@citrix.com> - 1.247.0-1
- maintenance: prepare for ocamlformat

* Mon May 18 2020 Christian Lindig <christian.lindig@citrix.com> - 1.246.0-1
- CP-33121: Remove Stdext and Stdext.monadic usages from tests
- CP-33121: Remove Stdext and Stdext.monadic from xapi_database
- CP-33121: remove Stdext.monadic from quicktests
- CP-33121: remove Stdext and Stdext.monadic from xapi_datamodel
- CP-33121: Remove Stdext.Opt usages from xapi
- maintenance: prefer using Option.fold

* Mon May 18 2020 Christian Lindig <christian.lindig@citrix.com> - 1.245.0-1
- CA-339601: source the iqn conf file.

* Fri May 15 2020 Lin Liu <lin.liu@citrix.com> - 1.244.0-2
- CA-338596: Check filenames for xe upload and download files

* Tue May 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.244.0-1
- CA-338137: Fix upgrade case in generate-iscsi-iqn

* Wed May 06 2020 Christian Lindig <christian.lindig@citrix.com> - 1.243.0-1
- CA-336730 add debugging to help solve template timeout issue

* Wed Apr 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.242.0-1
- CA-338617: Use the FQDN if possible when generating certificates

* Wed Apr 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.241.0-1
- CA-334763: Show errors during metadata export/import
- CP-33511 reduced XenAPI sessions to one per mail-alarm script invocation
- CP-33511 code formatted using black
- CP-27904: use Pci instead of Pciutils
- CA-337113/CA-338521: No more Tools ISO by default
- CA-338423: Remove use of Tools SR from Quicktest

* Mon Apr 27 2020 Christian Lindig <christian.lindig@citrix.com> - 1.240.0-1
- Merge REQ-821: Separate out xapi's CLI server into its own library
- CP-33465: xapi-cli-server: initial library
- CP-33473: Remove deprecated CLI commands.
- CP-33457: Add field 'editions' to host class.
- CP-33457: Use RPC call in 'host_all_editions' CLI implementation.
- CP-33457: Get license editions by Host RPC call.
- CP-33489: Remove direct use Xapi_role.expr_no_permissions in gen_cmds.
- CP-33490: Remove use ExnHelper in CLI implementations
- CP-33400: xe command check to make sure uploaded files
- CP-33400: parse_eql use Astring lib
- CP-33451: Create diagnostics class
- CP-33503: Remove direct use of class_to_string and string_to_class in records.ml.
- CP-33212: Restrict CLI upload file size
- CP-33501: Move the "fake" RPC function into Xapi_cli
- CP-33501: Avoid use of Context in Xapi_cli
- CP-33452: cli server call Diagnostics.gc_compact to compact the heap
- CP-33494: Add Task.set_progress API call
- CP-33494: Eliminate uses of Db_actions and TaskHelper in Cli_operations
- CP-33453: cli server call Diagnostics.gc_stats to retrieve gc stats
- CP-33499: Refine cli_util.ml in CLI implementations.
- CP-33454: cli server call API to retrieve db stats
- CP-33455: cli server call Diagnostics.network_stats to
- CP-33455: Only pass the necessary params to API call
- CP-33493: Eliminate uses of Xapi_template in Cli_operations.
- CP-33540: Remove Diagnostic function session argument
- CP-33492: Remove use of Xapi_globs.* functions in CLI implementations
- CP-33498: Remove dependency of storage_interface in cli_operations
- CP-33492: Move the BIOS strings to constants.ml.
- CP-33454: cli server call API to retrieve db stats
- CP-33540: Fix sdk build failure by providing necessary docs
- CP-33496: Remove use of Xapi_http module in cli_operations.ml.
- CP-33496: Add Vpx_types in xapi types.
- CP-33456: Clean diagnostic_license_status with permitted modules
- CP-33551: Move Compression_algorithms into xapi_types
- CP-33491: Move out the role setter in pool_role
- CP-33496: Make xva.ml as module.
- CP-33496: Move xapi-xva into xapi-public
- CP-33496: Move table.ml to xapi-public
- CP-33552: Add API get_attached_live_hosts to SR
- CP-33556: Remove Importexport from cli server
- CP-33497: Remove dependency of Helper.get_localhost and Context
- CP-33552: Code refine basing on comments
- Reduce opam packages, rename xapi-public
- CP-33488: Move cli related files into xapi-cli-server folder.
- CP-33556: Remove Importexport from cli server
- Add xapi-inventory as dependency of xapi-consts.opam.

* Thu Apr 23 2020 Christian Lindig <christian.lindig@citrix.com> - 1.239.0-1
- Cp-32669: adapt tests to X509 0.11.0

* Tue Apr 21 2020 Christian Lindig <christian.lindig@citrix.com> - 1.238.0-1
- CP-32678: Use a variant instead of a boolean for certificates
- CP-32678: Add private key validation
- CP-32678: Add server certificate validation
- CP-32686: Don't generate diffie-hellman parameters
- CP-32686: follow shellcheck recommendations
- CP-32686: Server Certificate installation
- CP-32681: Add certificates to DB schema
- CA-265116: Better documentation for certificate API
- CA-265116: Distinguish CA certificates from server ones
- CP-32678: Return the certificate on install
- CP-32678: Add API to install server certificates
- CP-32678: Do not open stdext's Listext
- CP-32678: Add CLI to install server certificates
- CP-32681: store fingerprints as non-binary string
- CP-32663: Usage more natural language on errors
- CP-32696: Send expiring certificates alerts daily
- CP-32706: add emergency call to install a self-signed cert
- CA-337491: generate_ssl_cert now can replace existing servert cert
- CP-32696: avoid alerts on the 31st day
- CP-32696: Place message under a single root
- CP-32696: Use a separate test runner for alerts
- CA-337520: detect recently expired certificates as such
- CP-32695: Use UTC for dates in certificate errors
- CP-32708: prepare to detach install code from xapi
- CP-32708: Move certificate installation and validation to gencert
- CA-337731: reject files without certs for chains
- CA-337865: clear expired certificate alerts
- CA-337865: filter certificate alerts only once
- CP-32663: bump schema version
- CA-338141 mirror other_config when performing InternalAsync operation

* Fri Apr 17 2020 Christian Lindig <christian.lindig@citrix.com> - 1.237.0-1
- CA-337899 pass ciphersuites arg to sparse_dd
- CA-334756: add missing capabilities to SM features table
- CP-33292: add VDI read caching SM capability
- CP-31118: Avoid xapi as module name in logs
- CA-337929 remove gencert xapi-wait-init-complete dependency
- CA-337903 insert stunnel into xapi shutdown order
- CA-337875 base not always passed to sparse_dd

* Tue Apr 14 2020 Christian Lindig <christian.lindig@citrix.com> - 1.236.0-1
- CP-31116: simplify dbtest dune for database package
- CP-28222: Reenable testing for pci
- CP-28222: port db tests to alcotest and enable them on opam
- CA-337087 avoid race condition in Helpers.Task.wait_for
- CA-337087 fix uncancellable migrations

* Mon Apr 06 2020 Ben Anson <ben.anson@citrix.com> - 1.235.0-2
- REQ-811: fix stunnel config in xapi.spec

* Mon Apr 06 2020 Christian Lindig <christian.lindig@citrix.com> - 1.235.0-1
- CP-33380: update to x509 0.10.0

* Fri Apr 03 2020 Christian Lindig <christian.lindig@citrix.com> - 1.234.0-1
- maintenance: fix compiler warnings
- CP-32840 fix xapi according to Stunnel changes
- CA-32840 remove references to ciphersuites
- CP-32840 stub out Host.set_ssl_legacy
- CP-32840 deprecate ssl_legacy flag in host class
- CP-32840 stub out legacy ssl operations on pools
- CP-32840 xapi stunnel config shouldn't enable legacy options
- CP-33058 centralize cipherstring
- CP-32840 final clean up of legacy ssl related code/docs
- CP-32840 fix xapi according to Stunnel changes
- CA-32840 remove references to ciphersuites
- CP-33058 centralize cipherstring
- CP-33057 purge lingering stunnel configs
- CP-33057 rewrite init.d-xapissl script in ocaml
- CP-33057 replace usages of xapissl script with systemd
- CP-33057 increase number of file descriptors for stunnel@xapi
- CP-32840 enable fips for CC certification
- maintenance: move paths to xapi_globs
- CP-33243: gencert binary
- CP-33243: create systemd gencert service
- CA-336408 ensure legacy ssl is disabled on upgrade
- CP-33061 remove iLO script
- REQ-453 re-expose reconfigure_stunnel

* Fri Mar 27 2020 Christian Lindig <christian.lindig@citrix.com> - 1.233.0-1
- CA-336735: preserve formatting of stars for wlb recommendations

* Mon Mar 23 2020 Christian Lindig <christian.lindig@citrix.com> - 1.232.0-1
- improve invalid VIF map error message for intra-pool migration
- Fix build: drop Xcp_coverage
- Simplify build: drop coverage rewriter

* Fri Mar 20 2020 Christian Lindig <christian.lindig@citrix.com> - 1.231.0-1
- improve invalid VIF map error message for intra-pool migration
- travis: follow validator recommendations

* Tue Mar 17 2020 Christian Lindig <christian.lindig@citrix.com> - 1.230.0-1
- maintenance: don't generate empty modules
- CA-333610 generate multiple async client frontends
- CA-333610 modify server.ml to accept InternalAsync calls
- CP-32398 must not use POD when using SRIOV vGPU
- CP-32649: Use Stdlib's Result
- CA-336258: Remove unused function argument
- CA-336258: fix API forwarder for JSONRPC calls
- CA-333610 utility to try InternalAsync call with fallback
- CA-333610 avoid long running idle connection during migration
- maintenance: server_helpers interface file
- CA-336685 improve error for mem constraints violation

* Thu Mar 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.229.0-1
- Fix cluster_stack_in_use error message
- datamodel_common: add quebec release
- CP-32678: update to X509 0.9.0
- license: enable unit-tests
- tests: move daily license checks to the suite

* Fri Mar 06 2020 Christian Lindig <christian.lindig@citrix.com> - 1.228.0-1
- CA-334951: Use a variant to model recommendations
- CA-334951: Ignore 0-star recommendations from WLB
- CA-334951: Code hygiene
- CA-334951: Use a map instead of a hashtable
- CP-33121: Stop using Xstringext in cli_operations

* Mon Mar 02 2020 Christian Lindig <christian.lindig@citrix.com> - 1.227.0-1
- maintenance: json files must not be executable

* Mon Feb 24 2020 Christian Lindig <christian.lindig@citrix.com> - 1.226.0-1
- CA-334909: Only update if the update is needed
- CP-33121: remove Listext usages
- CP-33121: reduce Stdext usages from xapi_vm
- CP-33121: remove stdext usages from xapi_vm_appliance
- CP-33121: Reduce usage of Xstringext
- CP-33121: remove uneeded open lines

* Wed Feb 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.225.0-1
- Fix parsing of platform:cores-per-socket to avoid divide-by-0 error
- CP-32124: Set fips=yes explicitly for stunnel
- CP-32124: Remove 'LEGACY_CLIENT_ACCEPT' for stunnel
- CP-32124: Set the default log facility as 'authpriv'
- CA-331142: stunnel on server side close SSL sock unexpectedly
- CA-334797: Disable TLSv1.3 when legacy is true
- CP-32298: Move 40-generate-iscsi-iqn to a standalone service
- CA-325068: Move networking firstboot script to its own service
- CP-31090: Move prepare-control-domain-params script to its own service
- CP-31090: Move reset-and-reboot into a separate script
- CA-333712: use wrapped string type for pool internal API calls

* Wed Feb 05 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.224.0-2
- CP-31090: Migrate toolstack xenserver-firstboot scripts

* Tue Feb 04 2020 Christian Lindig <christian.lindig@citrix.com> - 1.224.0-1
- Mark OCaml source code files as not executable

* Tue Jan 28 2020 Christian Lindig <christian.lindig@citrix.com> - 1.223.0-1
- Branding for the quebec release; defined stockholm release; corrected
       field version; bumped client min/max version to 2.15.
- Remove xenserver-buildenv based Travis builds
- REQ-627 CA-333495 add Xapi_pci.dequarantine

* Fri Jan 24 2020 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.222.0-2
- Removed patch with Quebec branding (it is moving into the source code)

* Fri Jan 17 2020 Christian Lindig <christian.lindig@citrix.com> - 1.222.0-1
- CA-325582: do not open Listext in message_forwarding
- CA-325582: Move DB checks for SR removal to message_forwarding
- CA-325582: Allow forwarding SR operations to all hosts with related PBDs
- CA-325582: Remove SR DSs from memory on SR.forget and destroy
- CA-325582: fix some storage quicktests for pools

* Fri Jan 10 2020 Christian Lindig <christian.lindig@citrix.com> - 1.221.0-1
- CP-32461: Delete CPUID leveling checks from WLB

* Mon Jan 06 2020 Christian Lindig <christian.lindig@citrix.com> - 1.220.0-1
- CA-328130 extract usb speed attribute
- CA-328130 add usb speed field to api
- CA-328130 Make sure speed updated after update
- CA-328130 Fix usb_scan tests

* Mon Dec 09 2019 Christian Lindig <christian.lindig@citrix.com> - 1.219.0-1
- maintenance: remove Pervasives deprecated warnings
- CP-28369: remove unused daemonize code
- CP-32429: Modernize python2 code (automated)
- CP-32429: Modernize python2 code, needs manual fixes
- CP-32429: Fix invalid transformations from futurize
- CP-32429: Modernize python2 code, with manual fixes
- CP-32429: enable python3 testing
- CP-32429: Use python-3 compatible idioms on tests

* Wed Dec 04 2019 Christian Lindig <christian.lindig@citrix.com> - 1.218.0-1
- CA-325940 bind PCI before calling sriov-manage

* Fri Nov 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.217.0-1
- CA-330162 Allow explicit floppy userdevice
- CA-330162 Improve vbd-create error message
- fixup! CA-330162 make floppies a first class citizen
- CA-330162 make floppies a first class citizen
- CA-330961 Clean the yum cache before prechecking/applying an update
- maintenance: optimize Helpers.get_localhost

* Mon Nov 25 2019 Christian Lindig <christian.lindig@citrix.com> - 1.216.0-1
- CA-330979: set current_domain_type for slaves
- fix compiler warnings: Warning 52
- fix compiler warnings: (+++)
- fix compiler warnings: Re.get_ofs deprecated

* Mon Nov 25 2019 Christian Lindig <christian.lindig@citrix.com> - 1.215.0-1
- CA-313081 fix moving template between SRs

* Fri Nov 22 2019 Christian Lindig <christian.lindig@citrix.com> - 1.214.0-2
- Define branding for release Quebec

* Thu Nov 21 2019 Pau Ruiz Safont <pau.safont@citrix.com> - 1.214.0-1
- CA-330902 Improve logging
- CA-330902 host-bugreport-upload args via env vars
- CA-330902 Xapi_support.do_upload env vars
- CA-330919: Revert "CP-32138: rely systemd to have wsproxy available"

* Tue Nov 19 2019 Christian Lindig <christian.lindig@citrix.com> - 1.213.0-1
- fixup! CA-307578 Cluster_host.enable host starts clusterd

* Mon Nov 18 2019 Christian Lindig <christian.lindig@citrix.com> - 1.212.0-1
- CP-32437: update assert_can_boot_here documentation
- CP-32437: do the CPUID check inside assert_can_boot_here
- CP-32437: call assert_can_boot_here with appropriate do_cpuid_check
- CP-32437: use Map_check.getf instead of manipulating and passing around strings
- CP-32437: print a delta of features on changes and mismatches
- CP-32446: Support extra CPUID features for migration
- CP-32446: Enable AssertVMIsCompatible test and fix tests
- CP-32446: drop support for RPU from pre-Dundee hosts in CPU leveling

* Fri Nov 15 2019 Christian Lindig <christian.lindig@citrix.com> - 1.211.0-1
- CA-330693: Limit access to state.db to just root

* Fri Nov 15 2019 Christian Lindig <christian.lindig@citrix.com> - 1.210.0-1
- CA-307578 Cluster_host.enable host starts clusterd
- CA-330693: Limit access to state.db to just root

* Tue Nov 12 2019 Christian Lindig <christian.lindig@citrix.com> - 1.209.0-1
- CA-329466 Simplify logging for plugins' parameters
- CA-329835 Improve logging
- CA-329843 broaden usage of secrets API

* Mon Nov 04 2019 Christian Lindig <christian.lindig@citrix.com> - 1.208.0-1
- fixup! REQ-627 release PCI from VM when halted|suspended
- REQ-627 CA-328075 after migration, remove stale PCI

* Tue Oct 29 2019 Edvin Török <edvin.torok@citrix.com> - 1.207.0-1
- CA-327885: update NVIDIA multiple vGPU driver list
- Corrected spelling to match the docs. Use en-us spelling. Removed unused error.
- CP-32138: rely on systemd to have wsproxy available

* Thu Oct 24 2019 Christian Lindig <christian.lindig@citrix.com> - 1.206.0-1
- Fix a typo in comment

* Tue Oct 22 2019 Christian Lindig <christian.lindig@citrix.com> - 1.205.0-1
- REQ-627 release PCI from VM when halted|suspended
- REQ-627 handle multiple SR-IOV vGPUs
- CP-30647 Ignore /data/updated key
- CP-30647 whitespace
- CA-326241 Set resident_on manually for first task
- CA-326349 Log when slaves slow during startup
- CA-326349 Kill stunnel processes on restart

* Tue Oct 15 2019 Christian Lindig <christian.lindig@citrix.com> - 1.204.0-1
- Merge REQ-627 (SR-IOV support for NVidia GPUs)

* Tue Oct 15 2019 Christian Lindig <christian.lindig@citrix.com> - 1.203.0-1
- Revert "CA-32641 Orphaned dbsync tasks cleaned up"

* Mon Oct 14 2019 Christian Lindig <christian.lindig@citrix.com> - 1.202.0-1
- CA-326241 assign localhost_ref earlier

* Fri Oct 04 2019 Christian Lindig <christian.lindig@citrix.com> - 1.201.0-1
- Remove spammy log lines

* Tue Oct 01 2019 Christian Lindig <christian.lindig@citrix.com> - 1.200.0-1
- CA-326621 Remove VM.migrate op when finished

* Fri Sep 27 2019 Christian Lindig <christian.lindig@citrix.com> - 1.199.0-1
- CA-325988: Add a common dmidecode parser
- CA-325988: Use new parser for gathering OEM info
- CA-325988: Use first board only for baseboard strings
- CA-325988: Use new parser for bios and system strings
- CA-325988: Cleanups in string cleanups
- CA-325988: Tests added for dmidecode output handling
- CA-325988: Add fmt dependency to opam for tests

* Tue Sep 24 2019 Christian Lindig <christian.lindig@citrix.com> - 1.198.0-1
- CA-326244: do not include host name in log format
- Fix incorrect hostname in syslog: send HUP when hostname is changed

* Wed Sep 18 2019 Christian Lindig <christian.lindig@citrix.com> - 1.197.0-1
- CA-325330 add error for VGPU driver incompatibility

* Fri Sep 13 2019 Christian Lindig <christian.lindig@citrix.com> - 1.196.0-1
- CP-31859 Remove support for VSS
- maintenance: remove unused directory

* Tue Sep 10 2019 Christian Lindig <christian.lindig@citrix.com> - 1.195.0-1
- Revert "CA-326174: fix race condition between SR.scan and VDI.forget"

* Mon Sep 09 2019 Christian Lindig <christian.lindig@citrix.com> - 1.194.0-1
- CP-32055: Adapt x509 usage to >0.7

* Tue Sep 03 2019 Christian Lindig <christian.lindig@citrix.com> - 1.193.0-1
- CA-326174: fix race condition between SR.scan and VDI.forget
- Corrected the spelling of plug-in to be consistent with the docs.

* Fri Aug 30 2019 Christian Lindig <christian.lindig@citrix.com> - 1.192.0-1
- python: fix typo in readme, add link to examples
- CA-325988: do not lose newlines from dmidecode

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 1.191.0-2
- bump packages after xs-opam update

* Wed Aug 21 2019 Christian Lindig <christian.lindig@citrix.com> - 1.191.0-1
- travis: load vars from xs-opam repo
- Gather the list of host datasources
- Gather VM and SR data source lists too
- CP-12980: maintain import behaviour on package

* Thu Aug 15 2019 Christian Lindig <christian.lindig@citrix.com> - 1.190.0-1
- CA-311625: alarm only if the last attempt of PBD.plug fails
- CA-322204: write to log synchronously before fencing
- CA-325319 Fix host-display script console handling
- CP-12980: python xenapi: enable building package
- CP-12980: turn python xenapi into a module

* Wed Aug 07 2019 Christian Lindig <christian.lindig@citrix.com> - 1.189.0-1
- CP-31117: Remove implementation of obsolete VM options
- CP-31117: QEMU stub domains are no longer implemented

* Fri Aug 02 2019 Christian Lindig <christian.lindig@citrix.com> - 1.188.0-1
- CA-299343: Explain reason when DMC operation fails
- CP-31450: Add domid to Datapath.attach
- CP-31450: Fix toolstack always passing domid 0 to Datapath.attach
- CP-31980: Update Nvidia host driver white list that support multiple vGPU
- maintenance: report the actual power state on logs
- Remove obsolete lines from attach-static-vdis
- Remove obsolete network scripts
- Remove obsolete references to old network scripts
- Remove unused xapi-netdev dependency

* Thu Aug 01 2019 Rob Hoes <rob.hoes@citrix.com> - 1.187.0-3
- Remove obsolete network scripts

* Thu Aug 01 2019 Rob Hoes <rob.hoes@citrix.com> - 1.187.0-2
- Remove unused xapi-netdev dependency

* Tue Jul 30 2019 Christian Lindig <christian.lindig@citrix.com> - 1.187.0-1
- CA-316165: make test_network_event_loop more deterministic
- CA-316165: fix race condition in unit test
- CA-316165: speed up running the unit test
- CP-30614: Only link against libraries that do not use libxc
- CP-30614: Add unit test to check that the xenctrl dependency has not come back
- CP-30618: Disable host on startup in case of xen or libxc incompatibilities
- CP-30618: Prevent calls to xenopsd with incompatible xen/libxc
- CA-322045: make light_fuse idempotent

* Mon Jul 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.186.0-1
- CA-322045: tell XAPI to shut down only once
- CP-28368 Remove alcotest from test_highlevel
- CP-28368 Whitespace
- sr_health_check: Actually make the thread start instead of dead code
- Fix some partial application errors in the tests

* Tue Jul 23 2019 Rob Hoes <rob.hoes@citrix.com> - 1.185.0-1
- CA-322146: set NBD device scheduler and max_sectors to more efficient values

* Wed Jul 17 2019 Christian Lindig <christian.lindig@citrix.com> - 1.184.0-1
- CP-31729 Add auto_update_mac to Bond database record and cli
- CP-31729 Ensure PIF Bond master's MAC address matches primary slave
- CA-316165 Convert some Thread.delay to Delay.wait

* Wed Jul 10 2019 Christian Lindig <christian.lindig@citrix.com> - 1.183.0-1
- CA-316165: uplift Thread.delay thresholds to make relative timing more reliable
- CA-322749: Add configration variable nvidia_multi_vgpu_enabled_driver_versions
- Maintenance: silence Merlin warnings

* Mon Jul 08 2019 Christian Lindig <christian.lindig@citrix.com> - 1.182.0-1
- CA-322682: Remove PVS Proxy from a VM when it is templated
- CA-319960: Remove user KRBTGT from cache before checking
- Changed the release code name from plymouth to quebec.

* Mon Jul 01 2019 Christian Lindig <christian.lindig@citrix.com> - 1.181.0-1
- CA-321930 XSI-374 GPU compatibility check not done on snapshot revert
- CA-321930 XSI-374 Add logging
- CA-322710 improve clustering error message

* Tue Jun 25 2019 Christian Lindig <christian.lindig@citrix.com> - 1.180.0-1
- CA-321983: Write compatibility lookup file for NVidia VGPU types
- CA-321983: Updates for vgpu changes to xenops IDL
- CA-321983: Handle upgrade case in get_vgpu_compatibility_metadata
- CA-321983: Bring VGPU device numbers back to a range starting from 0
- CA-322450 xe-restore-metadata: ImportError: fsimage
- CA-322044: also throttle the automated API calls for SR.scan
- Revert "CA-320458: Upgrade vGPU default device id from 0 to 11"
- VGPU tests: check device/PCI-slot relationship
- Catch any exceptions in create_compat_lookup_file
- Remove unnecessary log line

* Fri Jun 21 2019 Christian Lindig <christian.lindig@citrix.com> - 1.179.0-1
- CA-321787: Block migrate/suspend/resume when there is no pGPU
- CA-322044: throttle number of active SR scans
- CP-31400: Improve API error text.
- List RRD directory once per monitor poll

* Tue Jun 18 2019 Christian Lindig <christian.lindig@citrix.com> - 1.178.0-1
- CA-320458: Upgrade vGPU default device id from 0 to 11
- CA-321654: domains must be stopped before xapi is
- CA-258385: Improved phrasing for errors thrown by assert_can_migrate.
- Replace /tmp/network-reset literal with Xapi_globs
- Travis: remove opam-coverage
- Modifications to the error messages for better compliance with the
  values exposed via the API clients.

* Thu Jun 06 2019 Christian Lindig <christian.lindig@citrix.com> - 1.177.0-1
- CA-320458: Upgrade vGPU default device id from 0 to 11
- Replace /tmp/network-reset literal with Xapi_globs
- Travis: remove opam-coverage

* Wed Jun 05 2019 Christian Lindig <christian.lindig@citrix.com> - 1.176.0-1
- REQ-720: CP-31058: Datamodel changes for multiple Nvidia VGPU support
- CP-29991: Host selection for multiple vGPU
- CP-30660: Dry run the allocate vGPU to pGPU
- CP-30756: Replace Base64 library
- CP-31058: Update Nvidia data structures according to idl change.
- CP-31122: Send vGPU uuid to Xenopsd.
- CP-31124: Add vGPU uuid as parameter to get metadata.
- CP-31160: Support for multiple vGPU creation
- CP-31321: Support extra_args for vGPU configration
- Add cases for multiple vGPUs in metadata test.
- Delete old way of parse Nvidia config file.
- Fix test failure.
- Fix unit test failures introduced by multi-vGPU code. (#3876)
- Improve UUID and code indentation.
- maintenance: whitespace
- Avoid xapi as module name in logs

* Wed May 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.175.0-1
- CP-30433: add uefi_certificates field (#3808)
- CP-30559 Use the API to add the uefi certificates
- CP-30434 Parse secureboot=auto
- CP-30440: always set pool certificate
- CP-30440: fix tarfile extraction
- CA-312227: fix extraction of uefi certificates
- CA-314381: fix race condition in secure boot startup
- .travis.yml: pin xapi subpackages
- Update for Plymouth release
- Pass in vm_uuid as well
- Use xs-opam's uefi branch for travis
- Revert "Use xs-opam's uefi branch for travis"

* Tue May 28 2019 Christian Lindig <christian.lindig@citrix.com> - 1.174.0-1
- CA-296827: Improve CLI log filter

* Mon May 20 2019 Christian Lindig <christian.lindig@citrix.com> - 1.173.0-1
- Remove the Xenctrl dependency in Monitor_master.update_pifs
- Drop the xencrtl dependency
- Quicktest still needs xenctrl

* Tue May 14 2019 Christian Lindig <christian.lindig@citrix.com> - 1.172.0-1
- CP-30614: Use rrd files to gather memory statistics

* Wed May 08 2019 Christian Lindig <christian.lindig@citrix.com> - 1.171.0-1
- CA-316241 redirect stderr output from probe-device-for-file
- CA-315688: Bumped API version to 2.14 for the plymouth release
- Do not autogenerate placeholders for unreleased API versions in the docs.

* Fri May 03 2019 Christian Lindig <christian.lindig@citrix.com> - 1.170.0-1
- CA-316165: workaround - disable CBT unit tests
- CA-316165: disable more unit tests that used Thread.delay
- Changed the checksum algorithm from SHA1 to xxHash,
  backwards compatability is maintained
- Revert "CP-30614: Use rrd files to gather memory statistics"

* Thu May 02 2019 Christian Lindig <christian.lindig@citrix.com> - 1.169.0-1
- CA-316165: workaround - disable nondeterministic unit test

* Thu May 02 2019 Christian Lindig <christian.lindig@citrix.com> - 1.168.0-1
- Move jemalloc into xapi.service (was: CA-289625)

* Mon Apr 29 2019 Christian Lindig <christian.lindig@citrix.com> - 1.167.0-1
- CP-30294: Bumped the API minor version and the client min/max version to 2.13
- CA-315107 Create xapi-init-complete systemd target

* Tue Apr 16 2019 Christian Lindig <christian.lindig@citrix.com> - 1.166.0-1
- CA-314317: Protect PVS-cache get_or_recreate_vdi by mutex
- Zstd export: Implement Zstd option for disk export
- Zstd export: Add some helper functions
- Zstd export: Allow specifying zstd export on the CLI
- Zstd export: On VM import, autodetect whether gzip or zstd
  has been used to compress the image
- Zstd export: Add feature flag for zstd export
- Add zstd dependency to xapi.opam
- Zstd export: fall back to gzip in all non-zstd cases, not just
  if the gzip magic string is present

* Tue Apr 09 2019 Christian Lindig <christian.lindig@citrix.com> - 1.165.0-1
- CA-314290: Allow to specify SMBIOS type2 info from the toolstack
- CA-312226 XSI-251 add logging for vGPU meta data updates
- CA-312226 XSI-251 clear unexpected vGPU metadata on shutdown

* Wed Apr 03 2019 Christian Lindig <christian.lindig@citrix.com> - 1.164.0-1
- Change release name from oslo to plymouth

* Thu Mar 28 2019 Christian Lindig <christian.lindig@citrix.com> - 1.163.0-1
- Revert "Add zstd dependency to xapi.opam"
- Revert "Zstd export: Add feature flag for zstd export"
- Revert "Zstd export: On VM import, autodetect whether gzip or zstd has been used to compress the image"
- Revert "Zstd export: Allow specifying zstd export on the CLI"
- Revert "Zstd export: Add some helper functions"
- Revert "Zstd export: Implement Zstd option for disk export"

* Tue Mar 26 2019 Christian Lindig <christian.lindig@citrix.com> - 1.162.0-1
- CA-310173: remember multipath status with static vdi data

* Wed Mar 20 2019 Christian Lindig <christian.lindig@citrix.com> - 1.161.0-1
- XSI-132 CA-312644 CA-299554 update dom0 vcpu count
- Zstd export: Implement Zstd option for disk export
- Zstd export: Add some helper functions
- Zstd export: Allow specifying zstd export on the CLI
- Zstd export: On VM import, autodetect whether gzip or zstd has been used to compress the image
- Zstd export: Add feature flag for zstd export
- Add zstd dependency to xapi.opam
- maintenance: prepare xapi globs for more metrics types
- maintenance: try to make the flow clearer on monitor_pvs_proxy
- maintenance: avoid using open on monitor_pvs_proxy
- maintenance: move find_rrd_files where it can be common
- maintenance: move ignored_errors cache to db_calls_cache
- maintenance: move datasource loading to a function
- CP-30614: Use rrd files to gather memory statistics

* Thu Mar 14 2019 Christian Lindig <christian.lindig@citrix.com> - 1.160.0-1
- CA-311705: Add VDI usage checking for metadata backup scripts.

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
