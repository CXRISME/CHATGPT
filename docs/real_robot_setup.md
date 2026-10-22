# Real TurtleBot3 Burger Setup

This is the evidence log for configuring the physical TurtleBot3 Burger for the
SLAM final-year project. In this project, the user's term "Pico Pi" means the
robot's **Raspberry Pi**, not a Raspberry Pi Pico microcontroller.

Required baseline: **Ubuntu 22.04 Server 64-bit (ARM64), ROS 2 Humble,
TurtleBot3 Burger**. The baseline is a requirement, not evidence of an installed
system. Do not substitute a different Ubuntu or ROS distribution silently.

## Current Status

**22 October 2026 — Steps 1–3 complete.** The PC and SD-card read-only audit is
complete. The owner identified the board as **Raspberry Pi 4 Model B** and
confirmed that the H: microSD card has no data requiring preservation.
The owner subsequently explicitly authorised overwriting the entire Disk 3
(H:, approximately 64 GB) with Ubuntu Server 22.04.5 64-bit.
**Step 2 image writing, readback verification and separate boot-seed inspection
have passed.** The owner selected an iPhone hotspot, entered credentials in a
local masked form, and its Wi-Fi seed passed separate file readback checks.
The owner visually traced the existing power cable from the OpenCR connector
labelled 5V/GND to Pi physical pins 4/6 respectively. This cable check is
complete; electrical measurements and load testing remain unperformed.
The owner has since reported power-on with the top LiDAR rotating and the wheels
and chassis stationary. Ubuntu first boot, cloud-init completion and key-based
SSH login have now been verified, with the SSH connection checked again on
22 October. Step 4's initial locale, timezone, clock and filesystem checks
passed; package updates remain pending. No robot firmware update, ROS 2
installation or motion test has been performed.

The owner subsequently selected the existing VirtualBox workstation guest.
Its terminal screenshot confirms Ubuntu 22.04.5 LTS and `x86_64`. See the
[Ubuntu VM handoff](ubuntu_vm_handoff.md) for verified state and the next
setup step. The guest's Codex CLI installer subsequently reported
version 0.163.0 installed successfully, and the owner's next screenshot verifies
`codex --version` returned `codex-cli 0.163.0`. The subsequent login-status
output confirms `Logged in using ChatGPT`. A project session, VM-to-Pi access
and guest ROS checks remain pending.

Each step will be completed and its actual output checked before the next step.
When a command fails, preserve its output and diagnose that failure before
considering a reinstall. Step 2 image preparation and write verification are
complete. First boot and SSH have passed; sensor, motion and SLAM runtime stages
remain **Pending / To be tested**.

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
| Windows OpenSSH client | Available | Key-based robot login subsequently verified in Step 3 |
| Raspberry Pi Imager | Installed, product version `v2.0.6` | Executable metadata inspected; no write started |
| Ubuntu/ROS workstation | Ubuntu VM OS subsequently identified | Ubuntu 22.04.5 LTS / x86_64 confirmed in the guest terminal; ROS installation and operation still pending inspection |

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
| 3 | Generic MassStorageClass, USB | 62,534,975,488 bytes | H: card identified; later write approval recorded in Step 2 |

For the H: device:

- Physical device path: `\\.\PhysicalDrive3` (use this exact spelling with Imager's CLI).
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
| Raspberry Pi | Raspberry Pi 4 Model B Rev 1.5; `free -h` reports 1.8 GiB RAM | Model initially identified by owner; model/revision and total reported memory subsequently read over SSH |
| microSD card | H: device identified above; no data requiring preservation | Owner confirmed no backup needed; printed brand/capacity not recorded |
| OpenCR control board | Exact board revision and installed firmware unknown | Pending label and later USB/firmware checks |
| Left and right DYNAMIXEL motors | Models, IDs and baud rate unknown | Pending labels and later communication checks |
| LiDAR | Owner reports continuous rotation after power-on; model and interface unknown | Rotation observed by owner only; label and actual scan data pending |
| Camera | Owner reports a camera module connected to a Pi USB 2 port; model unknown | Connection reported; detection and driver checks pending |
| Power and cabling | Owner reports an 11.1 V battery connected to OpenCR; visually traced its labelled 5V output to Pi physical pin 4 and GND to pin 6; Pi USB-C unconnected | Existing cable endpoints/polarity confirmed by owner; no meter or load test; board revision, battery condition and power stability pending |

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
- [x] Immediately before the approved write, re-read disk information and
  display the target physical disk, reader name, capacity, partitions and drive
  letter. Explain that imaging replaces the entire disk, including its partitions.
- [x] Obtain explicit owner confirmation for Disk 3 and the Ubuntu 22.04.5 image write.

Drive letters and disk numbers can change. The snapshot above is **not**
permission to select a different device later. Never target Disk 0 or Disk 1. No formatting,
partition deletion or image writing may occur before the write gate is satisfied.

## Step 2 — Approved Image Write and First-Boot Configuration

For a compatible Raspberry Pi, ROBOTIS's Humble SBC instructions specify
**Ubuntu Server 22.04.5 LTS (64-bit)**. The official Raspberry Pi preinstalled
server image is:

```text
ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz
```

The owner-confirmed Pi 4 Model B is compatible with this baseline.
Canonical's compatibility matrix lists 22.04 support for Pi 3B/3B+/4B, among
other models, but not Pi 5. A Pi 5 would require resolving the hardware/baseline
conflict before proceeding. SD write verification passed at this stage;
subsequent first-boot and SSH results are recorded in Step 3.

Sources: [ROBOTIS SBC setup, Humble section](https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/),
[Canonical Raspberry Pi compatibility](https://ubuntu.com/hardware/docs/boards/how-to/ubuntu_supported/raspberry-pi/),
[official Ubuntu 22.04 images](https://cdimages.ubuntu.com/ubuntu/releases/22.04/release/).

### Verified download result — 21 October 2026

The official compressed image and its published checksum list were downloaded
over HTTPS into `E:\ChatGPT\FYP\robot-images`, outside the GitHub checkout.
No raw disk was opened for writing during the download stage. The image binary
is not committed to Git.

| Item | Actual result |
| --- | --- |
| File | `ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz` |
| Downloaded size | `1,038,926,560` bytes, matching the server's Content-Length |
| SHA256 | `fd7687c5c9422a6c7ba4717c227bf6473fe4e0c954d5a9f664201dcecc63e822` |
| Official checksum comparison | **Passed**; exactly matches the image's entry in `SHA256SUMS` |
| Image written to SD | **Passed**; approved Disk 3, exact CLI device `\\.\PhysicalDrive3` |
| Imager readback verification | **Passed**; matching uncompressed-image hashes |
| First boot | Not tested during download/image writing; subsequently passed in Step 3 |

Sources: [image download](https://cdimages.ubuntu.com/ubuntu/releases/22.04/release/ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz)
and [published SHA256SUMS](https://cdimages.ubuntu.com/ubuntu/releases/22.04/release/SHA256SUMS).
This records a SHA256 comparison with the official HTTPS checksum list, not a
separate GPG-signature verification.

The download used `curl.exe --fail --location` with an ordinary output file:

```powershell
curl.exe --fail --location --output 'E:\ChatGPT\FYP\robot-images\ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz' 'https://cdimages.ubuntu.com/ubuntu/releases/22.04/release/ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz'
curl.exe --fail --location --output 'E:\ChatGPT\FYP\robot-images\SHA256SUMS' 'https://cdimages.ubuntu.com/ubuntu/releases/22.04/release/SHA256SUMS'
Get-FileHash -LiteralPath 'E:\ChatGPT\FYP\robot-images\ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz' -Algorithm SHA256
```

`curl.exe` downloads the image and checksum list; `--fail` rejects HTTP errors
and `--location` follows redirects. `Get-FileHash` reads the downloaded file and
calculates its SHA256. The actual hash was compared programmatically with the
single matching official entry; a mismatch would stop image preparation.
Do not rerun a download over an existing verified file unnecessarily.

A fresh read-only check after checksum verification still mapped H: to Disk 3,
USB, `62,534,975,488` bytes, with `IsBoot=False` and `IsSystem=False`.
The owner then approved that exact physical target. Disk, partition, image hash
and software version checks were repeated before the writer was started.

### Approved target and safeguards

The owner's confirmation covered **the entire Disk 3**, including replacement of
its partitions. Fresh preflights still found H: on that USB device, with the
same capacity, one exFAT partition, and no boot/system flags. C: and E: remained
on Disk 0. A local fixed-target guard rejected a simulated H:-to-Disk-0 mapping
in a read-only negative test. No write was performed by that test.

The actual CLI destination is `\\.\PhysicalDrive3`, matching Imager's enumerated
device spelling exactly. No system-drive override or verification-disabling
option is used. The `.xz` SHA256 was checked before writing; it is not passed
to Imager's `--sha256` option, which expects the decompressed image's hash in
this version.

### First-boot seed on the card — subsequently checked over SSH

The owner confirmed **GB / Europe/London**. The following seed configuration
was written to the SD card and inspected separately. Its initial file inspection
was not proof of a running system; subsequent runtime results are recorded here
and in Step 3 below:

| Setting | Prepared value | Runtime verification |
| --- | --- | --- |
| Username | `ubuntu` | Verified by `whoami` over SSH |
| Hostname | `tb3-burger` | Verified by `hostname` over SSH |
| Locale | `en_GB.UTF-8` | Verified by `locale` |
| Timezone | `Europe/London` | Verified by `timedatectl` |
| SSH | Dedicated Ed25519 public key; password authentication disabled in seed | Dedicated-key login passed; effective password policy not yet inspected |
| Local password | Locked initially; key-based SSH is the intended access method | No console-password login configured |
| Administrator access | `ubuntu` has sudo access for setup | `sudo -n true` passed |
| Ethernet | `eth0`, DHCP, optional interface | Prepared fallback; iPhone Wi-Fi selected for first boot |
| Wi-Fi | iPhone hotspot credentials stored privately; `wlan0`, DHCP, country GB | PC-to-Pi SSH via hotspot passed; effective regulatory domain not yet queried |

A dedicated key pair was created by Windows OpenSSH at
`C:\Users\LENOVO\.ssh\id_ed25519_tb3_burger` and its `.pub` companion. The private
key stays on the PC. Only the public key is included in the local cloud-init
seed. Actual seed files, keys and raw debug logs are kept outside the GitHub
checkout under the user's profile. No credentials or keys are committed.

The local `user-data` uses Ubuntu cloud-init to create the user, configure the
hostname, locale and timezone, authorise the public key, and enable the SSH
service on first boot. Updates are deferred until the network and SSH work.
At image-write completion, `network-config` enabled Ethernet DHCP only. Step 3
subsequently added the private iPhone Wi-Fi configuration before first boot.

The official image manifest lists cloud-init `24.2-0ubuntu1~22.04.1`, netplan.io
`0.106.1-7ubuntu0.22.04.4`, and openssh-server `1:8.9p1-3ubuntu0.10`.
These are image-manifest versions, not measured running-robot versions.

### Write method and evidence requirements

Imager 2.0.6 does not offer its customisation wizard for a local "Use Custom"
image by default. Its official CLI accepts cloud-init seed files directly.
The installed executable's Windows signature was valid, signed by Raspberry Pi
Limited. It was launched with Windows administrator elevation after the guards
passed; Windows security and execution-policy settings were not changed.

The operation uses these Imager arguments, with already-prepared local seed
files and the explicitly approved disk. This is an operation record, not a
portable disk selection command:

```powershell
$tb3ImagerArgs = @(
    '--cli', '--debug', '--disable-eject',
    '--log-file', 'C:\Users\LENOVO\.tb3-burger\imager-write-3.log',
    '--cloudinit-userdata', 'C:\Users\LENOVO\.tb3-burger\user-data',
    '--cloudinit-networkconfig', 'C:\Users\LENOVO\.tb3-burger\network-config',
    'E:\ChatGPT\FYP\robot-images\ubuntu-22.04.5-preinstalled-server-arm64+raspi.img.xz',
    '\\.\PhysicalDrive3'
)
Start-Process -FilePath 'C:\Program Files\Raspberry Pi Ltd\Imager\rpi-imager.exe' -ArgumentList $tb3ImagerArgs -Verb RunAs -WindowStyle Hidden -Wait -PassThru
```

`--cli` uses the command-line writer; the two `--cloudinit-*` arguments supply
Ubuntu first-boot settings. `--debug` retains diagnostic logging, and
`--disable-eject` leaves the card available for seed inspection. Readback
verification is enabled by default. `-Verb RunAs` requests Windows elevation;
the OS handles any administrator consent prompt. The writer is hidden because
it is a background CLI operation, and `-Wait` observes its exit.

Success requires actual write and readback evidence, a zero writer exit code,
the expected boot/Linux partition layout, and a separate check of the injected
seed files. Seed customisation occurs after image readback, so writer success
alone does not verify the seed contents or first boot. Reject any Windows
prompt to format the Linux partition.

Sources: [Imager 2.0.6 CLI](https://github.com/raspberrypi/rpi-imager/blob/v2.0.6/src/cli.cpp),
[current Imager customisation-format guidance](https://github.com/raspberrypi/rpi-imager/blob/main/doc/os_customisation_formats.md),
[Ubuntu first-boot seeds](https://ubuntu.com/hardware/docs/boards/how-to/special_hardware/headless-usage/),
[official image manifest](https://cdimages.ubuntu.com/ubuntu/releases/22.04/release/ubuntu-22.04.5-preinstalled-server-arm64+raspi.manifest).

### Completed write and post-write inspection — 21 October 2026

| Check | Observed result |
| --- | --- |
| Approved physical destination | Disk 3, `\\.\PhysicalDrive3`, USB reader, `62,534,975,488` bytes |
| Actual write | Completed; Imager reported `Write done in 106 seconds` |
| Uncompressed image write hash | `e4ac1280ee701f5a891b4a9c3ba98db736ea46e746ea2decf45c122da29197eb` |
| Device readback hash | Identical to the uncompressed image write hash |
| Verification time | `50.979` seconds |
| Writer completion | Exit code `0`, debug cycle reported `success: true` after real write/verification/customisation |
| Boot partition | Partition 1, H:, label `system-boot`, FAT32, `536,870,912` bytes, offset `1,048,576` |
| Second partition | Partition 2, `4,128,837,632` bytes, offset `537,919,488`; Windows reports `Unknown`, as expected for the image's Linux root partition |
| Boot files | `config.txt`, `cmdline.txt`, `vmlinuz`, `initrd.img`, Pi 4 device tree, and all three cloud-init seed files present |
| `user-data` readback | Matches the prepared seed after normalising line endings and duplicate `#cloud-config` header comments |
| SSH public key | Matches the dedicated PC public key; private key never copied to the SD card |
| `network-config` readback | At image-write completion, matched the Ethernet-DHCP-only seed; Wi-Fi added and checked separately in Step 3 |
| Running Ubuntu / SSH login | Not tested during image writing; subsequently passed in Step 3 |

The readback verifies the written image, not every byte of the nominal 64 GB
card. The Linux filesystem and its capacity after first-boot expansion were
subsequently checked on the Raspberry Pi in Step 4. No Windows formatting is required for the
second partition or remaining space.

These read-only Windows checks established the post-write partition layout:

```powershell
Get-Partition -DiskNumber 3 |
    Select-Object DiskNumber, PartitionNumber, DriveLetter, Type, Size, Offset
Get-Volume -DriveLetter H |
    Select-Object DriveLetter, FileSystemLabel, FileSystem, Size, HealthStatus
```

`Get-Partition` reports the two image partitions; `Get-Volume` confirms the
mounted FAT32 boot volume. Separate local comparisons checked the seed text and
public key without printing their contents. First-boot execution has not been
tested merely by inspecting these files.

The owner selected an iPhone hotspot. At the image-write stage, joining the same
hotspot and testing peer connectivity/SSH were still pending; they subsequently
passed the Step 3 checks. On an iPhone
that offers Maximise Compatibility, that mode provides 2.4 GHz / WPA2 Personal
for this initial connection. The Wi-Fi seed is now saved and checked, as recorded
below. See [Apple's hotspot compatibility explanation](https://support.apple.com/guide/security/wi-fi-security-with-apple-devices-secfd166f620/web).

If Ethernet is used as an alternative, the later sequence is to
safely eject the card, insert it with the Raspberry Pi powered off, connect the
Pi to the same router/LAN as the PC, then power it using a verified suitable
power arrangement. If Ethernet is unavailable, complete the private Wi-Fi seed
first. Do not infer a working Wi-Fi connection from a successful image write.

## Step 3 — First Boot and SSH Passed

The owner entered the hotspot name and password manually in a local masked
Tkinter form. Before changing `H:\network-config`, the helper checked pinned
fingerprints of the approved card's `meta-data` and `user-data`. It backed up
the earlier Ethernet-only seed outside the repository, saved the new UTF-8
configuration, flushed it, and compared the SD file with the local private copy.
The owner reported the save/readback success message; a separate local check
confirmed the file match, valid credential fields, networkd renderer, country GB,
and unchanged user/SSH metadata. Credential values were not printed or committed.

The following is a **sanitised example**, not the actual hotspot credentials:

```yaml
version: 2
renderer: networkd
ethernets:
  eth0:
    dhcp4: true
    optional: true
wifis:
  wlan0:
    dhcp4: true
    optional: true
    regulatory-domain: GB
    access-points:
      "<HOTSPOT_SSID>":
        password: "<HOTSPOT_PASSWORD>"
```

`dhcp4` requests an address from the hotspot. `optional` allows boot to finish
without waiting indefinitely for an absent interface. The access point entry
provides the private WPA/WPA2 credential, and `regulatory-domain` selects GB.
The image includes Netplan 0.106 and wpa_supplicant; the networkd backend supports
these settings. Cloud-init 24.2 passes this version-2 seed through to Netplan.

The local helper was opened with:

```powershell
Start-Process -FilePath 'C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\pythonw.exe' -ArgumentList 'C:\Users\LENOVO\.tb3-burger\wifi_setup.py' -WindowStyle Normal
```

This opens the local form for human credential entry. The helper and real
configuration stay outside the GitHub checkout. No screenshot or UI-text capture
was used to collect the credentials. Independent inspection printed boolean
results only, including `SDSeedReadbackPassed: true`, `CountryGB: true`, and
`OriginalUserAndMetadataUnchanged: true`.

**Acceptance:** private seed saved/read back, Raspberry Pi boot, PC-to-Pi
reachability through the selected hotspot and key-based SSH login — **Passed**.
The owner confirmed that the PC joined the configured iPhone hotspot; direct
SSH access from that interface succeeded.
Later package downloads will consume the hotspot's mobile data.

### Power-cable inspection — owner-confirmed endpoints

On 21 October 2026, the owner reported that the Pi's two USB 2 ports connect to
OpenCR and a camera module, its USB-C port has no cable, and OpenCR is connected
to an 11.1 V battery. The supplied images are reference diagrams, not evidence
of the actual board revision or wiring. The owner subsequently found a separate
power cable on the Pi header and confirmed its existing connections:

| Supply endpoint | Raspberry Pi endpoint | Evidence |
| --- | --- | --- |
| OpenCR connector labelled `5V` | Physical header pin 4, the 5 V rail | Owner visually traced the cable |
| OpenCR connector labelled `GND` | Physical header pin 6, ground | Owner visually traced the cable |

These are **physical header numbers**, not BCM GPIO4 and GPIO6. The existing
GPIO power path explains why USB-C is unconnected; an additional USB-C supply
is not needed for this first-boot attempt. No cable changes were requested.
The USB connection to OpenCR is separate from this power cable. Do not connect
the 11.1 V battery or an OpenCR 12 V output directly to the Pi or rely on USB
back-powering.

**Acceptance:** cable source label and endpoint polarity — **Confirmed by the
owner's visual inspection**. This is not a voltage measurement or load test.
OpenCR's exact board revision and installed firmware remain unknown. Power
stability under load and battery condition remain **Pending / To be tested**.
Actual Ubuntu boot subsequently passed the terminal checks below.
Identify the board before selecting any version-dependent firmware operation;
no firmware write has been performed.

Sources: [Raspberry Pi power requirements and USB back-powering](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#power-supply),
[Pi 4 official datasheet, GPIO connector pinout](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-datasheet.pdf),
[ROBOTIS separate SBC power-cable guidance](https://emanual.robotis.com/docs/en/platform/turtlebot3/compatible_devices/#power-supply).

### First-boot procedure and subsequent verification

1. Turn on the already-configured iPhone hotspot, enable Allow Others to Join
   and Maximise Compatibility if available, and keep its hotspot settings open
   while connecting. Keep the saved hotspot name and password unchanged. Connect
   the Windows PC to the same hotspot.
2. Safely eject the H: `system-boot` microSD card using Windows' removable-device
   controls. Wait for safe-removal confirmation before removing it. If Windows
   reports that the card is in use, resolve that before unplugging the reader.
3. With the robot and Pi powered off, insert the card into the Pi's microSD slot.
   Retain the confirmed existing GPIO power cable and leave USB-C unconnected.
4. Place the robot on a clear, level floor, keep its power switch accessible,
   and turn on the existing OpenCR power switch. Do not press motor-test buttons
   or run any movement command.
5. Allow about five minutes for initial boot and cloud-init; do not interrupt
   an active first boot. Report the Pi's power/activity LEDs and any visible
   errors before proceeding to network discovery and SSH.

The sequence above was issued before first boot. The owner's later LED report
and LiDAR rotation were supporting observations only; the terminal checks below
established actual Ubuntu boot and SSH. Safe-ejection timing was not separately
observed by the assistant. A lit power LED or an extra hotspot client alone
does not prove that Ubuntu, cloud-init or SSH succeeded.

Sources: [Ubuntu Raspberry Pi first boot and cloud-init](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#4-boot-ubuntu-server),
[Apple Personal Hotspot connection procedure](https://support.apple.com/en-gb/111785).

### Power-on observation — partial evidence only

On 21 October 2026, the owner reported that the top LiDAR keeps rotating after
power-on and confirmed that the wheels and chassis remain stationary. No speed,
scan quality, motor response or ROS topic was measured. The LiDAR model is still
unknown; no driver has been selected from this observation.

Continuous rotation alone is not a fault diagnosis or a passed sensor test.
For example, ROBOTIS documents that updated LDS-01 firmware runs the sensor
directly on power-on. This is background information, not identification of
this robot's LiDAR. See the [official LDS-01 power-on note](https://emanual.robotis.com/docs/en/platform/turtlebot3/appendix_lds_01/).

The owner later reported a lit red Pi LED, a flashing green LED and that the PC
was connected to the same iPhone hotspot. Exact boot elapsed time and LED flash
pattern were not recorded. LiDAR rotation itself does not verify Ubuntu boot,
cloud-init completion, ROS 2 installation or `/scan` publication.

### Verified SSH access — 21 October; checked again 22 October 2026

Read-only Windows checks identified the active WLAN IPv4 subnet and gateway.
Name lookups for `tb3-burger.local` and `tb3-burger` did not resolve. Discovery
was then limited to TCP port 22 on the directly connected hotspot subnet,
excluding the PC and gateway. No VPN subnet was probed or disabled. One device
returned an Ubuntu OpenSSH banner. The dedicated key successfully authenticated
as `ubuntu`; commands then verified the expected hostname, OS and board.
Actual addresses and MAC addresses are omitted from this public log.

The first connection used OpenSSH `StrictHostKeyChecking=accept-new` with a
dedicated local known-hosts file. Subsequent connections require the recorded
host key (`StrictHostKeyChecking=yes`); host-key checking was not disabled.
The local Windows SSH config at `C:\Users\LENOVO\.ssh\config` did not exist,
so a new `Host tb3-burger` entry was created without overwriting other entries.
It selects the current privately recorded IP, user `ubuntu`, the dedicated
identity, `IdentitiesOnly=yes`, and the dedicated known-hosts file. The real
host config and key remain outside the repository.

On this configured Windows PC, open PowerShell and run:

```powershell
ssh tb3-burger
```

This opens an interactive shell on the Pi using the tested alias and key. A
shell prompt normally appears as `ubuntu@tb3-burger:~$` once logged in. That
prompt is an example; the checks below identify the remote system directly.
Commands entered there execute on the Pi, not on Windows.

```bash
hostname
whoami
uname -m
cat /etc/os-release
cloud-init status
```

`hostname` identifies the remote machine; `whoami` identifies the account;
`uname -m` checks architecture; `/etc/os-release` identifies Ubuntu; and
`cloud-init status` checks completion of first-boot configuration. The actual
sanitised results were:

| Check | Verified result |
| --- | --- |
| Remote hostname | `tb3-burger` |
| Remote user | `ubuntu` |
| Ubuntu | `Ubuntu 22.04.5 LTS`, Jammy |
| Architecture | `aarch64` (64-bit ARM) |
| `/proc/device-tree/model` | `Raspberry Pi 4 Model B Rev 1.5` |
| First-boot status | `status: done` |
| Repeat SSH check on 22 October | Exit code `0`; same hostname, user, architecture, Ubuntu and cloud-init result |
| SSH shortcut check | `ssh -o BatchMode=yes tb3-burger 'hostname; whoami'` returned the expected hostname and user |

To end an interactive session and return to PowerShell:

```bash
exit
```

The alias uses a DHCP-assigned address. If the hotspot or lease changes,
re-identify the Pi and update the local alias; do not assume the old IP is still
correct or erase a changed host-key warning without investigation. Name lookup
failure was bypassed with the verified IP; no mDNS service was installed.
SSH provides terminal administration. Camera viewing, ROS remote operation and
wheel teleoperation have not been configured or tested yet.

## Step 4 — Ubuntu Baseline Checks Passed; Updates Pending

The following read-only checks and sudo check were run over the verified SSH
connection on 21 October 2026:

```bash
locale
timedatectl
uname -r
df -h / /boot/firmware
free -h
systemctl is-active ssh
sudo -n true
```

`locale` checks the UTF-8 environment. `timedatectl` checks timezone and clock
synchronisation. `uname -r` records the running kernel. `df` checks filesystem
capacity after first-boot expansion; `free` reports memory. `systemctl` checks
the SSH service, and `sudo -n true` verifies administrator access without a
password prompt or a system change.

| Check | Actual result |
| --- | --- |
| Locale | `LANG=en_GB.UTF-8`; reported LC categories use `en_GB.UTF-8` |
| Timezone | `Europe/London`, BST at inspection |
| System clock | Synchronised: `yes`; NTP service: `active` |
| Kernel | `5.15.0-1061-raspi` |
| Root filesystem | `/dev/mmcblk0p2`, `57G` total, `2.6G` used, `52G` available |
| Boot filesystem | `/dev/mmcblk0p1`, `505M` total, `68M` used, `437M` available |
| Memory | `1.8Gi` total reported; no swap configured |
| SSH service | `active` |
| Administrator access | `sudo -n true` exited successfully |

The expanded root filesystem confirms that the image's initial small Linux
partition now uses the card's available capacity. These values are a dated
snapshot, not a storage benchmark or a power-load test. System package updates,
post-update checks and any required reboot are **Pending**; ROS 2 installation
has not started. The next installation step will update Ubuntu within 22.04,
then check its actual output before proceeding to Humble.

References: [cloud-init 24.2 Netplan passthrough](https://docs.cloud-init.io/en/24.2/reference/network-config-format-v2.html#netplan-passthrough),
[Netplan 0.106 Wi-Fi settings](https://netplan.readthedocs.io/en/0.106/netplan-yaml/#properties-for-device-type-wifis).

## Configuration Record — Runtime Verification Pending

| Setting | Planned requirement / value | Actual result |
| --- | --- | --- |
| Ubuntu | Server 22.04, ARM64 | Verified 22.04.5 LTS, `aarch64`, over SSH |
| Image filename, source and checksum | Official Pi ARM64 Server 22.04.5 image | Downloaded; SHA256 comparison passed above |
| Username and hostname | `ubuntu` / `tb3-burger` | Verified over SSH |
| Wi-Fi | Country GB seed; iPhone credentials entered locally | Hotspot peer connectivity verified by SSH; regulatory-domain runtime query pending |
| SSH | Dedicated PC key and public-key first-boot seed prepared | Remote login and Windows alias passed; host key retained locally |
| Locale | `en_GB.UTF-8` | Verified over SSH |
| Timezone and clock sync | `Europe/London` confirmed | Timezone, active NTP and synchronised clock verified |
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
| 2 | Image preparation and approved write | Compatible board, verified image, explicit disk approval, successful write verification | Passed; boot seeds checked separately |
| 3 | Ubuntu first boot, network and SSH | Board/OS/architecture output and successful remote login from this PC | Passed; repeat SSH and shortcut checks passed on 22 October |
| 4 | Ubuntu baseline | Updates, username, hostname, UTF-8 locale, timezone and clock sync verified | Initial baseline checks passed; package updates and post-update checks pending |
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
| Card initially exposed one exFAT partition | Model, backup needs and exact-disk approval confirmed; image written and verified | Resolved |
| Raspberry Pi and peripheral versions cannot be established from the card | Owner identified Pi 4 Model B; peripheral labels/firmware remain to be checked | Pi model resolved; peripherals pending |
| Windows PowerShell 5 rejected a local helper script under its execution policy | Confirmed in a read-only validation run; used the installed Imager CLI directly with guards in the existing PowerShell host | Resolved without changing execution policy |
| Imager showed "already running" instead of starting the CLI write | Owner closed the startup dialog and idle wizard; checked no instance remained before a fresh invocation | Resolved; startup exit zero was not counted as a write |
| Uppercase `PHYSICALDRIVE3` did not match Imager's enumerated `PhysicalDrive3` | Inspected debug enumeration and unchanged exFAT layout; corrected spelling while retaining Disk 3 and all guards | Resolved before any write |
| USB write latency increased with the initial queue depth | Imager automatically reduced the queue depth from 128 to 2; writing and matching readback completed | Resolved by the writer's built-in recovery |
| Windows initially showed a stale full-disk FAT16 view after the raw write | Fresh storage queries subsequently showed the correct FAT32 boot and Linux image partitions; seed inspection then passed | Resolved without reformatting or rewriting |
| Pi hostname did not resolve on the hotspot | Discovered SSH only within the observed WLAN subnet, then authenticated with the dedicated key and verified the hostname; created a tested local SSH alias | Direct IP and alias work; mDNS not configured |

Actual terminal output now verifies Ubuntu boot, completed cloud-init and SSH.
The LiDAR rotation report remains a physical observation, not a ROS sensor
test. Add actual installation/runtime errors, diagnoses and verified resolutions
here as they occur.

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
