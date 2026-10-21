# CHATGPT

TurtleBot3 Burger ROS 2 SLAM final-year project. The required physical-robot
baseline is **Ubuntu 22.04 Server 64-bit (ARM64) + ROS 2 Humble**.

## Real TurtleBot3 Burger Setup / Physical Robot Setup

Start with the [physical robot setup log](docs/real_robot_setup.md).
It records hardware identification, SD-card preparation, Ubuntu, networking and
SSH, ROS 2, robot drivers, and the evidence required before movement and SLAM.

**Current progress (21 October 2026):** the Windows PC and H: microSD card have
been inspected using read-only commands. Before imaging, H: mapped to physical
Disk 3 (USB reader, approximately 64 GB, one exFAT partition). The owner confirmed a
Raspberry Pi 4 Model B and no card data requiring preservation. Step 1 is
complete. The official Ubuntu 22.04.5 Raspberry Pi ARM64 Server image has been
downloaded to the PC and matches the published SHA256 checksum. The owner
approved overwriting Disk 3. **Image writing, readback verification and separate
first-boot seed inspection have passed.** H: now contains the `system-boot`
FAT32 partition, with a second Linux partition also present. The first-boot seed
specifies `ubuntu`, hostname `tb3-burger`, SSH public-key access,
`en_GB.UTF-8` and `Europe/London`. The owner selected an iPhone hotspot; its
private Wi-Fi seed has now been saved and read back successfully with country
GB. The next step is to confirm the power arrangement, then perform first boot
and test the actual network connection. No hotspot credentials are published.
SSH, robot bringup, sensor topics, motion, mapping, localisation and navigation
are **Pending / To be tested**.

Disk numbers can change. The setup log requires a fresh device check and explicit
owner confirmation before any formatting, partition deletion or image writing.

## Existing ROS 2 Project Work

At the initial inspection, `main` contained only the original README heading.
The existing ROS 2 SLAM scaffold is on
[`scaffold/ros2-slam-fyp`](https://github.com/CXRISME/CHATGPT/tree/scaffold/ros2-slam-fyp)
and is proposed in [PR #1](https://github.com/CXRISME/CHATGPT/pull/1).
Its source files, configuration examples, experiment template and documentation
are retained on that branch. This physical-setup documentation update does not
merge or replace that work. No completed Gazebo runs or physical-robot results
were verified during this inspection.
