# Real TurtleBot3 Burger Setup

This is the evidence log for configuring the physical TurtleBot3 Burger for the
SLAM final-year project. In this project, the user's term "Pico Pi" means the
robot's **Raspberry Pi**, not a Raspberry Pi Pico microcontroller.

Required baseline: **Ubuntu 22.04 Server 64-bit (ARM64), ROS 2 Humble,
TurtleBot3 Burger**. The baseline is a requirement, not evidence of an installed
system. Do not substitute a different Ubuntu or ROS distribution silently.

## Current Status

**21 October 2026 — Step 1 complete.** The PC and SD-card read-only audit is
complete. The owner identified the board as **Raspberry Pi 4 Model B** and
confirmed that the H: microSD card has no data requiring preservation.
No formatting, partition deletion, image
writing, robot firmware update or motion command has been performed.
No destructive SD-card operation has been authorised.

Each step will be completed and its actual output checked before the next step.
When a command fails, preserve its output and diagnose that failure before
considering a reinstall. All later stages below are **Pending / To be tested**.

## Repository Baseline and Preservation

- Repository: `CXRISME/CHATGPT`; requested publication branch: `main`.
- Initial `main` commit: `94bb033a20d6584ecdb750324d6d69fd9c9380b8`.
  Its only tracked file was a README containing `# CHATGPT`.
- Existing project scaffold:
  [`scaffold/ros2-slam-fyp`](https://github.com/CXRISME/CHATGPT/tree/scaffold/ros2-slam-fyp),
  inspected at `893ac18b80895deb1b34fd385f62f89f360785b4`;
  [PR #1](https://github.com/CXRISME/CHATGPT/pull/1) was open and unmerged.
- That branch contains `src/maze_slam_bringup`, environment examples, setup and
  roadmap documentation, an experiment template, and map/recording conventions.
  It remains unchanged by this documentation stage.
- This audit did not identify or validate completed Gazebo experiments. Existing
  simulation work elsewhere must be retained; its location can be linked later.
- Local checkout for this documentation: `E:\ChatGPT\FYP\CHATGPT`.
  The parent folder's pre-existing empty Git repository was left intact.

## Step 1 — Identify the PC, SD Card and Hardware

### Host observations

| Item | Observed result | Scope |
| --- | --- | --- |
| Current host | Windows 11 Home, Chinese edition, 64-bit | Inspected directly |
| Windows version | `10.0.26200` | Inspected directly |
| Git | Available | Repository cloned and inspected |
| Windows OpenSSH client | Available | No robot SSH connection tested |
| Raspberry Pi Imager | Installed, product version `v2.0.6` | Executable metadata inspected; no write started |
| Ubuntu/ROS workstation | Pending | No compatible Ubuntu/ROS runtime verified in this Windows session |

The Windows PC can prepare the card and act as an SSH client. Its current
Windows session is not proof of an Ubuntu 22.04 / ROS 2 Humble workstation.
The environment used for later RViz, SLAM and Nav2 must be verified separately.

### Physical disk observations

These values are a dated snapshot, not a permanent device selection.

| Disk | Device reported by Windows | Capacity | Role / action |
| --- | --- | --- | --- |
| 0 | SKHynix NVMe SSD | 1,024,209,543,168 bytes | Boot/system disk; contains C: and E:; exclude from imaging |
| 1 | ZHITAI TiPlus7100 NVMe SSD | 2,048,408,248,320 bytes | Internal data disk; exclude from imaging |
| 2 | Generic MassStorageClass, USB | 0 bytes, No Media | Empty reader presentation; exclude from imaging |
| 3 | Generic MassStorageClass, USB | 62,534,975,488 bytes | H: card candidate; inspection only; writing not authorised |

For the H: device:

- Current physical device path: `\\.\PHYSICALDRIVE3`.
- Capacity: approximately **62.53 GB / 58.24 GiB**, consistent with a nominal
  64 GB card; the printed capacity and brand still need checking.
- MBR partition table; one partition, number 1, mounted as H:.
- Partition size: `62,518,198,272` bytes; offset: `16,777,216` bytes.
- Filesystem: exFAT; reported healthy; no volume label.
- Volume size: `62,501,421,056` bytes; free: `62,500,634,624` bytes.
- Root directory listing showed only `System Volume Information`.
- Windows reports `IsBoot=False`, `IsSystem=False`, `IsReadOnly=False`.

**Interpretation:** no Ubuntu/Raspberry Pi installation was identified by this
read-only Windows partition and directory inspection. No FAT boot partition or
Linux root partition was reported. This is not a forensic examination and does
not prove that the card has no recoverable data. The generic USB device name
identifies the reader's presentation, not the card brand or Raspberry Pi model.

### Read-only inspection commands

These PowerShell commands document the audit. They do not format or write the
SD card. They have already been run; the owner does not need to repeat them now.

```powershell
Get-CimInstance Win32_OperatingSystem |
    Select-Object Caption, Version, OSArchitecture
```

Reports the operating system and architecture of the computer executing the
command, not the Raspberry Pi.

```powershell
Get-Partition -DriveLetter H |
    Format-List DiskNumber, PartitionNumber, DriveLetter, Type, Size, AccessPaths
```

Maps H: to its physical disk and partition. This reported Disk 3, partition 1.

```powershell
Get-Disk |
    Select-Object Number, FriendlyName, BusType, PartitionStyle,
        OperationalStatus, IsBoot, IsSystem, Size
Get-Partition -DriveLetter C,E |
    Select-Object DiskNumber, PartitionNumber, DriveLetter, Size
```

Lists disks and their roles, then checks where C: and E: reside. Both were on
Disk 0. These commands make the system disk distinguishable from the SD card.

```powershell
Get-Partition -DiskNumber 3 |
    Select-Object DiskNumber, PartitionNumber, DriveLetter, Type, Size, Offset
Get-Volume -DriveLetter H |
    Format-List DriveLetter, FileSystemLabel, FileSystem, DriveType,
        HealthStatus, Size, SizeRemaining
Get-ChildItem -LiteralPath 'H:\' -Force |
    Select-Object Mode, Length, Name
```

Reports all partitions on the currently identified candidate, volume properties
and root directory entries. The explicit `3` is valid for this audit snapshot
only; first re-identify H: if the card is reconnected or a write is proposed.

### Hardware inventory

| Component | Recorded information | Verification status |
| --- | --- | --- |
| Robot | TurtleBot3 Burger | Owner specified; physical inspection pending |
| Raspberry Pi | Raspberry Pi 4 Model B; RAM and board revision not recorded | Model confirmed by owner from board identification |
| microSD card | H: device identified above; no data requiring preservation | Owner confirmed no backup needed; printed brand/capacity not recorded |
| OpenCR control board | Exact board revision and installed firmware unknown | Pending label and later USB/firmware checks |
| Left and right DYNAMIXEL motors | Models, IDs and baud rate unknown | Pending labels and later communication checks |
| LiDAR | Model and interface unknown | Pending label; do not infer from Burger |
| Power and cabling | Battery condition, power path and USB cables unverified | Pending physical inspection |

Keep robot power off while handling the microSD card or inspecting cabling.
The owner supplied the Raspberry Pi model and confirmed no card data needs
preserving. The printed card brand/capacity can be added to the inventory later.
Board identification cannot be obtained from this exFAT card.
LiDAR, OpenCR and motor details must be confirmed before their respective
driver, firmware or motor-configuration steps.

### Acceptance and write gate

- [x] Identify the current host and map H: to a physical disk.
- [x] Inspect partitions and visible files without modifying the card.
- [x] Distinguish internal/system disks from the SD-card candidate.
- [x] Owner identifies the Raspberry Pi 4 Model B and the H: microSD card.
- [x] Owner confirms no card data requires preservation; no backup requested.
- [x] Verify Pi 4 Model B is compatible with the required 22.04 ARM64 image.
- [ ] Immediately before any destructive action, re-read disk information and
  display the target physical disk, reader name, capacity, partitions and drive
  letter. Explain that imaging replaces the entire disk, including its partitions.
- [ ] Obtain explicit owner confirmation for that exact disk and operation.

Drive letters and disk numbers can change. The snapshot above is **not**
permission to write Disk 3 later. Never target Disk 0 or Disk 1. No formatting,
partition deletion or image writing may occur before the write gate is satisfied.

## Next Image — Compatible Candidate, Not Written

For a compatible Raspberry Pi, ROBOTIS's Humble SBC instructions specify
**Ubuntu Server 22.04.5 LTS (64-bit)**. The official Raspberry Pi preinstalled
server image is:

```text
ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz
```

This is a candidate, not a downloaded, checksum-verified or written image.
The owner-confirmed Pi 4 Model B is compatible with this baseline.
Canonical's compatibility matrix lists 22.04 support for Pi 3B/3B+/4B, among
other models, but not Pi 5. A Pi 5 would require resolving the hardware/baseline
conflict before proceeding. Image selection,
SHA256 verification, Imager settings, write verification and first boot will be
recorded when performed.

Sources: [ROBOTIS SBC setup, Humble section](https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/),
[Canonical Raspberry Pi compatibility](https://ubuntu.com/hardware/docs/boards/how-to/ubuntu_supported/raspberry-pi/),
[official Ubuntu 22.04 images](https://cdimages.ubuntu.com/ubuntu/releases/22.04/release/).

## Configuration Record — Not Applied Yet

| Setting | Planned requirement / value | Actual result |
| --- | --- | --- |
| Ubuntu | Server 22.04, ARM64 | Pending |
| Image filename, source and checksum | Record verified image before writing | Pending |
| Username and hostname | Agree with owner before first-boot configuration | Pending |
| Wi-Fi | Confirm SSID, authentication type and regulatory country locally | Pending |
| SSH | Enable and verify Windows-to-Pi login and host identity | Pending |
| Locale | UTF-8 locale; exact selection pending | Pending |
| Timezone and clock sync | Confirm robot location/timezone; verify time sync | Pending |
| System updates | Update within Ubuntu 22.04 after network access works | Pending |
| ROS distribution | Humble | Pending installation |
| Shell environment | Source Humble; use `TURTLEBOT3_MODEL=burger` | Pending |
| DDS configuration | Confirm domain, middleware and discovery on both hosts | Pending |
| TurtleBot3 packages and dependencies | Select compatible Humble packages | Pending |
| OpenCR and DYNAMIXEL | Confirm hardware and firmware before version-specific actions | Pending |
| LiDAR driver and `LDS_MODEL` | Select only after reading the actual sensor label | Pending |

Do not publish passwords, Wi-Fi credentials, SSH private keys, private network
details, or cloud-init files containing secrets. Record sanitised settings and
results only. The chat's Europe/London timezone does not establish the robot's
physical location or Wi-Fi regulatory country.

## Later Stages — Pending / To Be Tested

This is a sequence of future acceptance gates, not instructions to execute now.
Commands will be added in small, checked steps as hardware is confirmed.

| Step | Stage | Evidence required before advancing | Status |
| --- | --- | --- | --- |
| 2 | Image preparation and approved write | Compatible board, verified image, explicit disk approval, successful write verification | Pending |
| 3 | Ubuntu first boot, network and SSH | Board/OS/architecture output and successful remote login from this PC | Pending |
| 4 | Ubuntu baseline | Updates, username, hostname, UTF-8 locale, timezone and clock sync verified | Pending |
| 5 | ROS 2 Humble | Correct repositories/architecture, working CLI and checked shell environment | Pending |
| 6 | Robot components | Compatible TurtleBot3, DYNAMIXEL/OpenCR and LiDAR software; device access verified | Pending |
| 7 | Stationary bringup | Actual messages on `/scan`, `/odom`, `/imu`, `/joint_states`, `/tf` and `/tf_static`; connected frames and valid timestamps | To be tested |
| 8 | Basic low-speed teleoperation | Forward, reverse, left, right and reliable stop verified in a clear floor area | To be tested |
| 9 | Detailed LiDAR and TF checks | Scan quality/rate/frame, odometry behaviour and TF continuity recorded | To be tested |
| 10 | SLAM Toolbox and map saving | Real-time configuration, checked map and saved YAML/image pair | To be tested |
| 11 | Localisation | Saved map loaded and localisation performance verified | To be tested |
| 12 | Nav2 navigation | Localisation, costmaps, goals, obstacle response and stopping verified | To be tested |
| 13 | Final maze test | Repeatable route, parameters, results and limitations recorded | To be tested |

Before motion, place the robot on a clear, level floor away from edges, verify
the stop control, and keep the power switch accessible. Use a confirmed low
speed. Check one short action at a time and stop between actions. Stop if motion
or feedback is unexpected. No movement or navigation success is claimed here.

## Issues and Resolutions

| Observation | Action / resolution | State |
| --- | --- | --- |
| Local parent directory has an empty Git repository with no remote | Cloned the existing GitHub `main` into a separate child directory; retained the parent | Resolved for documentation work |
| `main` does not contain the existing ROS 2 scaffold | Located its branch and open PR; retained both and added links | Recorded; no merge performed |
| Card exposes one exFAT partition, not a recognised Ubuntu layout | Recorded actual output; model and backup needs confirmed; await write gate | Pending imaging approval |
| Raspberry Pi and peripheral versions cannot be established from the card | Owner identified Pi 4 Model B; peripheral labels/firmware remain to be checked | Pi model resolved; peripherals pending |

No robot runtime errors have been observed because the robot has not yet been
booted or connected in this session. Add actual terminal errors, diagnoses and
verified resolutions here as they occur.

## Stage Publication Procedure

After a documented stage, review the diff and publish only that stage's files.
From the repository checkout:

```powershell
git status --short --branch
git diff --check
git diff -- README.md docs/real_robot_setup.md
git add -- README.md docs/real_robot_setup.md
git diff --cached --check
git diff --cached --stat
git commit -m "docs: record TurtleBot3 Burger SD card inspection"
git push origin main
git status --short --branch
```

`status` checks the branch and working tree; `diff` checks formatting and scope;
`add` stages the two explicit documentation paths; the cached diff checks what
will be committed. `commit` names the work actually completed, and `push`
publishes it to `main`. The final status checks for remaining local changes.
Use a new, accurate message for each later stage. If the remote advances,
inspect and integrate its changes before pushing; do not force-push.

For each future step, append the date, host, commands with explanations,
sanitised output, pass/fail result, unresolved issues and next action. Mark every
unperformed hardware test **Pending / To be tested**.
