#!/bin/sh

case "$1" in
    0)
        # tear-down
        systemctl disable --now varstored-guard
        ;;
    1)
        # set-up
        systemctl enable --now varstored-guard
        ;;
    *)
        exit 0
esac
