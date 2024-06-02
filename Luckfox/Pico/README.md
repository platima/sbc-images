Note that for "2024-05-04 Luckfox_RV1106_SPI_Alpine_Platima.zip" the login is pico/luckfox, and su/sudo currently do not work. It was built for Pico Max.

"2024-05-04 Luckfox_RV1103_SD_Ubuntu_Factory.zip" is the SD card image made with SoC Toolkit and converted to a .img to flash with Balena etcher. I forget what I version I built this for, but I'd also expect Pico Max.

"2024-06-02 Luckfox_Pico_Mini_SD_Ubuntu_wEth.zip" is a build of Ubuntu for Pico Mini (both A and B) for flashing to an SD card with SoC Toolkit. Instructions: [https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-SD-Card-burn-image](https://wiki.luckfox.com/Luckfox-Pico/Luckfox-Pico-SD-Card-burn-image)

I am trying to work out a fix, and raised https://github.com/LuckfoxTECH/luckfox-pico/issues/102 but for now have set the root user password as Luckfox too! 2024-06-02 Update: Worked out the fix, haven't been assed updating it yet.
