# SAFME D2 Description

Gazebo simulation environment for the SAFMC drone competition, [PX4-Autopilot](https://github.com/PX4/PX4-Autopilot/tree/release/1.15) integration as a submodule.

![Screenshot](docs/Screenshot%20from%202025-01-28%2014-22-15.png)

## RUN

> [!IMPORTANT]  
> There is an issue with the `requirements.txt` file in `PX4-Autopilot/safmc-d2-gazebo/PX4-Autopilot/Tools/setup`.
> Manually change line 11 from `matplotlib>=3.0.*` to `matplotlib>=3.0`. This will be fixed in PX4-Autopilot version 1.16.

```sh
rm /tmp/.px4.setup

chmod +x px4_setup.sh run.sh
. ./px4_setup.sh

./run.sh
```
