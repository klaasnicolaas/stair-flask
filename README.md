<!-- PROJECT SHIELDS -->
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]

[![Build Status][build-shield]][build-url]
[![Code Coverage][codecov-shield]][codecov-url]

# Stair Challenge

In this repository you will find the code for the overall operation of the Stair Challenge, a project by [Basalt][basalt] - Smartlab and designed to allow rehabilitation patients to practice climbing stairs in a fun and interactive way. Made by [klaasnicolaas](https://github.com/klaasnicolaas).

## Get Started

For this project you need at least a Raspberry Pi 4 with at least 4GB of RAM. All services are able to run in Docker containers, we are talking about an MQTT Broker from EMQX, MySQL database and the Flask application itself.

### Prerequisites

You must set a fixed frequency on the Raspberry Pi, to avoid the idle CPU scaling changing the SPI frequency and breaking the ws281x timings:

Do this by adding the following lines to `/boot/config.txt` and reboot:

```txt
core_freq=500
core_freq_min=500
```

SPI requires you to be in the `gpio` group if you wish to control your LEDs without root.

### Starting the services

To start the services, you can use the `docker-compose.yml` file in the root of the project. This file contains all the services needed to run the application.

```bash
docker-compose up -d
```

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

### Starting the application

To start the application in development mode, you can use the default Flask CLI command:

```bash
flask run
```

### Run Flask CLI commands

If you want to run Flask CLI commands within a docker container, you should use the following format:

```bash
docker exec stair_challenge_flask flask init_db
```

CLI commands:

- `init_db` - Initialize the database
- `create_admin` - Create an admin user (only works when attached to shell)
- `seed_workouts` - Seed the workouts table with some default workouts

## FAQ

### Temporary failure in name resolution

`socket.gaierror: [Errno -3] Temporary failure in name resolution`

This error may indicate that the IP address of your MQTT server is incorrect.

<!-- MARKDOWN LINKS & IMAGES -->
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com

[basalt]: https://basaltrevalidatie.nl

[build-shield]: https://github.com/Basalt-Revalidatie/stair-dashboard/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/Basalt-Revalidatie/stair-dashboard/actions/workflows/tests.yaml
[codecov-shield]: https://codecov.io/gh/Basalt-Revalidatie/stair-dashboard/branch/main/graph/badge.svg?token=CC2PRKJGQ9
[codecov-url]: https://codecov.io/gh/Basalt-Revalidatie/stair-dashboard
[maintenance-shield]: https://img.shields.io/maintenance/yes/2023.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
