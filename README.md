# CHATGPT

## Minimal ROS2 SLAM / FYP Project Scaffold

Goal: use a Raspberry Pi-based TurtleBot3 Burger to scan a real maze, perform Simultaneous Localisation and Mapping (SLAM), then localise within the saved map and plan and execute routes.

**Current status: project scaffold.** Documentation, an experiment template and a SLAM launch entry point are provided. Mapping, localisation and navigation have not been validated on the physical robot. Navigation is a later stage; successful mapping alone does not demonstrate autonomous navigation or autonomous exploration.

Provisional reproduction baseline: Ubuntu 22.04 + ROS2 Humble, with the Burger model. The actual PC and Raspberry Pi operating systems, LiDAR model, firmware and topic names still need checking. Keep the existing device installations until their compatibility is confirmed.

### File Guide

| Path | Purpose |
| --- | --- |
| [docs/setup.md](docs/setup.md) | Environment checks, dependencies, build, connectivity and first mapping run |
| [config/README.md](config/README.md) | Configuration, clock sources, coordinate frames and parameter records |
| [config/robot.env.example](config/robot.env.example) | Example environment variables without addresses or credentials |
| [src/maze_slam_bringup](src/maze_slam_bringup) | Custom ROS2 bringup package |
| [experiments/TEMPLATE.md](experiments/TEMPLATE.md) | Reproducible experiment record template |
| [maps/README.md](maps/README.md) | Map file naming and version conventions |
| [bags/README.md](bags/README.md) | rosbag2 recording conventions |
| [docs/next-steps.md](docs/next-steps.md) | Development stages and acceptance criteria |

### Getting Started

1. Follow the [setup guide](docs/setup.md) to confirm both systems, ROS2 versions and LiDAR. First check `/scan`, odometry and coordinate transforms (TF).
2. Install dependencies and build this repository with `colcon`. The repository root can serve as the workspace root.
3. With the robot drivers running and TF working, run the following on the PC:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
source config/robot.env
ros2 launch maze_slam_bringup mapping.launch.py use_sim_time:=false
```

Create and review `robot.env` from the example first, as described in the setup guide. This entry point runs SLAM Toolbox only. Robot drivers, motion commands and Nav2 are outside this launch file.

4. Copy the experiment template, record the first run, and save the map and evidence. The following stages are map-based localisation, path planning and autonomous navigation.

### Contribution Conventions

- Each commit should describe one clear change. Experiment records must identify the code commit SHA, parameter files and data sources.
- `build/`, `install/`, `log/`, local environment files and raw recordings are excluded by default. Small maps may be committed; record the location, size and checksum of large files instead.
- Use branches and pull requests (PRs) to review changes. Preserve failed experiments and their explanations.
- The original README heading and commit history are preserved. The project licence has not been selected; replace the `TODO` in `package.xml` before granting reuse rights.
