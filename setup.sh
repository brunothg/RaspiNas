#!/bin/bash

rpi_update () {
	sudo apt update
	sudo apt full-upgrade
}

install_dependencies () {
	sudo apt -y install python3-gpiozero
}

activate_atx_powersupply () {
	local ATX_PIN=$1
	echo ""
	echo "activate atx powersupply with gpio $ATX_PIN"
	printf "\n#ATX Powersupply\ngpio=$ATX_PIN=op,dh" | sudo tee -a /boot/config.txt > /dev/null
}

rpi_update
install_dependencies

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
