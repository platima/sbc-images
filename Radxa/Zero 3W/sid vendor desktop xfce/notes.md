## Overview
- Had to remove ghostscript-x from xfce packages. Ref https://forum.armbian.com/topic/33051-armbian-build-pr-remove-ghostscript-x-in-sid-due-to-abandonment/
- UI is very snappy and feels good to use, especially compared to official B6 image
- 5GHz wifi should be fixed by installing [radxa-firmware](https://github.com/radxa-pkg/radxa-firmware/releases/tag/0.2.20), but I've not tested thoroughly 
- VLC does not support RTSP so flatpak required
- glmark-x11 result of 249 (best yet compared to bookworm, and compared to 5.10 kernel and drivers)

## OpenGL Information
```
GL_VENDOR:      Mesa
GL_RENDERER:    Mali-G52 r1 (Panfrost)
GL_VERSION:     3.1 Mesa 24.0.4-1
```

## VLC (from flathub via flatpak)
- Still laggy as hell due to trying to use OpenGL, not GL ES

## Benchmarks
- Geekbench5: [148 single 467 multi](https://browser.geekbench.com/v5/cpu/22365656) ([Radxa release b6 results here](https://browser.geekbench.com/v5/cpu/22362662))
- Geekbench6: [187 single 489 multi](https://browser.geekbench.com/v6/cpu/5562832) ([Radxa release b6 results here](https://browser.geekbench.com/v6/cpu/5537554))
