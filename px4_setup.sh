#!/usr/bin/sh
git submodule update --init --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh

cp -r ./models/* ./PX4-Autopilot/Tools/simulation/gz/models
cp ./worlds/safmc_d2.sdf ./PX4-Autopilot/Tools/simulation/gz/worlds

CMAKELIST_FILE="PX4-Autopilot/src/modules/simulation/gz_bridge/CMakeLists.txt"
WORLD_NAME="safmc_d2"

if grep -q "$WORLD_NAME" "$CMAKELIST_FILE"; then
  echo "$WORLD_NAME already exists in $CMAKELIST_FILE."
else
  # Insert safmc_d2 in the set(gz_worlds ...) block
  sed -i "/set(gz_worlds/a \ \ \ \ $WORLD_NAME" "$CMAKELIST_FILE"
  echo "$WORLD_NAME has been added to $CMAKELIST_FILE."
fi

#add this to access model and world created by us
export GZ_SIM_RESOURCE_PATH="$HOME/safmc-d2-gazebo/PX4-Autopilot/Tools/simulation/gz"


