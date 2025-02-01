#!/usr/bin/env bash

# ref: https://docs.px4.io/main/en/sim_gazebo_gz

set -e
cd PX4-Autopilot

PID_FILE="/tmp/.px4.pid"

stop_px4() {
    echo "Stopping all PX4 instances..."
    for pid_file in /tmp/.px4.pid.*; do
        if [[ -f "$pid_file" ]]; then
            pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null
                echo "PX4 instance with PID $pid stopped."
                rm -f "$pid_file"
            else
                echo "PX4 instance with PID $pid is already stopped."
                rm -f "$pid_file"
            fi
        fi
    done

    echo "Stopping Gazebo simulation processes..."
    for pid in $(pgrep -f "gz sim"); do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null
            echo "Gazebo simulation process with PID $pid stopped."
        fi
    done

    echo "All PX4 instances stopped."
}

start_px4() {
    local index="$1"
    local foreground="$2"
    local target_pid_file="$PID_FILE.$index"

    if [[ -f "$target_pid_file" ]]; then
        echo "PX4 instance with index $index is already running. Use 'stop' to stop it first."
        exit 1
    fi

    if [[ "$foreground" == "true" ]]; then
        PX4_SYS_AUTOSTART=4012 PX4_SIM_MODEL=gz_x500_safmc_d2 PX4_GZ_MODEL_POSE="0,-$((10 - index)),0,0,0,0" ./build/px4_sitl_default/bin/px4 -i "$index"
        echo $! > "$target_pid_file"
        echo "Started PX4 instance with index $index in the foreground."
    else
        PX4_SYS_AUTOSTART=4012 PX4_SIM_MODEL=gz_x500_safmc_d2 PX4_GZ_MODEL_POSE="0,-$((10 - index)),0,0,0,0" ./build/px4_sitl_default/bin/px4 -i "$index" > /dev/null &
        echo $! > "$target_pid_file"
        echo "Started PX4 instance with index $index in the background."
    fi
}

case "$1" in
    start)
        if [[ -z "$2" ]]; then
            echo "Usage: $0 start <index> [--foreground|-f]"
            exit 1
        fi
        
        foreground="false"
        if [[ "$3" == "--foreground" || "$3" == "-f" ]]; then
            foreground="true"
        fi

        start_px4 "$2" "$foreground"
        ;;
    stop)
        stop_px4
        ;;
    *)
        echo "Usage: $0 {start <index> [--foreground|-f] | stop}"
        exit 1
        ;;
esac
