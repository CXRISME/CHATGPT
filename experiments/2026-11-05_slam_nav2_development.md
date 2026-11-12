# Experiment Record: 2026-11-05 — ROS 2 SLAM and Nav2 Development

Project: **TurtleBot3 Burger — ROS 2 SLAM and Autonomous Navigation**.
Date: **5 November 2026**. This is a development checkpoint, not a formal
navigation-performance trial.

This entry follows the structure of `experiments/TEMPLATE.md` on the existing
`scaffold/ros2-slam-fyp` branch. The scaffold is not merged by this update.
Implementation steps and initial measurements were recorded from the owner's
progress report. On **12 November 2026**, the owner supplied a Word record
containing screenshots of the 5 November session. The evidence follow-up below
links the extracted original images and distinguishes visible output from
reported work and interpretation. The documentation update did not rerun the
experiments or access the VM. Original PGM/YAML map files, trial CSV files and
rosbag recordings have not been supplied.

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
| Simulation and visualisation | Gazebo Classic, official TurtleBot3 World, RViz2; screenshots show installation of `ros-humble-turtlebot3-gazebo` version `2.3.8-1jammy.20260915.233431`; other exact package versions not supplied |
| Robot model | TurtleBot3 Burger; `TURTLEBOT3_MODEL=burger` |
| SLAM and navigation software | TurtleBot3 packages and Gazebo integration, Cartographer, SLAM Toolbox and Navigation2 installed; Cartographer used for today's mapping, AMCL for localisation |
| Workspace | `~/fyp_slam_ws/src` created in the Ubuntu VM |
| Raspberry Pi / hardware | Physical TurtleBot3 Burger and Raspberry Pi; the October setup log identifies a Raspberry Pi 4 Model B and Ubuntu 22.04.5 LTS ARM64; today's report concerns SD preparation, connectivity configuration and replacement-battery checks |
| Network and SSH | First-boot Wi-Fi and SSH configured; current physical-robot SSH connectivity not fully verified; VM-to-Pi access remains pending |
| Timing and configuration | TF inspection command below explicitly uses `use_sim_time:=true`; screenshots contain TF simulator timestamps and topic-rate sample-window counts, but no synchronised Gazebo/TF sampling record or capture timezone |
| Run metadata | Experiment code revision, complete launch parameters, RMW, ROS domain, parameter hashes, complete route/start/goal records, map checksums and machine-readable logs not supplied; no repeated-trial dataset available |

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

The screenshots supplied later show the launch and topic-check commands below.
Other exact installation, manual-spawn and teleoperation command lines remain
untranscribed; no missing command is reconstructed as an executed step.

```bash
ros2 pkg prefix turtlebot3_gazebo
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 topic list
ros2 topic hz /scan
ros2 topic hz /odom
```

The launch screenshot records an initial 30-second `/spawn_entity` wait followed
by failure. A later terminal screenshot explicitly reports
`Successfully spawned entity [burger]`; the failure and recovery evidence are
both retained in the [source-image index](evidence/2026-11-05/README.md).

### Cartographer mapping and map saving

Launched Cartographer SLAM and generated a 2D occupancy grid of the simulated
environment. The reported visual result includes the outer walls and **nine
internal cylindrical obstacles**. This is a qualitative mapping observation;
no independent map-geometry error measurement is supplied.

Reported map files saved in the Ubuntu VM:

- `~/fyp_slam_ws/fyp_records/maps/2026-11-05_cartographer_map.pgm`
- `~/fyp_slam_ws/fyp_records/maps/2026-11-05_cartographer_map.yaml`

These are reported VM paths, not repository attachments. The alignment screenshot
shows a terminal readout from `cat` of the YAML path and the fields below. This
is screenshot evidence of metadata, not an inspected YAML/PGM file pair; original
file bytes and map checksums remain unavailable. The supplied 122 × 124 PNG is
indexed separately as a map preview and is not substituted for the saved PGM.

| Map parameter | Reported value |
| --- | --- |
| Resolution | 0.05 m/pixel |
| Origin | `[-3.34, -3.52, 0]` |
| Mode | `trinary` |
| Occupied threshold | 0.65 |
| Negate | 0; visible in the supplied terminal screenshot |
| Free threshold | 0.25; visible in the supplied terminal screenshot |

### AMCL localisation and initial Nav2 goal

1. Started Navigation2 with the saved map.
2. Initialised AMCL using RViz2's `2D Pose Estimate` and checked LaserScan
   alignment against the occupancy grid.
3. Successfully executed an initial autonomous task using `Nav2 Goal` and
   verified the `/navigate_to_pose` action interface.
4. Recovered the simulation and navigation environment after a virtual machine
   shutdown without reinstalling software or rebuilding the map.

This is an initial functional demonstration of mapping, localisation, path
planning and goal navigation. The supplied first-success screenshot visibly
shows Navigation2 feedback **`reached`**, with navigation/localisation active
and displayed distance remaining `0.00 m`. That display supports functional
goal completion; it does not measure ground-truth final-position error. Its
displayed `Time taken: 0 s` is not used as a measured navigation duration.
No validated task duration, stable final heading or formal collision/manual-
intervention trial record is supplied.

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
positional residuals below. The supplied screenshots now expose corresponding
Gazebo and aligned-frame pose readouts. Their Gazebo readouts lack matching
simulator timestamps, and the complete calibration protocol and independent
landmark measurements remain unavailable, so independent validation cannot be
established.

### Screenshot follow-up reviewed on 12 November 2026

The following pairs are transcribed from the terminal screenshots. D and E are
documentation labels for the two later comparisons, matching the proposed
evidence filenames; they are not formal navigation-trial IDs. Planar residuals
were recalculated as `sqrt((x_ros-x_gz)^2 + (y_ros-y_gz)^2)` using the displayed
coordinates, including the rounded TF values.

| Comparison / source | Gazebo world XY (m) | Aligned-frame ROS XY (m) | Recalculated planar residual | Gazebo / ROS yaw (rad) |
| --- | --- | --- | --- | --- |
| Initial aligned position; source `image19.png` | `[-0.960581, -0.547206]` | `[-0.969, -0.481]` | 0.06674 m, consistent with reported 0.067 m | `1.74125 / 1.721` |
| D; source `image21.png` | `[0.638673, -0.633912]` | `[0.632, -0.582]` | 0.05234 m, consistent with reported 0.052 m | `1.23646 / 1.268` |
| E; source `image22.png` | `[0.897465, 0.534088]` | `[0.905, 0.526]` | 0.01105 m, consistent with reported 0.011 m | `0.106861 / 1.061` |

For E, the displayed yaw difference is approximately 54.7°. RViz still shows
feedback `active`, distance remaining `0.04 m`, elapsed display `20 s` and one
recovery in that screenshot. It is not a stopped-state heading check or a
completed formal trial. Transient disconnected/invalid-frame messages also
precede successful TF output in the later screenshots. These still images do
not establish TF continuity or synchronised ground-truth comparison.

## Observations and Results

| Observation / metric | Reported result | Interpretation and limits |
| --- | --- | --- |
| Simulated LiDAR publishing rate | Approximately **4.3 Hz** | Figure 2 shows rolling averages 4.222–4.361 Hz; one entry is 4.321 Hz with window 31, final visible entry 4.287 Hz with window 114; window counts are samples, not seconds; not a physical LiDAR result |
| Simulated odometry publishing rate | Approximately **25.7 Hz** | Supplied odometry screenshot shows the second invocation ending at 25.690 Hz, window 603, min 0.010 s, max 0.074 s and std dev 0.00928 s; no machine-readable rate log supplied |
| Sensor/command/TF topics | `/scan`, `/odom`, `/cmd_vel`, `/tf` confirmed | Functional topic check; does not establish physical-robot communication |
| Keyboard teleoperation | Successful | Qualitative simulation result; no trajectory or speed dataset supplied |
| Cartographer map | Outer walls and nine internal cylinders represented | Qualitative occupancy-grid observation; map accuracy not measured |
| Initial Nav2 task | Successful task reported; screenshot feedback `reached`; `/navigate_to_pose` verified in the owner's report | Functional demonstration; no formal navigation accuracy or success-rate measurement |
| Preliminary alignment residual — first reported position | Approximately **0.067 m** | Figure 6 exposes the pose pair; independently calibrated reference not available |
| Preliminary alignment residual — subsequent position D | Approximately **0.052 m** | Figure 7 exposes the pose pair; unsynchronised coordinate-alignment comparison |
| Preliminary alignment residual — another position E | Approximately **0.011 m** | Figure 8 exposes the pose pair; not a navigation goal error |
| Heading discrepancy during comparison E | Approximately **54.7°** | Feedback is still active in Figure 8; actual rotation is not established by a still image; stopped-state verification pending |
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
| RViz Docking and Selector panels fail to load | Supplied navigation screenshots show missing `nav2_rviz_plugins/Docking` and `nav2_rviz_plugins/Selector` classes | Unresolved UI issue; Navigation2 feedback can still show `reached`; no repair is claimed |

## Evidence Index

The owner supplied `fyp进行记录.docx` on 12 November. Its 23 embedded images were
extracted and inspected. **21 original PNGs** are included unchanged under
[`evidence/2026-11-05/`](evidence/2026-11-05/README.md), with source-media mappings,
dimensions, byte sizes and SHA256 hashes in the
[manifest](evidence/2026-11-05/manifest.json). Two ChatGPT-response screenshots
(`image20.png` and `image23.png`) were excluded from the primary evidence set;
their analysis and instructions are not independent experimental observations.
The experiment date remains 5 November, and screenshot capture timezone is
unknown.

| Figure | Supplied evidence | Caption / evidence scope |
| --- | --- | --- |
| 1 | [Burger spawn success](evidence/2026-11-05/2026-11-05_Burger_Spawn_Success.png) | Source image3: Gazebo model tree includes Burger; robot and LiDAR rays visible after recovery |
| 2 | [LiDAR frequency test](evidence/2026-11-05/2026-11-05_LiDAR_Frequency_Test.png) | Source image5: successful spawn message, topic list and `/scan` rolling publishing-rate output around 4.3 Hz |
| 3 | [Cartographer SLAM result](evidence/2026-11-05/2026-11-05_Cartographer_SLAM_Result.png) | Source image8: enclosing walls and nine cylindrical obstacles represented in RViz alongside Gazebo; qualitative map result |
| 4 | [First Nav2 success](evidence/2026-11-05/2026-11-05_Nav2_First_Success.png) | Source image12: Navigation2 feedback `reached` and displayed distance remaining 0.00 m; no independent position-error measurement |
| 5 | [Gazebo ground-truth pose](evidence/2026-11-05/2026-11-05_Gazebo_Ground_Truth_Pose.png) | Source image14: `gz model -m burger -p` returns a simulator pose; adjacent map-frame TF illustrates the earlier mismatch |
| 6 | [Coordinate alignment comparison](evidence/2026-11-05/2026-11-05_Coordinate_Alignment_Success.png) | Source image19: Gazebo and aligned-frame TF values support the approximately 0.067 m residual; temporary transform and YAML readout visible |
| 7 | [Coordinate comparison D](evidence/2026-11-05/2026-11-05_Coordinate_Validation_D.png) | Source image21: displayed pose pair supports approximately 0.052 m alignment residual; samples lack a shared timestamp |
| 8 | [Coordinate comparison E](evidence/2026-11-05/2026-11-05_Coordinate_Validation_E.png) | Source image22: displayed pose pair supports approximately 0.011 m alignment residual; Nav2 feedback still active, heading verification pending |

The source Word caption calls image2 a successful startup log, but its terminal
actually shows the initial spawn timeout. It is retained as
[failure evidence](evidence/2026-11-05/2026-11-05_Burger_Spawn_Timeout.png).
Source image1 shows the world before Burger spawning, and source image4 is a
robot close-up rather than terminal-only success. Captions follow visible
content. Both rate-test screenshots initially warn that the topic does not
appear published, then show actual measurements.

- Original map YAML/PGM files and their checksums: not supplied; screenshot
  metadata and a PNG preview are available.
- Odometry-rate output and several pose pairs: now available as screenshots;
  complete machine-readable logs and synchronised calibration data remain absent.
- rosbag2 recordings and navigation-trial CSV results: not supplied. The evidence
  manifest contains image provenance, not a navigation-trial dataset.

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
