## Platima's SBC images

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
