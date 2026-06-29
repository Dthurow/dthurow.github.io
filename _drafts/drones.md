

skydio x10

Operation frequency 	Connect SL: 2400-2483.5MHz
5150-5850Mhz

Connect 5G: 600-960MHz, 1700-2200MHz
Transmitter power (EIRP)	Connect SL: 34.3dBmi (2.4GHZ)
Connect SL: 33.7dBmi (5GHZ)

Connect 5G: 20dBmi


An inexpensive fpv drone might have an analog video transmitter at 5.8 and on a control link at 2.4 on the elrs protocol (frequency hopping based on LoRa). Tracking 5.8 would tell you where the drone is and should be straightforward to decode. Tracking 2.4 would tell you where the operator is. Drones like dji use proprietary protocols. 

# Remote ID

uses opendrone ID

## Wifi

Wifi NAN discovery frames

Category ID 0x4

wifi MAC header: 
Subtype 8 for Beacon Remote ID **OR**
Subtype 13 for Wi-Fi NAN Remote ID
    In Droneaware: 
        after detects subtype 13, detects if frame is 4 (public)
        then if the Wifi Alliance OUI ([0x50, 0x6F, 0x9A]) and the type 0x13 are set
        it then verifies the Service ID is 6 bytes of a sha of "org.opendroneid.remoteid"

> **NOTE** when parsing the packet, it will be offset by 4 bits, so potentially want to check 0x80 and 0xD0, respectively, depending on how you're parsing it (or remember to do `>>4`)

WiFi alliance OUI is:
[0x50, 0x6F, 0x9A]

```c
    /* Neighbor Awareness Networking Specification v3.0 in section 2.8.1
     * NAN Network ID calls for the destination mac to be 51-6F-9A-01-00-00 */
    uint8_t target_addr[6] = { 0x51, 0x6F, 0x9A, 0x01, 0x00, 0x00 };
```


Service ID is 6 bytes of a sha of "org.opendroneid.remoteid"
```python
>>> blah = hashlib.sha256(b"org.opendroneid.remoteid").digest()[:6]
>>> print(", ".join(hex(b) for b in blah))
0x88, 0x69, 0x19, 0x9d, 0x92, 0x9
```


Beacon 

```
Walk 802.11 beacon Information Elements looking for the vendor-specific
    ASTM F3411 Remote ID payload (OUI FA:0B:BC, type 0x0D).

    Beacon frame body layout (after 24-byte MAC header):
      Fixed parameters: 8 (timestamp) + 2 (beacon interval) + 2 (capability) = 12 bytes
      Then: IE chain — tag(1) + length(1) + value(length)
```

Vendor Specific IE 0xDD (221d)
Vendor specific OUI [0xFA, 0x0B, 0xBC]

## Droneaware

### Verify wifi dongle
The internal wifi is used by both the ADSB and droneaware to talk to the internet, so I can't use that for scanning for drones. Instead, I need a wifi dongle that supports promiscuous and monitor mode on linux, allowing me to scan for any wifi packets flying through the air.


To verify it runs on linux, I plugged it into my linux laptop and ran `ifconfig` with and without wireless USB plugged in to get the interface name: `wlx9cefd5f644bd`

Then I verified it can work with monitor mode by resetting it to monitor mode via below:
```bash
$ sudo ifconfig wlx9cefd5f644bd down
$ sudo iwconfig wlx9cefd5f644bd mode monitored
$ sudo ifconfig wlx9cefd5f644bd up
```

Then ran wireshark and captured packets [here](/assets/drones/monitor_mode_panda.pcapng) to verify it was picking up everything.

Lastly, reset it back to the regular mode:
```bash
$ sudo ifconfig wlx9cefd5f644bd down
$ sudo iwconfig wlx9cefd5f644bd mode managed
$ sudo ifconfig wlx9cefd5f644bd up
```





### Install onto ADSB server

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

### Current detections

- only detecting via beacon frames, no NANs so far...



# References

Supported phones: [https://github.com/opendroneid/receiver-android/blob/master/supported-smartphones.md](https://github.com/opendroneid/receiver-android/blob/master/supported-smartphones.md)

Monitor mode wifi dongles: [https://www.acrylicwifi.com/en/wifi-analyzer/requirements-and-compatibility/](https://www.acrylicwifi.com/en/wifi-analyzer/requirements-and-compatibility/)

linux wifi dongles: [https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Adapters_that_are_supported_with_Linux_in-kernel_drivers.md#ac1200--ac1300---usb-3---24-ghz-and-5-ghz-wifi-5](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Adapters_that_are_supported_with_Linux_in-kernel_drivers.md#ac1200--ac1300---usb-3---24-ghz-and-5-ghz-wifi-5)

ASTM F3411 Wi-Fi Beacon protocol doc [https://thedroneprofessor.com/wp-content/uploads/2022/11/F3411.40165-UAS-Remote-ID.pdf](https://thedroneprofessor.com/wp-content/uploads/2022/11/F3411.40165-UAS-Remote-ID.pdf)

Setting up a flightaware raspberry pi with droneaware: [https://droneaware.io/flightaware.html](https://droneaware.io/flightaware.html)

Setting a wifi interface to monitor mode: [https://www.geeksforgeeks.org/linux-unix/how-to-put-wifi-interface-into-monitor-mode-in-linux/](https://www.geeksforgeeks.org/linux-unix/how-to-put-wifi-interface-into-monitor-mode-in-linux/)

Wireshark dissector of drone IDs [https://github.com/opendroneid/wireshark-dissector/tree/main](https://github.com/opendroneid/wireshark-dissector/tree/main)