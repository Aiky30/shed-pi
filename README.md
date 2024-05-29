# shed-pi

## Introduction

A package to run a Raspberry Pi in an outbuilding such as a garden shed, for the internet of sheds.

Automated use cases:

- Weather station
- Garden lighting
- Security

## Design Principles

The Hub contains a Protocol, and can utilise modules
A device contains a protocol, and can utilise modules

## TODO:

1. Fix: Bug: The script startup gets an incorrect time (Hasn't yet got the internet time)
2. Instructions on pinout

# TODO: General Integration test for the logger using a fake module

# TODO: Test default endpoint address settings work in theory, because the test above overrides them

# TODO: Device startup and shutdown needs a unit test

# TOOD: Temp probe should be a fixture

# TOOD: CPU temp probe should be a fixture

# TODO: Split the RPI and custom temp module, they will be standalone modules, New RPI module with it's own CPU temp component

### Wish list:

- Poetry (Not started)
- ASGI backend server (Daphne)
- Native webcomponent FE with Bootstrap
- pip install raspberry pi
- modular components that are easy to install from a software and hardware perspective
- Provide systemd script to 3rd parties
- venv is crucial before installing any third party packages!
- Pre commit config with ci integration

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
nano /lib/systemd/system/shed-pi.service
````

With the contents

```ini
[Unit]
Description = Shed-Pi
After = multi-user.target
StartLimitIntervalSec = 0

[Service]
Type = simple
ExecStart = /usr/bin/python3 /home/shed-pi/temp_logger.py
StandardInput = tty-force

[Install]
WantedBy = multi-user.target
```

Enable the service, (CAVEAT: didn't work when manually starting, works on reboot)

```shell
sudo systemctl daemon-reload
sudo systemctl enable shed-pi.service
sudo systemctl start shed-pi.service
sudo systemctl status shed-pi.service
```

Read the logs

```shell
tail -f /var/log/shed-pi.log
```

## Development

### Precommit

Install pre-commit: https://pre-commit.com/

Configure precommit on your local git for the project by running the following at the root of the project:

```shell
pre-commit install
```

Pre-commit will then automatically run for your changes at commit time.

To run the pre-commit config manually, run:

```shell
pre-commit run --all-files
```

## Release

Generate the release

```shell
pip install -q build
python -m build
twine upload dist/*
```
