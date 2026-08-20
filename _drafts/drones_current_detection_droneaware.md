



## Droneaware

Droneaware is designed to be more of an "ADSB feeder, but for drones" design. Its node setups use a raspberry pi and off the shelf wifi and bluetooth dongles, with a couple scripts that parse any scanned results, and feed them to both a local webserver and the shared [droneaware live map](https://droneaware.io/live.html), aggregating everyone's data.

![Screenshot of the droneaware live map. Most of the page is taken up with a map, zoomed in to show the Dallas metro area. There are orange and red triangles representing drones. The drones have small labels under them with the model of the drone. The left side is a sidebar showing more info about each detected drone, along with navigation buttons](/assets/drones_current_detection/screenshot_droneaware_live.png)

#### BLE 4 and 5

Droneaware uses Bleak for scanning, which on linux, uses BlueZ as the backend.

#### 5G Wifi

#### 2.4G Wifi

#### Parsing Remote ID protocols

### Setting up DroneAware

#### Verify wifi dongle
The internal wifi is used by both the ADSB and droneaware to talk to the internet, so I can't use that for scanning for drones. Instead, I need a wifi dongle that supports promiscuous and monitor mode on linux, allowing me to scan for any wifi packets flying through the air.


To verify it runs on linux, I plugged it into my linux laptop and ran `ifconfig` with and without wireless USB plugged in to get the interface name: `wlx9cefd5f644bd`

Then I verified it can work with monitor mode by resetting it to monitor mode via below:
```bash
$ sudo ifconfig wlx9cefd5f644bd down
$ sudo iwconfig wlx9cefd5f644bd mode monitored
$ sudo ifconfig wlx9cefd5f644bd up
```

```bash
sudo ifconfig wlx9cefd5f644bd down
sudo iw wlx9cefd5f644bd set monitor none
sudo ifconfig wlx9cefd5f644bd up

sudo iw dev wlx9cefd5f644bd set channel 6
```
Then ran wireshark and captured packets [here](/assets/drones/monitor_mode_panda.pcapng) to verify it was picking up everything.

Lastly, reset it back to the regular mode:
```bash
$ sudo ifconfig wlx9cefd5f644bd down
$ sudo iwconfig wlx9cefd5f644bd mode managed
$ sudo ifconfig wlx9cefd5f644bd up
```

or
```bash
sudo iw wlx9cefd5f644bd set type managed
``` 

#### Install onto ADSB server

setup root ssh on my adsb.im raspberry pi by going to the homepage of the feeder, then go to System -> Management. Click "Show Password" for it to generate a new root user password, save it, then accept. You can now remote into your raspberry pi if you're on the same network by doing the `ssh root@<your ip>` command, and typing in the root user password you saved earlier.

Once on your pi, you can run the install script:

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

> Note: you can see the release source code on github [https://github.com/fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) by downloading the zip of the source code. There you can see the python scripts that run the wifi and ble detection services. So you don't have to install things blindly here, if you don't want to


You can check if it finishes install and is running by using systemctl:
```bash
sudo systemctl status droneaware-wifi
sudo systemctl status droneaware-ble
```

There's also a `droneaware` command that gets installed, that has a few subcommands:
```
Commands:
  update       Download and install the latest firmware
  status       Show service status and firmware version
  logs         Tail live logs  (wifi by default, or: droneaware logs ble)
  test         Transmit a 60-second test flight and verify detection
  test --dry-run  Check rate-limit availability without transmitting
```


## Current detections

- droneaware - only detecting via beacon frames, up to about 1 mile out. There's been an occasional outlier at 2 miles, but it's often single pings and with weirdly high altitude readings, so it's unclear if those are faulty readings.


# References

Droneaware: [https://droneaware.io](https://droneaware.io)

Monitor mode wifi dongles: [https://www.acrylicwifi.com/en/wifi-analyzer/requirements-and-compatibility/](https://www.acrylicwifi.com/en/wifi-analyzer/requirements-and-compatibility/)

linux wifi dongles: [https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Adapters_that_are_supported_with_Linux_in-kernel_drivers.md#ac1200--ac1300---usb-3---24-ghz-and-5-ghz-wifi-5](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Adapters_that_are_supported_with_Linux_in-kernel_drivers.md#ac1200--ac1300---usb-3---24-ghz-and-5-ghz-wifi-5)


Setting up a flightaware raspberry pi with droneaware: [https://droneaware.io/flightaware.html](https://droneaware.io/flightaware.html)

Setting a wifi interface to monitor mode: [https://www.geeksforgeeks.org/linux-unix/how-to-put-wifi-interface-into-monitor-mode-in-linux/](https://www.geeksforgeeks.org/linux-unix/how-to-put-wifi-interface-into-monitor-mode-in-linux/)