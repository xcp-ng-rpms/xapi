#!/usr/bin/env bash
# Delete all OVS bridges on the first start of openvswitch after boot.
#
# At startup, xcp-networkd skips bridges that already exist in OVS, so their
# config is not re-applied from networkd.db. Deleting them lets networkd
# recreate and configure them, as on XCP-ng 8.3. The marker in /run (tmpfs)
# limits this to once per boot, so restarting openvswitch on a running host is
# safe.

# The bridges are created by xcp-networkd, from its own state in networkd.db.
# OVS also stores them in its database (/etc/openvswitch/conf.db), which
# persists across reboots: at boot, ovsdb-server will load them and ovs-vswitchd
# recreates those bridges before xcp-networkd starts.
#
# At startup, xcp-networkd skips bridges that already exist in OVS, so the
# configuration from networkd.db (ports, bonds, MAC, other_config) is not
# re-applied to them. On XCP-ng 8.3, the bridges did not exist yet when
# xcp-networkd started, so they were always recreated. Deleting them here
# restores that behaviour.
#
# The marker in /run (tmpfs) limits this to once per boot, so restarting
# openvswitch on a running host does not remove the bridges.

set -euo pipefail
set -x

marker=/run/openvswitch-bridges-cleared

[ -e "$marker" ] && exit 0
# Create the marker first: a failed attempt must not be retried on a running host.
touch "$marker"

ovs-vsctl --no-wait list-br | xargs -r -n1 ovs-vsctl --no-wait del-br
