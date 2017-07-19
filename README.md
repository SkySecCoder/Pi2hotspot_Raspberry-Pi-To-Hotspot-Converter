# Pi2hotspot_Raspberry-Pi-To-Hotspot-Converter
Easily convert your Raspberry Pi to a hotspot or access point to increase the wireless range in your area or for hacking purposes.

# Installation
```
$ git clone https://github.com/SkySecCoder/Pi2hotspot_Raspberry-Pi-To-Hotspot-Converter.git
```
# Usage
```
To install necessary packages and files in order to get started:
$ python Pi2Hotspot.py -i
$ python Pi2Hotspot.py -r

Usage: usage Pi2Hotspot.py [-i] [-r] [-s] [-u <ssid>] [-p <password_for_hotspot>]
```
Options:
  -h, --help   show this help message and exit
  -i           Install mode will modify and download necessary files
  -r           Run mode starts the hotspot
  -s           Stop mode stops the hotspot
  -u SSID      Specify SSID
  -p PASSWORD  Specify password for hotspot
```
# Security
```
By default the hotspot created will be WPA2 CCMP