#!/usr/bin/env bash
# Delete all OVS bridges on the first start of openvswitch after boot.
#
# At startup, xcp-networkd skips bridges that already exist in OVS, so their
# config is not re-applied from networkd.db. Deleting them lets networkd
# recreate them, as on XCP-ng 8.3. The marker in /run (tmpfs) limits this to
# once per boot, so restarting openvswitch on a running host is safe.
set -euo pipefail
set -x

marker=/run/openvswitch-bridges-cleared

[ -e "$marker" ] && exit 0
# Create the marker first: a failed attempt must not be retried on a running host.
touch "$marker"

ovs-vsctl --no-wait list-br | xargs -r -n1 ovs-vsctl --no-wait del-br
