# Stair Challenge

On an RPi 4 you must set a fixed frequency to avoid the idle CPU scaling changing the SPI frequency and breaking the ws281x timings:

Do this by adding the following lines to /boot/config.txt and reboot:

```txt
core_freq=500
core_freq_min=500
```

SPI requires you to be in the `gpio` group if you wish to control your LEDs
without root.

## Get Started


## Development

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.11+
- [Poetry][poetry-install]


1. Create an `.env` and make an symbolik link
```bash
cp ./app/.env.example ./app/.env
ln -s app/.env .env
```

2. Fillout the database credentials (if needed) in the `.env` file
3. Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

Setup the pre-commit check, you must run this inside the virtual environment:

```bash
pre-commit install
```

*Now you're all set to get started!*

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

## FAQ

### Temporary failure in name resolution

`socket.gaierror: [Errno -3] Temporary failure in name resolution`

This error may indicate that the IP address of your MQTT server is incorrect.

<!-- Remove below this -->

### Docker

https://linux.how2shout.com/how-to-start-docker-container-automatically-on-boot-in-linux/
