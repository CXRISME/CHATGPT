# Environment and First Run

This guide uses Ubuntu 22.04 / ROS2 Humble as a provisional baseline. It has not been validated on the user's physical robot. If the existing image uses another distribution, record the actual environment and follow the matching official documentation. Avoid mixing ROS2 distributions.

## 1. Record the Existing Environment

Run these commands on both the PC and Raspberry Pi and include the outputs in the experiment record:

```bash
cat /etc/os-release
uname -m
printenv ROS_DISTRO
printenv RMW_IMPLEMENTATION
printenv ROS_DOMAIN_ID
```

An empty `RMW_IMPLEMENTATION` means the middleware has not been explicitly selected; record the implementation actually used. Also record the Raspberry Pi model, LiDAR model, OpenCR firmware version when available, battery condition and connection method. These measured details are not yet available in this repository.

## 2. PC Dependencies and Build

Prerequisite: ROS2 Humble is installed following the official guide and its package repositories are configured. Run these commands only in a matching Ubuntu/ROS2 environment. Preserve the robot's existing image.

```bash
sudo apt update
sudo apt install ros-humble-slam-toolbox ros-humble-nav2-map-server ros-humble-tf2-ros ros-humble-rosbag2 ros-humble-rviz2 python3-colcon-common-extensions python3-rosdep
source /opt/ros/humble/setup.bash
```

Clone the repository if you do not already have a checkout; otherwise enter the existing directory:

```bash
git clone https://github.com/CXRISME/CHATGPT.git
cd CHATGPT
```

From the repository root:

```bash
cp config/robot.env.example config/robot.env
# Edit robot.env and confirm the model and lab communication domain before sourcing.
source config/robot.env
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select maze_slam_bringup
source install/setup.bash
ros2 launch maze_slam_bringup mapping.launch.py --show-args
```

If `rosdep update` reports that rosdep has not been initialised, run `sudo rosdep init` once first. Source the ROS2, workspace and environment files again in every new terminal. Navigation dependencies will be installed in a later stage; this stage only needs the map-saving tool.

## 3. Raspberry Pi Drivers and Communication

Follow the **Humble** section of the ROBOTIS manual to configure Raspberry Pi drivers, LiDAR and OpenCR. Use compatible ROS2 environments and the same communication domain on both machines. Check network communication and clock synchronisation. You can set the example environment variables manually on both machines; building this project on the Raspberry Pi is not required.

If the hardware is a standard TurtleBot3 Burger and its drivers are installed, run this in a Raspberry Pi terminal:

```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger
# Confirm ROS_DOMAIN_ID / ROS_LOCALHOST_ONLY match the PC settings.
ros2 launch turtlebot3_bringup robot.launch.py
```

If the lab already has a bringup procedure, confirm its interfaces first. Run only one set of base drivers.

In another PC terminal with the environment loaded, check the interfaces without sending motion commands:

```bash
ros2 node list
ros2 topic list -t
ros2 topic info /scan --verbose
ros2 topic echo /scan --once
ros2 topic hz /scan
ros2 topic echo /odom --once
ros2 run tf2_ros tf2_echo odom base_footprint
```

`topic hz` and `tf2_echo` run continuously; stop each with Ctrl+C before proceeding. Record the scan frequency, laser frame ID and timestamps. Then check TF from `base_footprint` to the actual laser frame ID. If topics or frames differ, update the documentation and configuration first. A Quality of Service (QoS) mismatch can prevent reception even when a topic is visible; compare publisher and subscriber settings.

**Acceptance criteria:** continuous scans and odometry, a connected TF chain, and no persistent timestamp or transform errors. Resolve failures before tuning SLAM.

## 4. First Mapping Run on the Physical Robot

Keep the robot drivers running and launch this on the PC:

```bash
ros2 launch maze_slam_bringup mapping.launch.py use_sim_time:=false
```

Run `rviz2` in another terminal. Set the Fixed Frame to `map` and add Map, LaserScan and TF displays. Subscribe the Map display to `/map`; set Durability to `Transient Local` if needed.

First observe the map and scans while stationary. Once the risk assessment is approved, movement is permitted on site and the stopping procedure is confirmed, use teleoperation compatible with the installed driver to move slowly. This scaffold does not move the robot automatically. Pass recognisable corners and return to the starting point to inspect the map after loop closure.

You can begin recording before launching mapping; use a new output directory for each run:

```bash
ros2 bag record -o bags/YYYYMMDD_maze01_run01 /scan /odom /tf /tf_static
```

Stop recording with Ctrl+C. Run `ros2 bag info bags/YYYYMMDD_maze01_run01` to check message counts, the time range and whether static TF was recorded. A recording directory alone does not prove valid data. For simulation, also pass `--use-sim-time` and record `/clock`. Replay in a separate session with physical drivers and other clock sources stopped: use `ros2 bag play <bag_path> --clock` and launch SLAM with `use_sim_time:=true`. Confirm the recording contains the required TF first.

Once a map is available, save it from another terminal at the repository root:

```bash
ros2 run nav2_map_server map_saver_cli -f "$PWD/maps/YYYYMMDD_maze01_run01"
```

Verify the YAML and image form a valid pair, the image path resolves, and walls and passages are represented. Record success only after actually saving and checking the files. Copy `experiments/TEMPLATE.md` into a new experiment record and fill in commands, parameter versions, evidence and failure reasons.

## Official References

- [ROS2 Humble installation](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
- [TurtleBot3 bringup: select Humble](https://emanual.robotis.com/docs/en/platform/turtlebot3/bringup/)
- [SLAM Toolbox Humble launch entry point](https://github.com/SteveMacenski/slam_toolbox/blob/humble/launch/online_async_launch.py)
- [rosbag2](https://github.com/ros2/rosbag2/tree/humble)
- [Nav2 mapping and map saving](https://docs.nav2.org/tutorials/docs/navigation2_with_slam.html)
