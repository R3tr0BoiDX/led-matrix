#!/bin/bash

# Update the system
sudo apt update && sudo apt upgrade -y

# Install the required system packages
sudo apt install -y python3 python3-pip python3-venv tmux libjpeg-dev zlib1g-dev

# Create a virtual environment and install the required packages
python -m venv .venv
source .venv/bin/activate

# Upgrade pip and setuptools
python3 -m pip install --upgrade pip setuptools

# Install the required packages
pip install -r requirements.txt

# Create RAM disk
# sudo mkdir -p /mnt/ram

# Add the following line to /etc/fstab
# echo "tmpfs /mnt/ram tmpfs nodev,nosuid,size=1G 0 0" | sudo tee -a /etc/fstab

# Create systemd service
sudo cp led-matrix.service /etc/systemd/system/

# Enable and start the service
sudo systemctl enable led-matrix
sudo systemctl start led-matrix

# Reboot the system
sudo reboot
