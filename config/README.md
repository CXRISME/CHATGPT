# Configuration

This directory contains an environment example and will hold validated SLAM parameters. `robot.env.example` is not loaded automatically: copy it to `robot.env`, review it, then source it in each terminal.

| Setting | Meaning and verification |
| --- | --- |
| `TURTLEBOT3_MODEL=burger` | Robot model; must match the physical hardware |
| `ROS_DOMAIN_ID=30` | ROS2 communication domain; 30 is an example. Match both machines and avoid other lab robots |
| `ROS_LOCALHOST_ONLY=0` | Allows discovery beyond the local machine; also check the network, firewall and middleware |
| `use_sim_time` | Use `false` on real hardware and `true` for simulation or replay with `/clock`; keep related nodes consistent |
| `slam_params_file` | Absolute path to a complete SLAM Toolbox YAML parameter file |

The bringup package defaults to `mapper_params_online_async.yaml` from the **installed version** of SLAM Toolbox, avoiding a copied configuration from a mismatched release. The upstream Humble configuration commonly uses `map`, `odom`, `base_footprint` and `/scan`; confirm these against the actual TF tree and topics.

## Capture the First Baseline

From the repository root, in a terminal with the ROS2 environment loaded:

```bash
cp "$(ros2 pkg prefix --share slam_toolbox)/config/mapper_params_online_async.yaml" config/slam_baseline.yaml
```

Review `mode: mapping`, `scan_topic`, `base_frame`, `odom_frame` and `map_frame` under `slam_toolbox.ros__parameters`. Set laser range limits according to the actual sensor. Keep the complete file, including solver parameters. Launch with:

```bash
ros2 launch maze_slam_bringup mapping.launch.py use_sim_time:=false slam_params_file:="$PWD/config/slam_baseline.yaml"
```

Record the source version using `dpkg-query -W ros-humble-slam-toolbox`, commit the YAML and include the commit SHA in the experiment record. Use `ros2 param dump /slam_toolbox` to inspect runtime parameters and compare them with the file; the launch argument selects the clock source.

Establish a baseline before changing one variable at a time, such as map resolution, minimum travel distance or loop closure thresholds. Record the previous value, new value, reason and outcome. Upstream defaults are not evidence of optimisation.

## TF and Time

- Robot drivers provide `odom → base_footprint`; the robot description provides transforms to the laser frame. SLAM provides `map → odom`.
- Confirm the actual base and laser frames using `/scan.header.frame_id` and the TF tree. Resolve missing driver transforms rather than masking them with arbitrary static transforms.
- When using Adaptive Monte Carlo Localisation (AMCL) later, AMCL provides `map → odom`. Stop mapping SLAM to avoid competing transform publishers.
- Synchronise system clocks on the real PC and Raspberry Pi. Simulation and replay require a valid `/clock` source.

Upstream launch and configuration reference: [SLAM Toolbox Humble](https://github.com/SteveMacenski/slam_toolbox/tree/humble).
