#!/usr/bin/sh

set -e

# Run PX4 Autopilot
cd PX4-Autopilot
make px4_sitl gz_x500_safmc_d2 -j"$(nproc)"
