## Overview
- UI is very snappy and feels good to use, especially compared to official B6 image
- Still seems to have issues with 5GHz networks, but WPA3 seems supported (possibly fixed by [radxa-firmware](https://github.com/radxa-pkg/radxa-firmware))
- VLC does not support RTSP so flatpak required

## VLC
- Has issues with libva unable to open DRI so gl fails when using OpenGL
- Both XVideo and X11 (XCB) is laggy as hell
- Compiling gl4es and copying libGL.so* to the app's lib directory results in no change (confirmed it was running)

## Benchmarks
- glmark2-x11 gave a score of
- Geekbench5: [144 single 459 multi](https://browser.geekbench.com/v5/cpu/22364872) ([Radxa release b6 results here](https://browser.geekbench.com/v5/cpu/22362662))
- Geekbench6: TBC [X single XX multi](https://browser.geekbench.com/v6/cpu/XXXX) ([Radxa release b6 results here](https://browser.geekbench.com/v6/cpu/5537554))
