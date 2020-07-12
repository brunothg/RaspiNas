#!/bin/bash

# Check privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

mkdir -p /usr/local/bin/case-hardware-drivers/power-button
rm -R /usr/local/bin/case-hardware-drivers/power-button
mkdir -p /usr/local/bin/case-hardware-drivers/power-button
cp ./src/* /usr/local/bin/case-hardware-drivers/power-button/
chown -R root:root /usr/local/bin/case-hardware-drivers/power-button

mkdir -p /etc/case-hardware-drivers
cp ./power-button.json /etc/case-hardware-drivers/
chown root:root /etc/case-hardware-drivers/power-button.json

cp ./power-button.service /etc/systemd/system/case-hardware-drivers.power-button.service
chown root:root /etc/systemd/system/case-hardware-drivers.power-button.service
# systemctl enable case-hardware-drivers.power-button.service
# systemctl start case-hardware-drivers.power-button.service

echo "Edit /etc/case-hardware-drivers/power-button.json for configuration"
echo "After configuration you can enable the service: systemctl enable case-hardware-drivers.power-button.service"
