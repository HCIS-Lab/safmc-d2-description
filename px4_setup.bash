#!/usr/bin/env bash
# set -e

export GZ_SIM_RESOURCE_PATH=$(pwd)/models:$(pwd)/worlds
export PX4_GZ_WORLD="safmc_d2"

git submodule update --init --recursive

if [ ! -e /tmp/.px4.setup ]; then
    bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
    touch /tmp/.px4.setup
fi

read -p "Regenerate safmc_d2 world? [y/N]: " user_input
if echo "$user_input" | grep -iq "^y"; then
    echo "Regenerating the world..."

    if command -v python3 >/dev/null; then
        SDF_PATH="$(pwd)/models" python3 utils/generate_world.py
    elif command -v python >/dev/null; then
        SDF_PATH="$(pwd)/models" python utils/generate_world.py
    else
        echo "Error: Python not found."
        return 1
    fi

    if [ $? -ne 0 ]; then
        echo "Error: Python script execution failed."
        return 1
    fi

    echo "World regenerated."
else
    echo "Skipped."
fi

echo "Copying world file..."
cp ./worlds/safmc_d2.sdf ./PX4-Autopilot/Tools/simulation/gz/worlds

find "./PX4-Autopilot.config" -type f | while read -r file; do
    relative_path="${file#./PX4-Autopilot.config/}"
    mkdir -p "./PX4-Autopilot/$(dirname "$relative_path")"
    cp "$file" "./PX4-Autopilot/$relative_path"
done

if [ ! -e /tmp/.px4.build ]; then
    cd PX4-Autopilot
    make px4_sitl
    touch /tmp/.px4.build
fi
