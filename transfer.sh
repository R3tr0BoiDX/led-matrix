#/bin/bash

# Transfer files
rsync \
    -av \
    --delete \
    --exclude .git/ --exclude .mypy_cache/ --exclude .venv/ --exclude .vscode/ --exclude __pycache__/ \
    . \
    syd@barrett.local:/home/syd/led-matrix

# Run the script
ssh syd@barrett.local "\
    sudo pkill python &&\
    cd /home/syd/led-matrix &&\
    nohup sudo .venv/bin/python main.py &\
    "
