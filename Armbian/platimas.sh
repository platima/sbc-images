#!/bin/bash

if [ ! -f "compile.sh" ]; then 
    echo  "Could not find compile.sh - please make sure you're in the Armbian 'build' folder"
    exit 1
fi

RELEASES=("bookworm" "sid")
BOARDS=("radxa-zero3" "rock-3a")
BRANCHES=("vendor" "legacy")

PACKAGES="libglx-mesa0
libgl1-mesa-dri
mesa-utils
mesa-utils-extra
vlc
glmark2-x11
net-tools
screen
vim
neofetch
chromium"

for RELEASE in ${RELEASES[@]}; do
    PACKAGES_FILE="config/desktop/$RELEASE/appgroups/platimas/packages"
    if [ ! -f $PACKAGES_FILE ]; then
        echo $PACKAGES > $PACKAGES_FILE
    fi

    for BOARD in ${BOARDS[@]}; do
        for BRANCH in ${BRANCHES[@]}; do
            ./compile.sh build BOARD=$BOARD BRANCH=$BRANCH BUILD_DESKTOP=yes BUILD_MINIMAL=no DESKTOP_APPGROUPS_SELECTED=platimas DESKTOP_ENVIRONMENT=xfce DESKTOP_ENVIRONMENT_CONFIG_NAME=config_base KERNEL_CONFIGURE=no RELEASE=$RELEASE
        done
    done
done