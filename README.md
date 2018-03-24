# wake_up_light_interface

This repository is to set up a Flask service on Raspbian, controlling the Wake-Up-Light. Allowing setting timers, displaying the time and controlling LED functionality.

## Install necessaray python packages:
apt-get install smbus

pip install WTForms

## Setup Crontab:
Add following line to crontab (using crontab -e)

python /[repository path]/wake_up_light_interface/timer_cron.py
