#!/bin/bash

rpi_update () {
	apt update
	apt full-upgrade
}

install_dependencies () {
	apt -y install python3-gpiozero
	apt -y install python3-systemd
	apt -y install smartmontools
	apt -y install wget
}

activate_atx_powersupply () {
	local ATX_PIN=$1
	echo ""
	echo "activate atx powersupply with gpio $ATX_PIN"
	printf "\n# ATX Powersupply\ngpio=$ATX_PIN=op,dh" | sudo tee -a /boot/config.txt > /dev/null
}

disable_bluetooth () {
	printf "\n# Disable Bluetooth\ndtoverlay=disable-bt" | sudo tee -a /boot/config.txt > /dev/null
}

install_led_service() {
	cd ./case-hardware-drivers/leds
	./setup.sh
	cd ../../
}

install_firewall() {
	apt -y install ufw
	ufw allow ssh
	ufw enable
	ufw status
}

install_omv() {
	echo "Install OMV..."
	echo "You may need to press Enter (and enter your password), if nothing is going to happen"
	wget -O - https://github.com/OpenMediaVault-Plugin-Developers/installScript/raw/master/install | bash
}


# Check privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

rpi_update
install_dependencies


# Firewall
echo ""
read -p "Firewall installieren (UFW)? [y/n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
	install_firewall
fi


# Bluetooth
echo ""
read -p "Bluetooth sperren? [y/n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
	disable_bluetooth
fi


# ATX Powersupply
echo ""
read -p "ATX Powersupply GPIO installieren? [y/n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
	read -p "Welcher GPIO Pin soll genutzt werden? [17]" GPIO
	GPIO=${GPIO:-17}
	activate_atx_powersupply "$GPIO"
	unset GPIO
fi

# LED Service
echo ""
read -p "LED Service installieren? [y/n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
	install_led_service
fi

install_omv
