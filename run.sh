#!/usr/bin/sh

set -e

# Run PX4 Autopilot
cd PX4-Autopilot
PX4_GZ_MODEL_POSE="0,-9,0,0,0,0" make px4_sitl gz_x500_safmc_d2
