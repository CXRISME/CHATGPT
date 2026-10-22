# CHATGPT

TurtleBot3 Burger ROS 2 SLAM final-year project. The required physical-robot
baseline is **Ubuntu 22.04 Server 64-bit (ARM64) + ROS 2 Humble**.

## Real TurtleBot3 Burger Setup / Physical Robot Setup

Start with the [physical robot setup log](docs/real_robot_setup.md).
It records hardware identification, SD-card preparation, Ubuntu, networking and
SSH, ROS 2, robot drivers, and the evidence required before movement and SLAM.
For continuing from the Ubuntu VirtualBox guest, read the
[Ubuntu VM handoff](docs/ubuntu_vm_handoff.md).

**Current progress (22 October 2026):** the Windows PC and H: microSD card have
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
GB. The owner visually traced the existing OpenCR connector labelled 5V/GND to
Pi physical pins 4/6 respectively. **Step 3 first boot and key-based SSH access
have passed**, with the connection checked again on 22 October. Terminal output
confirms `tb3-burger`, user `ubuntu`, Ubuntu 22.04.5 LTS, `aarch64`, Raspberry Pi 4
Model B Rev 1.5 and cloud-init `done`. Locale, timezone, clock synchronisation
and SD-card expansion were checked; system updates are pending. The Windows SSH
shortcut `ssh tb3-burger` has also been configured and tested. Private network
addresses and hotspot credentials are not published.

ROS 2 Humble installation, OpenCR revision/firmware identification, LiDAR data,
robot bringup, motion, mapping, localisation and navigation remain
**Pending / To be tested**. The owner reported LiDAR rotation with the wheels
and chassis stationary; this is not a passed sensor or movement test.

The Ubuntu workstation VM has now been identified from its terminal output as
**Ubuntu 22.04.5 LTS, x86_64**. Its Codex CLI installer reported version 0.163.0
installed successfully; `codex --version` then returned `codex-cli 0.163.0`.
ChatGPT sign-in was verified by `codex login status`, which returned
`Logged in using ChatGPT`. A project/model task has not yet been tested.
VM-to-Pi SSH and ROS 2 discovery checks are pending. The VM's name is not
evidence that ROS is installed.

Disk numbers can change. The setup log requires a fresh device check and explicit
owner confirmation before any formatting, partition deletion or image writing.

## Existing ROS 2 Project Work

At the initial inspection, `main` contained only the original README heading.
The existing ROS 2 SLAM scaffold is on
[`scaffold/ros2-slam-fyp`](https://github.com/CXRISME/CHATGPT/tree/scaffold/ros2-slam-fyp)
and is proposed in [PR #1](https://github.com/CXRISME/CHATGPT/pull/1).
Its source files, configuration examples, experiment template and documentation
are retained on that branch. This physical-setup documentation update does not
merge or replace that work. No completed Gazebo experiments, robot motion tests
or SLAM trials have been verified in this setup log.
