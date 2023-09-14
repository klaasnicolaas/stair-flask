## Stair Challenge

On an RPi 4 you must set a fixed frequency to avoid the idle CPU scaling changing the SPI frequency and breaking the ws281x timings:

Do this by adding the following lines to /boot/config.txt and reboot:

```txt
core_freq=500
core_freq_min=500
```

SPI requires you to be in the `gpio` group if you wish to control your LEDs
without root.


### Docker

https://linux.how2shout.com/how-to-start-docker-container-automatically-on-boot-in-linux/