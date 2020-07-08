#!/bin/bash

rpi_update () {
	apt update
	apt full-upgrade
}

install_dependencies () {
	apt -y install python3-gpiozero
	apt -y install python3-systemd
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



# Check privileges
if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

rpi_update
install_dependencies


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
