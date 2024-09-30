# Raspberry Pi device

TODO:

- Use a venv for the module
- Add the shed-pi module imports to the Python PATH
- Better placement of logs

## Installation

### Enable interfaces

For any temperature sensors the 1 wire interface is required

```shell
sudo raspi-config
```

1. Select the option: "Interface Options"

2. Select the Option I7: "1-Wire"

3. Agree to installing the 1-Wire script

4. Reboot

```shell
sudo reboot
```

Sanity check that the 1 Wire data is available:

```shell
ls /sys/bus/w1/devices/
```

Check the value read, be sure to change "28-000003ebbf13" to the values listed above:

```shell
cat  /sys/bus/w1/devices/28-000003ebbf13/w1_slave
```

### Script auto start with systemd

Create a file in systemd

```shell
nano /lib/systemd/system/shed-pi-rpi-device-modules.service
````

With the contents

```ini
[Unit]
Description = Shed-Pi Device Modules
After = multi-user.target
StartLimitIntervalSec = 0

[Service]
Type = simple
ExecStart = /usr/bin/python3 /home/shed-pi/standalone_modules/rpi/device_protocol.py
StandardInput = tty-force

[Install]
WantedBy = multi-user.target
```

Enable the service, (CAVEAT: didn't work when manually starting, works on reboot)

```shell
sudo systemctl daemon-reload
sudo systemctl enable shed-pi-rpi-device-modules.service
sudo systemctl start shed-pi-rpi-device-modules.service
sudo systemctl status shed-pi-rpi-device-modules.service
```

Read the logs

```shell
tail -f /var/log/shed-pi.log
```
