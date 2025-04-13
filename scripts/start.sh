#!/bin/bash

# Copy the files to the RAM disk
#SOURCE_DIR="/home/syd/led-matrix"
#TARGET_DIR="/mnt/ram/led-matrix"

# Create the target directory
#mkdir -p "$TARGET_DIR"

# Copy the files
#cp -r "$SOURCE_DIR"/{.,}* "$TARGET_DIR"

# Run the Python script
#sudo /mnt/ram/led-matrix/.venv/bin/python /mnt/ram/led-matrix/src/main.py

sudo .venv/bin/python -m src.main
