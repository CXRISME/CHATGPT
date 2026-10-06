# rosbag2 Recordings

Raw recordings in this directory are excluded by `.gitignore`; this guide remains tracked in Git. Naming: `YYYYMMDD_maze01_run01/`. Use a new directory for each run.

Minimum topics to consider: `/scan`, `/odom`, `/tf` and `/tf_static`, adjusted to the actual driver. Also record `/clock` for simulation. During navigation, add localisation, goals, planned paths and other topics as needed, and record their types and QoS settings.

See [setup.md](../docs/setup.md) for recording and replay commands. After recording, check message counts, time ranges, static TF and replayability. Document missing data rather than claiming full reproducibility.

Keep large recordings in a chosen external location. Record the accessible location, file names, sizes, SHA256 checksums and retrieval instructions in the experiment record. `metadata.yaml` alone contains no scan data and is not a substitute for a complete recording. Exclude private network details and unrelated imagery.
