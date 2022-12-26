@echo off
title Pychat 1.2
echo Please make sure you installed Python and Pip!
echo Installing requirements.txt
pip3 install -r requirements.txt
echo Done!
python3 ./data/client.py
pause
cls