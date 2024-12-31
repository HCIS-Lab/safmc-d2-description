#!/usr/bin/sh

read -p "Regenerate safmc_d2 world? [y/N]: " user_input

if echo "$user_input" | grep -iq "^y"; then
    echo "Regenerating the world..."

    # Check for Python (either python3 or python) and run the script
    if command -v python3 >/dev/null; then
        SDF_PATH="$(pwd)/models" python3 utils/generate_world.py
    elif command -v python >/dev/null; then
        SDF_PATH="$(pwd)/models" python utils/generate_world.py
    else
        echo "Error: Python not found."
        exit 1
    fi

    if [ $? -ne 0 ]; then
        echo "Error: Python script execution failed."
        exit 1
    fi

    echo "World regenerated."
else
    echo "Skipped."
fi

# Copy models and world files to the appropriate directories
echo "Copying models and world files..."
cp ./worlds/safmc_d2.sdf ./PX4-Autopilot/Tools/simulation/gz/worlds

# Run PX4 Autopilot
cd PX4-Autopilot
make px4_sitl gz_x500
