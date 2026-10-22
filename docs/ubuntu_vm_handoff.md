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
| Download tool | Initially missing; subsequent installer download ran successfully, confirming curl is now available |
| Codex CLI installer | Owner's screenshot reports `0.163.0 installed successfully` on Linux x64 |
| CLI command/version verification and sign-in | **Pending / To be tested** |
| Guest-to-Pi SSH and ROS 2 discovery | **Pending / To be tested** |

## Codex CLI Installation Evidence and Next Checks

The downloaded `chatgpt_amd64.deb` desktop package is separate from Codex CLI.
As checked on 22 October 2026, the official Linux desktop preview lists Ubuntu
24.04 and 26.04 as supported Ubuntu versions; 22.04 is not listed. Preserve the
project's Jammy/Humble baseline and use the official CLI installation route.
Do not upgrade the Ubuntu distribution merely to install the desktop app.

### Initial attempt — missing curl

The owner's next terminal screenshot on 22 October showed:

```text
Command 'curl' not found, but can be installed with:
sudo apt install curl
```

The installer download did not run. Returning to a shell prompt after the pipe
is not installation success. The following corrective command was provided for execution in the
**Ubuntu VM terminal**, not in the Pi SSH session or Windows PowerShell:

```bash
sudo apt update && sudo apt install curl
```

`apt update` refreshes the guest's package indexes; it does not upgrade the
Ubuntu distribution. `&&` starts `apt install curl` only if that succeeds.
The installation uses the VM user's sudo password, entered locally. The owner
then reported the APT lock wait described below. A later successful installer
download confirms that curl became available, but its exact package version and
APT completion output were not supplied. No VM or SD reinstallation was needed
for the successful installer retry.

### Curl installation waiting for automatic updates

The next screenshot showed repeated `Waiting for cache lock` messages for
`/var/lib/dpkg/lock-frontend`, held by process `6767 (unattended-upgr)`, with a
displayed wait of 159 seconds. This identifies a competing automatic-updates
process; that duration alone does not establish a hang. At that point curl and
Codex installation were still pending.

The owner was advised to keep the waiting APT terminal open. The proposed
read-only diagnostic in a second guest terminal was:

```bash
sudo tail -n 20 /var/log/unattended-upgrades/unattended-upgrades-dpkg.log
```

This reads the latest package-installation output from automatic updates and
does not interrupt them. Inspect the actual log before considering further
action. Do not delete lock files or force-kill the updater to bypass the wait.
When the updater releases its lock, the waiting installation can continue.
No updater log or final APT output was supplied. The later installer download
worked, but that does not separately verify how the automatic update completed.
No force-unlock command was prescribed.

Sources: [Ubuntu automatic-update logs](https://ubuntu.com/server/docs/how-to/software/automatic-updates/),
[Debian dpkg FAQ on lock files](https://wiki.debian.org/Teams/Dpkg/FAQ).

### Installer retry — success reported in the guest

The owner reran the official installation command in the guest:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

This downloads and runs the official standalone Codex CLI installer for the
current user. `curl -f` rejects HTTP errors, `-sS` keeps progress quiet while
showing errors, and `-L` follows redirects. The next screenshot on 22 October
showed these installer results:

| Installer observation | Reported result |
| --- | --- |
| Platform | Linux (x64) |
| Resolved version | `0.163.0` |
| Package location | Under `/home/vboxuser/.codex/packages/standalone/releases/` |
| PATH persistence | Installer reported adding PATH to `/home/vboxuser/.bashrc` |
| Completion | `Codex CLI 0.163.0 installed successfully.` |
| Start prompt | Owner selected `Y`; output showed `Launching Codex`, then the guest shell prompt |

This records installer-reported success, not a separately executed version
check or a signed-in session. The screenshot did not show authentication
completion. Returning to the shell alone is not evidence of an installation
failure. Check actual command output before choosing another installation path.

### Next check — current-shell PATH and CLI execution

The installer supplied a current-terminal PATH instruction. In the guest's
existing terminal, the next commands are:

```bash
export PATH="$HOME/.local/bin:$PATH"
codex --version
```

`export` adds the installer's command directory to this shell's PATH; it does
not reinstall anything or overwrite the PATH entries already present.
`codex --version` then verifies that the installed command executes and reports
its version. These commands have been provided as the next check; their result
remains **Pending**. A new terminal is another way to load the PATH entry that
the installer reported adding to `.bashrc`.

After version verification, complete the sign-in locally with:

```bash
codex login
```

The default ChatGPT sign-in flow opens a browser. Once that flow completes,
`codex login status` can verify the authentication mode without displaying the
credential file. Sign-in and status verification remain **Pending**. Start
`codex` from the chosen project directory after its contents are inspected.
Do not publish authentication files, login codes or tokens.

Sources: [official Codex CLI installation](https://learn.chatgpt.com/docs/codex/cli),
[official authentication procedure](https://learn.chatgpt.com/docs/auth),
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
