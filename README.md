# wake_up_light_interface

This repository is to set up a Flask service on Raspbian, controlling the Wake-Up-Light. Allowing setting timers, displaying the time and controlling LED functionality.

## Install necessaray python3 packages:
```
apt-get install ntpdate python-smbus
pip install WTForms
```
## Setup Crontab:
Add following line to crontab (using crontab -e)

```
* * * * * python /[repository path]/wake_up_light_interface/timer_cron.py
```

## Setup Crontab:
Update ntp to ensure a proper time base:

```
sudo /etc/init.d/ntp stop
sudo ntpd -q -g
sudo /etc/init.d/ntp start
```
