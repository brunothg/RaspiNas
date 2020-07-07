#!/bin/bash

rpi_update () {
	sudo apt update
	sudo apt full-upgrade
}

install_dependencies () {
	sudo apt -y install python3-gpiozero
}


rpi_update
install_dependencies
