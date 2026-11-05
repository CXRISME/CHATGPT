# Experiment Record: 2026-11-05 — ROS 2 SLAM and Nav2 Development

Project: **TurtleBot3 Burger — ROS 2 SLAM and Autonomous Navigation**.
Date: **5 November 2026**. This is a development checkpoint, not a formal
navigation-performance trial.

This entry follows the structure of `experiments/TEMPLATE.md` on the existing
`scaffold/ros2-slam-fyp` branch. The scaffold is not merged by this update.
Today's implementation steps, observations and measurements below are recorded
from the owner's supplied progress report. The documentation update did not
rerun the experiments or inspect the Ubuntu VM's saved artifacts. No screenshots,
map files or trial CSV files were found in the inspected `main` tree or local
repository working tree. Proposed evidence is indexed below without implying
that it has been supplied.

## Objective and Hypothesis

- Prepare the Raspberry Pi and robot power supply for later physical testing.
- Establish a ROS 2 Humble workstation in VirtualBox and verify simulated robot
  spawning, sensor topics and keyboard teleoperation.
- Generate and save a Cartographer occupancy grid, then demonstrate an initial
  Nav2 goal using AMCL localisation.
- Investigate Gazebo-world versus ROS-map coordinate alignment before measuring
  navigation accuracy.
- Formal acceptance criterion for the later evaluation: at least **8 of at least
  10 navigation trials** must complete without collision or manual intervention
  and with final-position error **within 0.2 m**. The 10-trial evaluation has
  **not been performed**; this entry establishes no formal pass rate.

The possible explanation that the robot was still rotating during a heading
measurement is an **unverified hypothesis**, not a confirmed cause.

## Environment and Versions

| Item | Reported details / verification limits |
| --- | --- |
| Workstation | Ubuntu 22.04.5 LTS in Oracle VirtualBox; earlier handoff identifies the guest as x86_64 |
| ROS distribution | ROS 2 Humble Desktop; official ROS 2 APT repository added; `ROS_DISTRO=humble` and the `ros2` CLI verified in the reported session |
| Simulation and visualisation | Gazebo Classic, official TurtleBot3 World, RViz2; exact package versions not supplied |
| Robot model | TurtleBot3 Burger; `TURTLEBOT3_MODEL=burger` |
| SLAM and navigation software | TurtleBot3 packages and Gazebo integration, Cartographer, SLAM Toolbox and Navigation2 installed; Cartographer used for today's mapping, AMCL for localisation |
| Workspace | `~/fyp_slam_ws/src` created in the Ubuntu VM |
| Raspberry Pi / hardware | Physical TurtleBot3 Burger and Raspberry Pi; the October setup log identifies a Raspberry Pi 4 Model B and Ubuntu 22.04.5 LTS ARM64; today's report concerns SD preparation, connectivity configuration and replacement-battery checks |
| Network and SSH | First-boot Wi-Fi and SSH configured; current physical-robot SSH connectivity not fully verified; VM-to-Pi access remains pending |
| Timing and configuration | TF inspection command below explicitly uses `use_sim_time:=true`; complete launch parameters, package versions, RMW, ROS domain, test timestamps and measurement windows not supplied |
| Run metadata | Experiment code revision, parameter hashes, route/start/goal coordinates, speed limits, map checksums and raw logs not supplied; no repeated-trial dataset available |

The [physical setup log](../docs/real_robot_setup.md) records successful
Windows-to-Pi SSH on 21–22 October. Today's pending connectivity check does not
invalidate that dated result or establish VM-to-Pi access. The
[Ubuntu VM handoff](../docs/ubuntu_vm_handoff.md) also retains the earlier
restricted-session audit in which ROS/Gazebo were absent from the visible
environment. Today's installation report is a later checkpoint; the October
observations remain preserved.

## Procedure and Parameters

### Physical robot and Raspberry Pi preparation

1. Prepared an Ubuntu SD card for the Raspberry Pi and configured first-boot
   Wi-Fi connectivity and SSH access.
2. Confirmed that the replacement robot battery fits and charges/discharges
   correctly, as reported by the owner. No numerical battery measurements or
   additional electrical qualification are supplied.
3. Left current physical-robot SSH verification pending. Physical LiDAR data,
   robot motion, real mapping and real navigation are not verified by today's
   simulation results.

No new Pi command transcript is supplied for this checkpoint. These preparation
notes do not imply that an additional SD-card rewrite was performed today.

### Ubuntu VM environment and simulation

1. Installed ROS 2 Humble Desktop using the official ROS 2 APT repository;
   verified the distribution and CLI, configured automatic environment sourcing
   in `.bashrc`, and installed the TurtleBot3, Gazebo, SLAM and Nav2 packages
   listed above.
2. Configured the Burger model, created `~/fyp_slam_ws/src`, and successfully ran
   the following command from the workspace root:

   ```bash
   colcon build --symlink-install
   ```

   The workspace was initially empty. This verifies the reported empty-workspace
   build command, not compilation of a populated project or evaluation node.
3. Successfully started RViz2 and loaded the official TurtleBot3 World in Gazebo.
   Initial automatic spawning failed while `/spawn_entity` was unavailable.
   Manually spawned the Burger after the service became available. This was an
   immediate recovery; an automatic startup-order fix has not been demonstrated.
4. Verified the simulated robot, differential-drive system, LiDAR visualisation,
   `/scan`, `/odom`, `/cmd_vel` and `/tf` topics, and keyboard teleoperation.
   Recorded approximate scan and odometry publishing rates in the results below.

Exact installation, launch, manual-spawn, topic-rate and teleoperation command
lines were not supplied; this record does not reconstruct them as executed
commands.

### Cartographer mapping and map saving

Launched Cartographer SLAM and generated a 2D occupancy grid of the simulated
environment. The reported visual result includes the outer walls and **nine
internal cylindrical obstacles**. This is a qualitative mapping observation;
no independent map-geometry error measurement is supplied.

Reported map files saved in the Ubuntu VM:

- `~/fyp_slam_ws/fyp_records/maps/2026-11-05_cartographer_map.pgm`
- `~/fyp_slam_ws/fyp_records/maps/2026-11-05_cartographer_map.yaml`

These are reported VM paths, not verified repository attachments. Their contents
and checksums were not available for this documentation update.

| Map parameter | Reported value |
| --- | --- |
| Resolution | 0.05 m/pixel |
| Origin | `[-3.34, -3.52, 0]` |
| Mode | `trinary` |
| Occupied threshold | 0.65 |
| Other YAML fields | Not supplied; not inferred |

### AMCL localisation and initial Nav2 goal

1. Started Navigation2 with the saved map.
2. Initialised AMCL using RViz2's `2D Pose Estimate` and checked LaserScan
   alignment against the occupancy grid.
3. Successfully executed an initial autonomous task using `Nav2 Goal` and
   verified the `/navigate_to_pose` action interface.
4. Recovered the simulation and navigation environment after a virtual machine
   shutdown without reinstalling software or rebuilding the map.

This is an initial functional demonstration of mapping, localisation, path
planning and goal navigation. No final-position error, task duration, stable
final heading or formal collision/manual-intervention trial record is supplied.

### Preliminary coordinate-frame alignment

Observed that Gazebo's `world` and ROS 2's `map` coordinate frames were rotated
relative to each other. Initial pose measurements indicated approximately
**−86.74°** from world to map. A temporary frame was established with the
reported command:

```bash
ros2 run tf2_ros static_transform_publisher \
  --x -0.474 --y -0.585 --z 0 \
  --yaw -1.514 --pitch 0 --roll 0 \
  --frame-id map \
  --child-frame-id gazebo_world_aligned
```

This publishes the pose of the child frame `gazebo_world_aligned` relative to
the parent `map`: translation `(-0.474, -0.585, 0)` m and yaw `-1.514` rad.
It is a temporary reference derived from preliminary pose measurements,
**not an independently calibrated ground-truth transformation**.

Gazebo simulator reference (ground-truth) robot poses were obtained using:

```bash
gz model -m burger -p
```

ROS pose estimates were inspected in the temporary reference frame using:

```bash
ros2 run tf2_ros tf2_echo \
  gazebo_world_aligned base_footprint \
  --ros-args -p use_sim_time:=true
```

After correcting an AMCL initial-localisation mismatch, the owner reported the
positional residuals below. Reference poses, timestamps, sampling windows and
the complete calibration/validation correspondences were not supplied, so
independent validation cannot be established.

## Observations and Results

| Observation / metric | Reported result | Interpretation and limits |
| --- | --- | --- |
| Simulated LiDAR publishing rate | Approximately **4.3 Hz** | Measured rate reported for simulation; measurement window and raw output not supplied; not a physical LiDAR result |
| Simulated odometry publishing rate | Approximately **25.7 Hz** | Measured rate reported for simulation; measurement window and raw output not supplied |
| Sensor/command/TF topics | `/scan`, `/odom`, `/cmd_vel`, `/tf` confirmed | Functional topic check; does not establish physical-robot communication |
| Keyboard teleoperation | Successful | Qualitative simulation result; no trajectory or speed dataset supplied |
| Cartographer map | Outer walls and nine internal cylinders represented | Qualitative occupancy-grid observation; map accuracy not measured |
| Initial Nav2 task | Successful task reported; `/navigate_to_pose` verified | Functional demonstration; no formal navigation accuracy or success-rate measurement |
| Preliminary alignment residual — first reported position | Approximately **0.067 m** | Coordinate-alignment residual; independently calibrated reference not available |
| Preliminary alignment residual — subsequent position | Approximately **0.052 m** | Coordinate-alignment residual; no correspondence to a proposed screenshot inferred |
| Preliminary alignment residual — another position | Approximately **0.011 m** | Coordinate-alignment residual; not a navigation goal error |
| Heading discrepancy during one navigation test | Approximately **54.7°** | Unresolved observation; robot may still have been rotating, but that explanation is unverified |
| VM shutdown recovery | Simulation/navigation restored using existing installation and saved map | Functional recovery reported; recovery command transcript not supplied |
| Formal navigation trials, durations and final-position errors | **Not performed / not measured** | No CSV, success ratio or validated 0.2 m accuracy result |

**The three positional residuals are coordinate-alignment residuals, not
independently validated navigation goal errors. They must not be used as proof
of meeting the 0.2 m final-position requirement.** Stable-state heading
verification and independent world-to-map validation remain pending.

Development outcome: **initial simulation integration successful as reported;
performance validation incomplete**. Physical-robot runtime tests remain
**Pending / To be tested**.

### Issues and resolutions

| Issue / observation | Action and reported result | Remaining limitation / lesson |
| --- | --- | --- |
| ROS installation initially missing | Installed official ROS 2 Humble and verified the distribution/CLI in the VM | A VM name alone does not establish installed software; record actual checks |
| Gazebo spawn service timeout | Waited for `/spawn_entity`, then manually spawned Burger | Startup readiness matters; automatic spawn sequencing still needs a repeatable fix |
| Missing `map → odom` transform | Initialised AMCL using RViz2's initial-pose tool | Confirm localisation and TF before issuing navigation goals |
| Ambiguous localisation around repeated obstacle geometry | Reset the AMCL initial pose; alignment improved | Repeated cylinders can make pose interpretation ambiguous; localisation reliability is not quantified |
| Gazebo-world / ROS-map coordinate mismatch | Established the temporary rigid transform and compared poses | Independent landmark validation is still required before accuracy claims |
| Virtual machine shutdown | Restored simulation and navigation without reinstalling or recreating the map | Retaining the saved map and environment allowed recovery; exact recovery steps still need recording |

## Evidence Index

All eight filenames below are **proposed evidence names**. None was present in
the inspected repository or local working tree. Captions describe intended
figures; they do not certify unseen screenshot contents. No broken image embeds
or links to missing files are included.

| Proposed figure | Proposed filename | Intended caption / evidence scope |
| --- | --- | --- |
| 1 | `2026-11-05_Burger_Spawn_Success.png` | Burger visible in TurtleBot3 World after delayed manual spawning; qualitative spawn evidence |
| 2 | `2026-11-05_LiDAR_Frequency_Test.png` | Simulated `/scan` frequency check, reported at approximately 4.3 Hz; retain the actual sampling output when supplied |
| 3 | `2026-11-05_Cartographer_SLAM_Result.png` | Cartographer occupancy grid showing outer walls and nine cylindrical obstacles; qualitative map result |
| 4 | `2026-11-05_Nav2_First_Success.png` | Initial Nav2 goal completion in the saved map; functional success, not a final-position accuracy measurement |
| 5 | `2026-11-05_Gazebo_Ground_Truth_Pose.png` | Gazebo Burger pose from `gz model -m burger -p`; simulator reference pose requiring frame/time correspondence |
| 6 | `2026-11-05_Coordinate_Alignment_Success.png` | Temporary world/map alignment comparison; preliminary residual, not independently validated navigation accuracy |
| 7 | `2026-11-05_Coordinate_Validation_D.png` | Proposed additional coordinate comparison D; raw poses and correspondence to reported residuals remain to be supplied |
| 8 | `2026-11-05_Coordinate_Validation_E.png` | Proposed additional coordinate comparison E; raw poses and correspondence to reported residuals remain to be supplied |

- Map YAML/image: reported VM paths above; files not supplied to this repository.
- Raw terminal logs, odometry-rate evidence, calibration pairs and timestamps:
  not supplied.
- rosbag2 recordings, trial CSV files and artifact checksums: not supplied.

## Discussion and Next Step

The reported work establishes an initial simulation workflow from robot
spawning through mapping and AMCL localisation to Nav2 goal navigation. The
empty-workspace build, visible map and successful first goal support functional
progress at their stated scope. They do not quantify mapping or navigation
accuracy, repeatability, or physical-robot performance.

The alignment investigation shows why coordinate frames and localisation must
be checked before calculating errors. Resetting AMCL improved the reported
positional comparisons, but the temporary transform still lacks an independent
reference. The 54.7° heading discrepancy requires a stable-state measurement;
continued rotation remains only a possible explanation.

Next steps, not completed work:

1. Verify final robot heading after navigation has completely stopped.
2. Independently validate the world-to-map transformation using known static
   landmarks, retaining calibration and independent validation measurements.
3. Develop a ROS 2 Python evaluation node to send Nav2 goals and capture task
   outcomes.
4. Record Gazebo ground-truth final positions, transformed goal positions,
   navigation durations and position errors in a common validated frame.
5. Export repeatable experiment results to CSV files, retaining failures as well
   as successes.
6. Conduct at least 10 navigation trials. Count a trial as successful only when
   it completes without collision or manual intervention and its final-position
   error is within 0.2 m; the required minimum is at least 8 successful trials.
7. Connect the physical TurtleBot3 Raspberry Pi over SSH and validate real
   LiDAR data; preserve the distinction between historical Windows access and
   current VM/robot verification.
8. Compare simulation and physical-robot performance using recorded results.
