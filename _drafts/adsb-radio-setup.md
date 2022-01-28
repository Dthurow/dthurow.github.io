download from: https://www.adsbexchange.com/how-to-feed/adsbx-custom-pi-image/

use md5sum to verify

```
danielle@danielle-z-series:~/Downloads/md5sum ./adsbx_buster.1.0.zip
danielle@danielle-z-series:~/Downloads/adsbx_buster.1.0$ md5sum ./adsbx-1.0.11.img 
```

use `dh -f` to get name of SD card (both partitions)
/dev/mmcblk0p1 
/dev/mmcblk0p2

unmounted both partitions from filesystem
`sudo umount /dev/mmcblk0`


do `dd` command to copy image over:

`sudo dd if=./adsbx-1.0.11.img of=/dev/mmcblk0 bs=1M status=progress`

use https://www.mapcoordinates.net/en to get lat/long

44.96798722
-93.26707465
256m

create wifi config:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

# set the 2 letter code for your country, for a list google "wifi country code"

country=US

# change my_wifi and my_password to the appropriate values
# make sure not to delete the quotes as some editors might replace them with slightly different characters that will cause the system to malfunction
# exactly how the quotes need to look like for reference: "my_wifi"

network={
 ssid="USI-FIBER-19FC_Guest"
 psk="IAmAGuestUser"
}
```

hunt for pi:
nmap -sn 192.168.68.0/24

Nmap scan report for 192.168.68.100
Host is up (0.0029s latency).
