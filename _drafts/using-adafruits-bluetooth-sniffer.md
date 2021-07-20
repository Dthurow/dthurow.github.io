---
layout: post
title: Bluetooth Low Energy and Reversing a "smart" light
categories:
- technical write up
- side project
- How-to
- reverse engineering
tags:
- side project
- teardown
- embedded
status: publish
type: post
published: true
toc: true
---



### The Plan

### Intro to Bluetooth Low Energy

### Setting up the Sniffer

### Analyzing Packets

### Hypothesis and Testing


downloaded extcap folder from adafruit: https://learn.adafruit.com/introducing-the-adafruit-bluefruit-le-sniffer/using-with-sniffer-v2

copied into my extcap folder for wireshark, at /usr/lib/x86_64-linux-gnu/wireshark/extcap

ran python --version to make sure it was 2.7
ran sudo pip2 install pyserial to get rid of serial error

get "No arguments given!" which indicates it's running right

closed wireshark, plugged in sniffer, opened wireshark, found nrf sniffer

double clicked to run, got error: "Couldn't run /usr/bin/dumpcap in child process: Permission denied"

ran `sudo usermod -a -G wireshark danielle` logged off and then logged on again, now it works



Used nordic smartphone app (https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en), got LED info:
Name: LEDBlue-8B109BEB 
Address: 50:33:8B:10:9B:EB
RSSI: -46
Last advertisement packet:
Raw data: 0x0201060702F0FFE5FFE0FF12094C4544426C75652D384231303942454220051210001400020A04


It has the following UID Unknown services
0000fff0-0000-1000-8000-00805f9b34fb
0000ffe5-0000-1000-8000-00805f9b34fb
0000ffe0-0000-1000-8000-00805f9b34fb

https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_sniffer_ble%2FUG%2Fsniffer_ble%2Fsniffer_usage.html


General bluetooth low energy info:
https://www.bluetooth.com/bluetooth-resources/bluetooth-le-developer-starter-kit/
https://www.bluetooth.com/specifications/specs/