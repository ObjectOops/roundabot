# roundabot
The most roundabout means of programming a robot.

---

```
Hotspot commands.

systemctl status NetworkManager
systemctl start NetworkManager
sudo nmcli device wifi hotspot ssid <hotspot name> password <hotspot password> ifname wlan0

sudo nmcli connection modify <connection UUID from `nmcli connection`> connection.autoconnect yes connection.autoconnect-priority 100

For the command above, the defaults are "no" and "0", respectively.
```

---

```
Enabled the NetWorkManager service with `systemctl enable NetworkManager`.

Added openvscode-server autosart via. `crontab -e`.

Changed IPv6 Ethernet configuration to the brick to be "Link-Local Only".
Network thing in top right > Advanced Options > Edit Connections > [choose correct wired connection] > cog > IPv6 Settings > Method --> Link-Local Only.

That menu can also be used to change the hotspot settings.
```

---

```
PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
NAME="Raspbian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"

OpenVsCode Server
Version: 1.87.0
Commit: e3760f6c200e00bb2e549e76e533a349aeb014d3
Date: 2024-03-05T20:00:04.549Z
Browser: Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36

Name: ev3dev-browser
Id: ev3dev.ev3dev-browser
Description: Browse for ev3dev devices
Version: 1.2.1
Publisher: ev3dev
VS Marketplace Link: https://open-vsx.org/vscode/item?itemName=ev3dev.ev3dev-browser

https://github.com/gitpod-io/openvscode-server
https://www.ev3dev.org/
https://pybricks.com/ev3-micropython/
https://www.raspberrypi.com/tutorials/host-a-hotel-wifi-hotspot/
https://open-vsx.org/
```
