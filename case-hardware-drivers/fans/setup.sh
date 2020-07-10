#!/bin/bash

# Check privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

mkdir -p /usr/local/bin/case-hardware-drivers/fans
rm -R /usr/local/bin/case-hardware-drivers/fans
mkdir -p /usr/local/bin/case-hardware-drivers/fans
cp ./src/* /usr/local/bin/case-hardware-drivers/fans/
chown -R root:root /usr/local/bin/case-hardware-drivers/fans

mkdir -p /etc/case-hardware-drivers
cp ./fans.json /etc/case-hardware-drivers/
chown root:root /etc/case-hardware-drivers/fans.json

cp ./fans.service /etc/systemd/system/case-hardware-drivers.fans.service
chown root:root /etc/systemd/system/case-hardware-drivers.fans.service
# systemctl enable case-hardware-drivers.fans.service
# systemctl start case-hardware-drivers.fans.service

echo "Edit /etc/case-hardware-drivers/fans.json for configuration"
echo "After configuration you can enable the service: systemctl enable case-hardware-drivers.fans.service"
