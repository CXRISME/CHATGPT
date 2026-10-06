# Maps

Naming: `YYYYMMDD_maze01_run01.yaml` with the matching `.pgm` or actual output image format. Commit the pair together and check the YAML `image` path. Relative paths must resolve on another machine. Small maps can be tracked in Git; keep an index for large files instead.

In the corresponding experiment record, identify the source code SHA, SLAM parameters, environment dimensions, recording and quality checks. Use a new name for each experiment to preserve earlier maps.

An occupancy grid map supports later Nav2 navigation; it is different from the SLAM pose graph. To continue optimisation or mapping, save the pose graph separately using the SLAM Toolbox serialisation interface and record the software version. No maps have been generated yet.
