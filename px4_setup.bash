#!/usr/bin/env bash

export GZ_SIM_RESOURCE_PATH=$(pwd)/models:$(pwd)/worlds
export PX4_GZ_WORLD="safmc_d2"

git submodule update --init --recursive

# Setup PX4
if [[ ! -e /tmp/.px4.setup ]]; then
    bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
    touch /tmp/.px4.setup
fi

# Regenerate a new world (or not)
read -rp "Regenerate safmc_d2 world? [y/N]: " user_input
if [[ "${user_input,,}" == "y" ]]; then
    echo "Regenerating the world..."

    # 檢查 Python
    if command -v python3 &>/dev/null; then
        python_exec="python3"
    elif command -v python &>/dev/null; then
        python_exec="python"
    else
        echo "Error: Python not found."
        exit 1
    fi

    # Generate a new world
    if ! SDF_PATH="$(pwd)/models" "$python_exec" utils/generate_world.py; then
        echo "Error: Python script execution failed."
        exit 1
    fi

    echo "World regenerated."
else
    echo "Skipped."
fi

# Copy safmc_d2 world file
echo "Copying world file..."
cp ./worlds/safmc_d2.sdf ./PX4-Autopilot/Tools/simulation/gz/worlds

# Copy configuration files
find "./PX4-Autopilot.config" -type f | while read -r file; do
    relative_path="${file#./PX4-Autopilot.config/}"
    mkdir -p "./PX4-Autopilot/$(dirname "$relative_path")"
    cp "$file" "./PX4-Autopilot/$relative_path"
done

# Build PX4 SITL
if [[ ! -e /tmp/.px4.build ]]; then
    cd PX4-Autopilot
    make px4_sitl
    cd ..
    touch /tmp/.px4.build
fi

# Gazebo System (Plugin)
export GZ_SIM_SYSTEM_PLUGIN_PATH=/workspace/safmc-d2-gazebo/build/payload_system:/workspace/safmc-d2-gazebo/build/position_system
source /workspace/safmc-d2-gazebo/install/setup.bash
