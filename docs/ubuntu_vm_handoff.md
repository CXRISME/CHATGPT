# Ubuntu VM Workstation Handoff

Updated: **22 October 2026**. Continue the TurtleBot3 Burger setup from the
current verified state. Read [the physical setup evidence log](real_robot_setup.md)
before making changes. The required ROS baseline remains **Ubuntu 22.04 +
ROS 2 Humble**. The Pi uses the ARM64 Server image; the workstation guest uses
the x86_64 desktop environment.

## Verified Workstation Information

The owner supplied a screenshot of these commands in the VirtualBox guest:

```bash
cat /etc/os-release
uname -m
```

The first command identifies the installed distribution; the second checks the
running architecture. The screenshot shows:

| Item | Evidence / result |
| --- | --- |
| Virtualisation platform | Oracle VirtualBox window |
| Ubuntu | `Ubuntu 22.04.5 LTS`, Jammy Jellyfish |
| Architecture | `x86_64` |
| Guest shell | `vboxuser@ROS2humble` |
| VM resources | Read-only host inspection: 4 virtual CPUs, 11,165 MiB configured memory |
| VM network | Read-only host inspection: adapter 1 is NAT; adapter 2 disabled |
| Guest ROS installation | **Pending inspection**; the VM name does not verify ROS |
| Codex CLI installation and sign-in | **Pending / To be tested** |
| Guest-to-Pi SSH and ROS 2 discovery | **Pending / To be tested** |

## Next Step — Install Codex CLI in the Guest

The downloaded `chatgpt_amd64.deb` desktop package is separate from Codex CLI.
As checked on 22 October 2026, the official Linux desktop preview lists Ubuntu
24.04 and 26.04 as supported Ubuntu versions; 22.04 is not listed. Preserve the
project's Jammy/Humble baseline and use the official CLI installation route.
Do not upgrade the Ubuntu distribution merely to install the desktop app.

Run this next command in the **Ubuntu VM terminal**, not in the Pi SSH session
or Windows PowerShell:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

This downloads and runs the official standalone Codex CLI installer for the
current user. `curl -f` rejects HTTP errors, `-sS` keeps progress quiet while
showing errors, and `-L` follows redirects. This command has been provided as
the next step; its execution and result in the guest have **not** been verified.
Check its actual output before proceeding. An error is a troubleshooting input,
not a reason to reinstall Ubuntu or the robot image.

After the installation output is checked, verify the command in the guest:

```bash
codex --version
```

This reports the installed CLI version. Follow any installer PATH instructions
or open a new terminal if necessary; do not assume a successful download means
that the command is available. Version verification remains **Pending**.
Then use `codex` from the chosen project directory and complete the sign-in
flow locally. Do not publish authentication files, login codes or tokens.

Sources: [official Codex CLI installation](https://learn.chatgpt.com/docs/codex/cli),
[official Linux desktop support matrix](https://learn.chatgpt.com/docs/linux/linux-app).

## Existing Robot State to Preserve

- Pi 4 Model B Rev 1.5: Ubuntu 22.04.5 LTS, `aarch64`, hostname `tb3-burger`,
  account `ubuntu`, cloud-init `done`; verified over SSH from Windows.
- Dedicated-key SSH access from Windows and its local `ssh tb3-burger` alias
  passed. This is not evidence of SSH access from the VM.
- Locale `en_GB.UTF-8`, timezone `Europe/London`, active NTP and clock sync,
  active SSH service, sudo access and SD root expansion were checked.
- Ubuntu package updates and ROS 2 installation on the Pi have not started.
- Existing GPIO power cable was visually traced by the owner: OpenCR-labelled
  5V to Pi physical pin 4, GND to physical pin 6. Electrical load tests are pending.
- OpenCR revision/firmware and LiDAR model are unknown. LiDAR rotation with a
  stationary chassis was reported; actual `/scan` and other topics are untested.
- No robot firmware write, wheel teleoperation, real SLAM, localisation, Nav2
  or maze test has been performed.

## Continue in Small Checked Steps

1. Verify Codex CLI installation and sign-in in the guest.
2. Inspect existing guest project directories and ROS installations before
   cloning or installing anything. Retain all existing Gazebo/ROS work.
3. Prepare VM-specific SSH access. Windows' key, known-hosts file and alias do
   not automatically exist inside the VM. The Pi account was prepared with a
   locked password; do not assume password login is available. A guest-specific
   public key can be authorised through the already-working Windows connection.
   Keep every private key outside chat and Git.
4. Test VM-to-Pi SSH. NAT is the observed configuration, not proof that DDS
   communication works or fails. Make network changes based on actual test
   results; SSH success alone is not a ROS discovery test.
5. Resume Step 4 Ubuntu updates on the Pi, inspect their output, and perform
   required post-update checks before installing Humble. Confirm peripheral
   versions before selecting version-dependent firmware or drivers.
6. After Humble is verified on both the VM and Pi, test bidirectional ROS 2
   discovery and check the relevant network and DDS settings before robot
   bringup. This test has not yet been performed.

Repository: **CXRISME/CHATGPT**, publication branch **main**. The existing
`scaffold/ros2-slam-fyp` branch and PR #1 have been preserved. Do not reset,
overwrite or merge existing work merely to change workstation environment.
Publish English documentation after a clear checkpoint, with actual results
and **Pending / To be tested** for work not yet verified. Never re-image the SD
card or start motion as part of this workstation handoff.
