# Experiment Record: <YYYYMMDD_maze01_run01>

> Copy this file to create a new record. Write "not measured" or "to be confirmed" for missing information. This blank template does not represent an executed experiment.

## Objective and Hypothesis

- What this run will verify:
- Predefined pass/fail criteria:
- Comparison baseline and the single changed variable:

## Environment and Versions

| Item | Observed details |
| --- | --- |
| Date, time zone and operator | |
| Code branch and commit SHA; uncommitted changes | |
| PC OS, architecture, ROS2 and RMW implementation | |
| Raspberry Pi model, OS, ROS2, drivers and firmware | |
| LiDAR model, frame ID and measured scan frequency | |
| SLAM Toolbox / Nav2 package versions | |
| Communication domain, network and clock synchronisation | |
| Maze ID, dimensions, wall materials and environment changes | |
| Battery, speed limits, start/goal and driven route | |
| Parameter file path and SHA; use_sim_time | |
| Map version, bag path, external data location and SHA256 | |

## Procedure and Parameters

Separate PC and Raspberry Pi steps. Paste the complete commands actually executed and key outputs, and state which environment files were sourced. Exclude passwords, network credentials and tokens.

```bash
# Commands actually executed for this run
```

| Parameter | Baseline value | This run's value | Reason for change |
| --- | --- | --- | --- |
| | | | |

## Observations and Results

- Driver, topic, TF and timestamp checks:
- Map, scan and loop closure observations:
- Outcome: not run / passed / failed / partially passed (select and explain)

| Metric | Predefined threshold | Measured value and units | Method / evidence |
| --- | --- | --- | --- |
| Mapping: fixed wall segment error | | | |
| Localisation: independent reference point error | | | |
| Navigation: successful attempts / all attempts | | | |
| Navigation: elapsed time, path length and collisions | | | |

Write "not applicable" where appropriate. Do not report absolute localisation accuracy without a ground-truth position. Give repeated runs separate IDs and preserve failures.

## Evidence Index

- RViz screenshots / video:
- Map YAML and image:
- rosbag2 information: duration, message counts, topics and TF completeness:
- Log excerpts, data file sizes and checksums:

## Discussion and Next Step

- Observed facts:
- Suspected causes (label hypotheses rather than presenting them as proven):
- Limitations and unverified items:
- The next single change and its acceptance criteria:
