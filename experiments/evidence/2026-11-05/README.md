# Screenshot Evidence for 5 November 2026

These 21 PNG files were extracted from the owner-supplied Word document
`fyp进行记录.docx` and reviewed on **12 November 2026**. Each file preserves the
original embedded PNG bytes. Source image numbers refer to `word/media/imageN.png`
inside the DOCX, rather than to figure numbering or verified capture times.

The [development record](../../2026-11-05_slam_nav2_development.md) explains the
experiment and its remaining limitations. The [machine-readable manifest](manifest.json)
records the source document SHA256, image mapping, dimensions, byte counts and
SHA256 checksums. The source Word document is retained by the owner and is not
committed here. Screenshot capture timezone has not been established.

## Source and Integrity

Source document SHA256:

`0004b93d070ffaf37ff45c54be7463b061676b78d68c36807e6ee4b416dfa0a3`

No screenshot has been cropped, resized, redrawn or recompressed for this evidence
collection. Captions describe visible content; a source-document caption is not
used to override contradictory terminal output. In particular, image 1 precedes
robot spawning and image 2 records the initial spawn failure.

## Image Index

| Source image | Repository file | Caption |
| --- | --- | --- |
| 1 | [2026-11-05_Gazebo_World_Before_Spawn.png](2026-11-05_Gazebo_World_Before_Spawn.png) | TurtleBot3 World and nine cylinders before Burger appears in the model list. |
| 2 | [2026-11-05_Burger_Spawn_Timeout.png](2026-11-05_Burger_Spawn_Timeout.png) | Initial automatic spawning fails because /spawn_entity is unavailable after a 30-second timeout. |
| 3 | [2026-11-05_Burger_Spawn_Success.png](2026-11-05_Burger_Spawn_Success.png) | Burger appears in the Gazebo model list and arena, with simulated LiDAR rays. |
| 4 | [2026-11-05_Burger_Model_LiDAR_Closeup.png](2026-11-05_Burger_Model_LiDAR_Closeup.png) | Close-up of the Burger model and simulated LiDAR visualisation. |
| 5 | [2026-11-05_LiDAR_Frequency_Test.png](2026-11-05_LiDAR_Frequency_Test.png) | Terminal reports successful Burger spawning, lists ROS topics and displays ros2 topic hz /scan measurements around 4.3 Hz. |
| 6 | [2026-11-05_Odometry_Frequency_Test.png](2026-11-05_Odometry_Frequency_Test.png) | Two ros2 topic hz /odom checks; the final displayed rate is 25.690 Hz with window count 603. |
| 7 | [2026-11-05_Cartographer_Initial_Map.png](2026-11-05_Cartographer_Initial_Map.png) | Cartographer RViz2 configuration showing an intermediate occupancy grid, LaserScan and TF. |
| 8 | [2026-11-05_Cartographer_SLAM_Result.png](2026-11-05_Cartographer_SLAM_Result.png) | Cartographer occupancy grid shows the enclosing walls and nine cylinders alongside Gazebo and teleoperation output. |
| 9 | [2026-11-05_Occupancy_Grid_Preview.png](2026-11-05_Occupancy_Grid_Preview.png) | Embedded 122 by 124 pixel occupancy-grid preview; not the saved PGM map artifact. |
| 10 | [2026-11-05_Nav2_Localisation_View.png](2026-11-05_Nav2_Localisation_View.png) | RViz2 navigation/localisation display, occupancy grid and costmaps alongside Gazebo. |
| 11 | [2026-11-05_Nav2_Goal_In_Progress.png](2026-11-05_Nav2_Goal_In_Progress.png) | RViz2 Nav2 goal and navigation feedback view during the initial navigation sequence. |
| 12 | [2026-11-05_Nav2_First_Success.png](2026-11-05_Nav2_First_Success.png) | RViz2 reports Navigation active, Localisation active and Feedback reached; this is functional goal completion evidence. |
| 13 | [2026-11-05_Keyboard_Teleoperation.png](2026-11-05_Keyboard_Teleoperation.png) | Keyboard teleoperation terminal output alongside the Gazebo robot and arena. |
| 14 | [2026-11-05_Gazebo_Ground_Truth_Pose.png](2026-11-05_Gazebo_Ground_Truth_Pose.png) | Gazebo model-pose terminal output alongside RViz2 and Gazebo; simulator reference pose evidence. |
| 15 | [2026-11-05_ROS_Map_Pose.png](2026-11-05_ROS_Map_Pose.png) | Gazebo pose output followed by tf2_echo map base_footprint with simulation time; coordinate comparison before alignment. |
| 16 | [2026-11-05_Gazebo_Pose_Recheck.png](2026-11-05_Gazebo_Pose_Recheck.png) | Further simulator and ROS pose inspection alongside RViz2 and Gazebo. |
| 17 | [2026-11-05_Coordinate_Frame_Investigation.png](2026-11-05_Coordinate_Frame_Investigation.png) | Terminal and RViz2/Gazebo views used to investigate coordinate-frame alignment. |
| 18 | [2026-11-05_Coordinate_Frame_Transform.png](2026-11-05_Coordinate_Frame_Transform.png) | Terminal and RViz2/Gazebo views during temporary reference-frame alignment work. |
| 19 | [2026-11-05_Coordinate_Alignment_Success.png](2026-11-05_Coordinate_Alignment_Success.png) | Map/LaserScan alignment view and pose output after the reported localisation adjustment; preliminary alignment evidence. |
| 21 | [2026-11-05_Coordinate_Validation_D.png](2026-11-05_Coordinate_Validation_D.png) | Further simulator/ROS coordinate comparison D; independent landmark calibration and navigation accuracy are not established. |
| 22 | [2026-11-05_Coordinate_Validation_E.png](2026-11-05_Coordinate_Validation_E.png) | Further simulator/ROS coordinate comparison E; independent landmark calibration and navigation accuracy are not established. |

## Interpretation Limits

- Image 9 is only an embedded occupancy-grid preview. It is not the original
  `2026-11-05_cartographer_map.pgm`; the saved PGM/YAML pair has not been supplied.
- Topic-rate windows shown by `ros2 topic hz` are displayed sample-window counts,
  not elapsed seconds. The figures support the rounded simulated rates of about
  4.3 Hz for `/scan` and 25.7 Hz for `/odom`; they do not measure a physical sensor.
- RViz2 `Feedback: reached` supports initial functional Nav2 goal completion.
  Its displayed zero timing values are not a recorded navigation duration, and
  the screenshot does not establish independently measured final-position error.
- Coordinate comparisons use a temporary reference transform derived from
  preliminary robot poses. The reported 0.067 m, 0.052 m and 0.011 m residuals
  remain coordinate-alignment residuals, not validated navigation goal errors.
- Independent landmark calibration, stable final-heading verification and the
  formal ten-trial evaluation remain pending. These images do not demonstrate
  compliance with the 0.2 m navigation-accuracy requirement or physical-robot
  runtime performance.
- Screenshots preserve selected terminal output, not complete machine-readable
  logs, map files, CSV trials, calibration datasets or rosbag recordings.

## Excluded Source Images

Source images 20 and 23 show ChatGPT-generated interpretation/calculations.
They are omitted from the experiment evidence because they are not primary
simulator or ROS measurements. Their original embedded paths and checksums
remain listed in the manifest to account for all 23 source images.
