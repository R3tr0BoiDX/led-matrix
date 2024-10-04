#/bin/bash

# Transfer files
rsync -avz --exclude .git/ --exclude .mypy_cache/ --exclude .venv/ --exclude .vscode/ --exclude __pycache__/ . syd@barrett.local:/home/syd/led-matrix

# Run the script
ssh syd@barrett.local "sudo /home/syd/led-matrix/.venv/bin/python /home/syd/led-matrix/main.py"
