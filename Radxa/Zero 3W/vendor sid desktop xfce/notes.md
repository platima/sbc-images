## Overview
- Had to remove ghostscript-x from xfce packages. Ref https://forum.armbian.com/topic/33051-armbian-build-pr-remove-ghostscript-x-in-sid-due-to-abandonment/
- UI is very snappy and feels good to use, especially compared to official B6 image
- 5GHz wifi should be fixed by installing [radxa-firmware](https://github.com/radxa-pkg/radxa-firmware/releases/tag/0.2.20)) but I've not tested thoroughly 
- VLC does not support RTSP so flatpak required
- glmark-x11 result of 249 (best yet compared to bookworm, and compared to 5.10 kernel and drivers)

## VLC (from flathub via flatpak)
- TBC

## Benchmarks
- Geekbench5: [TBC](https://browser.geekbench.com/v5/cpu/XXX) ([Radxa release b6 results here](https://browser.geekbench.com/v5/cpu/22362662))
- Geekbench6: [TBC](https://browser.geekbench.com/v6/cpu/XXX) ([Radxa release b6 results here](https://browser.geekbench.com/v6/cpu/5537554))
