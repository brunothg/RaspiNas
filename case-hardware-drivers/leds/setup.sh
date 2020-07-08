#!/bin/bash

# Check privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

mkdir -p /usr/local/bin/case-hardware-drivers/leds
cp ./src/* /usr/local/bin/case-hardware-drivers/leds/
chown -R root:root /usr/local/bin/case-hardware-drivers/leds

mkdir -p /etc/case-hardware-drivers
cp ./leds.json /etc/case-hardware-drivers/
chown root:root /etc/case-hardware-drivers/leds.json

cp ./leds.service /etc/systemd/system/case-hardware-drivers.leds.service
chown root:root /etc/systemd/system/case-hardware-drivers.leds.service
systemctl enable case-hardware-drivers.leds.service
systemctl start case-hardware-drivers.leds.service
