# SAFME D2

![Screenshot](docs/Screenshot%20from%202024-12-06%2001-12-12.png)

## RUN

> [!IMPORTANT]  
> There is an issue with the `requirements.txt` file in `PX4-Autopilot/safmc-d2-gazebo/PX4-Autopilot/Tools/setup`.
> Manually change line 11 from `matplotlib>=3.0.*` to `matplotlib>=3.0`. This will be fixed in PX4-Autopilot version 1.16.

```sh
chmod +x px4_setup.sh run.sh
. ./px4_setup.sh

./run.sh
```

## TODO

- [ ] random bonus zone entrance
