# SAFMC D2 Description

Gazebo simulation environment for the SAFMC D2 competition, [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot/tree/release/1.15) integration as a submodule.

![Screenshot](docs/Screenshot%20from%202025-01-28%2014-22-15.png)

## RUN

> [!IMPORTANT]  
> There is an issue with the `requirements.txt` file in `PX4-Autopilot/safmc-d2-gazebo/PX4-Autopilot/Tools/setup`.
> Manually change line 11 from `matplotlib>=3.0.*` to `matplotlib>=3.0`. This will be fixed in PX4-Autopilot version 1.16.

```sh
pip install symforce

rm /tmp/.px4.setup
rm /tmp/.px4.build

chmod +x px4_setup.bash run.bash

source ./px4_setup.bash

./run.bash start 1
./run.bash start 2
./run.bash start 3
./run.bash start 4

./run.bash stop
```

## ROS2 Bridge

```bash
# ref: https://github.com/gazebosim/ros_gz/blob/ros2/ros_gz_bridge/README.md

# single drone
ros2 run ros_gz_bridge parameter_bridge \
/world/safmc_d2/model/x500_safmc_d2_1/link/lidar_2d_link/sensor/lidar_2d_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan \
/world/safmc_d2/model/x500_safmc_d2_1/link/lidar_2d_link/sensor/lidar_2d_sensor/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked \
/world/safmc_d2/model/x500_safmc_d2_1/link/pi3_cam_link/sensor/pi3_cam_sensor/image@sensor_msgs/msg/Image[gz.msgs.Image \
/world/safmc_d2/model/x500_safmc_d2_1/link/pi3_cam_link/sensor/pi3_cam_sensor/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo

# 4 drones (i = 1 ~ 4)
ros2 run ros_gz_bridge parameter_bridge \
/world/safmc_d2/model/x500_safmc_d2_1/link/lidar_2d_link/sensor/lidar_2d_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan \
/world/safmc_d2/model/x500_safmc_d2_1/link/lidar_2d_link/sensor/lidar_2d_sensor/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked \
/world/safmc_d2/model/x500_safmc_d2_1/link/pi3_cam_link/sensor/pi3_cam_sensor/image@sensor_msgs/msg/Image[gz.msgs.Image \
/world/safmc_d2/model/x500_safmc_d2_1/link/pi3_cam_link/sensor/pi3_cam_sensor/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo \
/world/safmc_d2/model/x500_safmc_d2_2/link/lidar_2d_link/sensor/lidar_2d_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan \
/world/safmc_d2/model/x500_safmc_d2_2/link/lidar_2d_link/sensor/lidar_2d_sensor/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked \
/world/safmc_d2/model/x500_safmc_d2_2/link/pi3_cam_link/sensor/pi3_cam_sensor/image@sensor_msgs/msg/Image[gz.msgs.Image \
/world/safmc_d2/model/x500_safmc_d2_2/link/pi3_cam_link/sensor/pi3_cam_sensor/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo \
/world/safmc_d2/model/x500_safmc_d2_3/link/lidar_2d_link/sensor/lidar_2d_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan \
/world/safmc_d2/model/x500_safmc_d2_3/link/lidar_2d_link/sensor/lidar_2d_sensor/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked \
/world/safmc_d2/model/x500_safmc_d2_3/link/pi3_cam_link/sensor/pi3_cam_sensor/image@sensor_msgs/msg/Image[gz.msgs.Image \
/world/safmc_d2/model/x500_safmc_d2_3/link/pi3_cam_link/sensor/pi3_cam_sensor/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo \
/world/safmc_d2/model/x500_safmc_d2_4/link/lidar_2d_link/sensor/lidar_2d_sensor/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan \
/world/safmc_d2/model/x500_safmc_d2_4/link/lidar_2d_link/sensor/lidar_2d_sensor/scan/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked \
/world/safmc_d2/model/x500_safmc_d2_4/link/pi3_cam_link/sensor/pi3_cam_sensor/image@sensor_msgs/msg/Image[gz.msgs.Image \
/world/safmc_d2/model/x500_safmc_d2_4/link/pi3_cam_link/sensor/pi3_cam_sensor/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo \
```
