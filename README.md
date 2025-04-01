# Table of Contents
1. [Radxa Images](#radxa)
2. [Luckfox Images](#luckfox)

# Radxa
## UPDATE
**2025-04-01**: Added new Zero 3 Debian Bookworm CLI and XFCE images using the latest `rsdk`

## Legacy Images:
At the time of writing (2024-04-01) the Radxa images for the Rock 3A and Zero 3W have a number of problems, namely;
 - Wifi needs 2.4GHz WPA2 to work
 - Locales and terminfo appear missing
 - GL is 3.1 Mesa 20.3.5 by Mesa
 - Based on Debian 11
 - Kernel is 5.10
 - Other annoyances like packages I want not there

So I built an Armbian build using the Zero 3 WIP file, and it worked really bloody well, thus I decided to share them. Using [RKDevTool v2.96](https://github.com/platima/sbc-images/blob/main/Radxa/RKDevTool_Release_v2.96_en.zip)  and [this loader](https://github.com/platima/sbc-images/blob/main/Radxa/Zero%203W/rk356x_spl_loader_ddr1056_v1.10.111.bin) worked a treat on both boards so far.

These are not perfect, and probably need fixes, but I like them. Starting with these Radxa images, I'm going to start adding all of my custom images here.

Packages I added:
 - libglx-mesa0
 - libgl1-mesa-dri
 - mesa-utils
 - mesa-utils-extra
 - vlc
 - glmark2-x11
 - net-tools
 - screen
 - vim
 - neofetch
 - chromium

# Luckfox

This repository contains SD card images for various configurations of the Luckfox Lyra development board, including both Buildroot and Ubuntu-based systems.

These are built from the downloads available at the time, and have matching filenames, but do not require special software to image the TF/SD card with.

## Available Images

### Lyra (Base Model)
- Buildroot-based:
  - `Luckfox_Lyra_MicroSD_241230.img.bz2`
  - `Luckfox_Lyra_MicroSD_241230.img.sha256`
- Ubuntu-based:
  - `Luckfox_Lyra_Ubuntu_MicroSD_241230.img.bz2`
  - `Luckfox_Lyra_Ubuntu_MicroSD_241230.img.sha256`

### Lyra Plus
- Buildroot-based:
  - `Luckfox_Lyra_Plus_MicroSD_241230.img.bz2`
  - `Luckfox_Lyra_Plus_MicroSD_241230.img.sha256`
- Ubuntu-based:
  - `Luckfox_Lyra_Plus_Ubuntu_MicroSD_241230.img.bz2`
  - `Luckfox_Lyra_Plus_Ubuntu_MicroSD_241230.img.sha256`

## Usage

1. Download the appropriate image for your Luckfox Lyra board
2. Verify the SHA256 checksum of the uncompressed image using the provided .sha256 file
3. Extract the .bz2 file
4. Flash the image to your microSD card

## Verification

To verify your download after extraction:
```bash
sha256sum -c Luckfox_Lyra_MicroSD_241230.img.sha256
```

## Image Details

- Buildroot images provide a minimal, fast-booting system optimized for embedded applications
- Ubuntu images offer a fuller glibc environment with additional packages and development tools

## Flashing Instructions
### Linux/macOS
```bunzip2 Luckfox_Lyra_MicroSD_241230.img.bz2
sudo dd if=Luckfox_Lyra_MicroSD_241230.img of=/dev/sdX bs=4M status=progress
```

Replace /dev/sdX with your SD card device (can be found using lsblk command).

### Windows
Use Balena Etcher.

## Warning
Always verify you're using the correct device path before flashing. Using the wrong device path can result in data loss.

## Expanding Root Partition

After flashing, you may want to expand the root partition to use the full SD card space. You can do this using the provided Python script:

```bash
# Download the expansion script
wget https://raw.githubusercontent.com/[your-repo]/expand_partition.py

# Make it executable
chmod +x expand_partition.py

# Run as root (replace mmcblk0 with your device)
sudo ./expand_partition.py /dev/mmcblk0

# Update kernel partition table
sudo partx -u /dev/mmcblk0

# Expand the filesystem
sudo resize2fs /dev/mmcblk0p3
```

Note: If you're running this on the Lyra board itself, the device will typically be /dev/mmcblk0. If you're preparing the card on a PC with a card reader, the device might be something like /dev/sdX.

## Safety Checks
Before running the expansion:
1. Verify your device path using lsblk
2. Ensure you have a backup of important data
3. Make sure you're expanding the correct partition (usually partition 3)
