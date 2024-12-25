#!/bin/bash
cd ~/safmc-d2-gazebo

read -p "Do you want to regenerate safmc_d2 world? (yes/no): " user_input

if [[ "$user_input" == "yes" || "$user_input" == "y" ]]; then

    echo "Regenerating the world..."

    if command -v python &>/dev/null; then
        python ./main.py
    elif command -v python3 &>/dev/null; then
        python3 ./main.py
    else
        echo "python not installed"
        exit 1
    fi

    chmod +x px4_setup.sh
    ./px4_setup.sh || { 
        echo "Error: Failed to run ./setup_px4."; 
        exit 1; 
    }

    echo "World regeneration completed."
else
    echo "World regeneration skipped."
fi

cd PX4-Autopilot
PX4_GZ_WORLD=safmc_d2 make px4_sitl gz_x500