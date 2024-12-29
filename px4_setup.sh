#!/usr/bin/sh

export GZ_SIM_RESOURCE_PATH="$(pwd)/PX4-Autopilot/Tools/simulation/gz"
export PX4_GZ_WORLD="safmc_d2"

git submodule update --init --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh

CMAKELIST_FILE="PX4-Autopilot/src/modules/simulation/gz_bridge/CMakeLists.txt"

if grep -q "$PX4_GZ_WORLD" "$CMAKELIST_FILE"; then
    echo "$PX4_GZ_WORLD already exists in $CMAKELIST_FILE."
else
    # Insert safmc_d2 in the set(gz_worlds ...) block
    sed -i "/set(gz_worlds/a \ \ \ \ $PX4_GZ_WORLD" "$CMAKELIST_FILE"
    echo "$PX4_GZ_WORLD has been added to $CMAKELIST_FILE."
fi
