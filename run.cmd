@echo off
title Pychat 1.2
echo Please make sure you installed Python3 and Pip3!
echo Installing requirements.txt
pip3 install -r requirements.txt
echo Done!
python3 ./data/client.py
pause
cls
