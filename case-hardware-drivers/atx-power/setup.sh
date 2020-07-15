#!/bin/bash

# Check privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

mkdir -p /usr/local/bin/case-hardware-drivers/atx-power
rm -R /usr/local/bin/case-hardware-drivers/atx-power
mkdir -p /usr/local/bin/case-hardware-drivers/atx-power
cp ./src/* /usr/local/bin/case-hardware-drivers/atx-power/
chown -R root:root /usr/local/bin/case-hardware-drivers/atx-power

mkdir -p /etc/case-hardware-drivers
cp ./atx-power.json /etc/case-hardware-drivers/
chown root:root /etc/case-hardware-drivers/atx-power.json

cp ./atx-power.service /etc/systemd/system/case-hardware-drivers.atx-power.service
chown root:root /etc/systemd/system/case-hardware-drivers.atx-power.service
# systemctl enable case-hardware-drivers.atx-power.service
# systemctl start case-hardware-drivers.atx-power.service

echo "Edit /etc/case-hardware-drivers/atx-power.json for configuration"
echo "After configuration you can enable the service: systemctl enable case-hardware-drivers.atx-power.service"
