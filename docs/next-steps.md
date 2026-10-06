# Development Roadmap

These are pending tasks, not completed results. The current repository provides a scaffold and a launch wrapper. Follow the prerequisites in order:

| Stage | Next concrete task | Acceptance evidence |
| --- | --- | --- |
| 0: Environment | Confirm PC/Pi systems, LiDAR, drivers, communication domain and TF | Experiment record plus `/scan`, `/odom` and TF outputs |
| 1: Mapping | Map using the existing drivers and this package; capture the first SLAM parameter file | Loadable YAML/image pair, recording index and RViz screenshots |
| 2: Map quality | Repeat the baseline with a fixed maze and route; change one parameter at a time | Measured versus mapped wall distances, before/after loop closure images, all successful and failed runs |
| 3: Localisation | Install matching Nav2 packages, stop mapping SLAM, and integrate the map server and AMCL | Pose updates during movement after initialisation at a known start, with a single `map → odom` publisher |
| 4: Navigation | Add `navigation.launch.py` and verified Nav2 parameters; configure robot footprint, speed and obstacle layers | A feasible route between specified start/goal positions and actual arrival; record failures and collisions |
| 5: FYP analysis | Repeat navigation experiments under fixed conditions and summarise mapping/localisation/navigation metrics | A report linked to code SHAs, maps, parameters and data |

## Where to Extend the Code

- Current entry point: `src/maze_slam_bringup/launch/mapping.launch.py`. It wraps the upstream SLAM launch file without changing the SLAM algorithm.
- First parameter baseline: follow `config/README.md` to create a complete `config/slam_baseline.yaml`.
- Future navigation configuration can live in `src/maze_slam_bringup/config/`. Add installation rules for that directory to `CMakeLists.txt` and declare the actual dependencies in `package.xml` when introducing it.
- If custom experiment acquisition nodes are needed, create a separate ROS2 package under `src/` to keep bringup separate from algorithms and data collection.
- Define inputs, expected outputs and acceptance criteria before each development step, then record the observed results. Mark items without physical evidence as unverified.

## Defining Metrics

Start map error measurements with fixed wall segment lengths, stating the method, units and errors. Localisation error requires an independent reference position; odometry is not ground truth. Without reference positioning equipment, report qualitative observations or comparisons at known measured points and state the limitation.

Navigation success rate is the number of attempts meeting predefined arrival criteria divided by all attempts. Define position tolerances, time limits and collision criteria in advance. Also record elapsed time, path length and failure reasons. Choose repetition counts and thresholds before experiments, and retain failed runs.

Autonomous exploration of an unknown maze is an additional feature requiring a strategy such as frontier exploration. The initial scope is manual mapping followed by navigation in a known map; neither stage demonstrates autonomous exploration by itself.
