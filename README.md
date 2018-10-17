# wake_up_light_interface

This repository is to set up a Flask service on Raspbian, controlling the Wake-Up-Light. Allowing setting timers, displaying the time and controlling LED functionality.

## Install necessaray python3 packages:
```sh
apt-get install ntpdate python-smbus
pip install WTForms
```
## Setup Crontab:
Create a new file at `/etc/cron.d/wake_up_light`

```
* * * * * www-data python3 /[repository path]/wake_up_light_interface/timer_cron.py
```

## Update time via ntp:
Update ntp to ensure a proper time base:

```sh
sudo /etc/init.d/ntp stop
sudo ntpd -q -g
sudo /etc/init.d/ntp start
```

## Run Webserver as non root
Install and configure authbind:
```sh
sudo apt install authbind
sudo touch /etc/authbind/byport/80
sudo chown www-data /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
```

Start as user:
```sh
authbind python3 app.py
```

or as (executable!) script `/etc/init.d/wake_up_light`:

    #!/bin/sh
    ### BEGIN INIT INFO
    # Provides:             door
    # Required-Start:       $start
    # Required-Stop:        $shutdown
    # Default-Start:        2 3 4 5
    # Default-Stop:
    # Short-Description:    wake up light
    ### END INIT INFO

    su www-data
    authbind python3 app.py

    exit 0
