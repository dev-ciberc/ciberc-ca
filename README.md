# ciberc-ca

CiberC Code Automation

Generation of interface reports for IOS devices in parallel, cross validations for migration of VRFs from IOS devices to XR with option for save data from devices in database MongoDB.

# https://www.ciberc.com

#  Technology stack

Python >= 3.8 or < 4.0

#  Status

latest version validated and tested

# Use Case Description

One of our clients generated the VRF migration report in an exhausting time, in terms of the client, one week to validate each piece of equipment, ciberc-ca generates a comparative cross-validation report saving a lot of time and avoiding human errors, at the same time it allows saving and viewing records of alive and interfaces command when establishing a connection with a MongoDB database.

# Installation

```
Ubuntu 20.04 or o any Distribution of Linux with support to Python3
```

# Steps to install in Ubuntu workstation (automation station)

```
prepare environment:
  sudo apt-get install python3
  sudo apt-get install git
  sudo apt-get install python3-pip
  python3 -m pip install virtualenv

  python3 -m venv env
  source env/bin/activate
  python3 -m pip install cibercca
  mkdir code
  cd code

```

# Steps to install using Visual Studio Code

```
You can follow this steps or view this video example https://youtu.be/Ca5pvCZadhg

1. Install Python version >=3.8 or <4.0
	First, download and install Python from the official Python page.
	Make sure to check the "Add Python to PATH" option during the installation.

	python --version

	URL to download Python 3.9.13: https://www.python.org/downloads/release/python-3913/

2. Install Git
	Download and install Git from the official Git page: https://git-scm.com/download/win

3. Install pip (package installer for Python) (if not included with Python)
	Generally, the Python installation on Windows includes pip automatically. To verify, open the Command Prompt (cmd) and run:

	python -m ensurepip --upgrade

4. Start a Python project in Visual Studio Code

	Install virtualenv using pip
	Open the Command Prompt (cmd as administrator) and run:

	python -m pip install virtualenv

5. Create and activate a virtual environment in Visual Studio Code
	Open the Command Prompt (cmd as administrator) and run the following commands to create and activate a virtual environment:

	python -m venv env

	To activate the virtual environment run:

	env\Scripts\activate

	Then create a new folder called code, this folder is going to use to do the management and data of the device network independent:
	mkdir code
	cd code

6. Install cibercca using pip within the virtual environment

	With the virtual environment activated, install cibercca:

	python -m pip install cibercca

```

# Configuration

The first step is to create the inventory files, in these will go the record of the devices assigned to evaluate

### Inventory files command:

```
Description: Create the necessary files to create the cyberc-ca system inventory

Options:
  --create / --no-create  create files from inventory examples  [default: no-create]

Note: Remember to execute command into folder './code >'

Example:
    > ciberc-ca inventory --create
```



### Alive command:

```
Description: Ping report of all inventory devices. When --output=database must be establish database connection 

Options:
  --path TEXT
  --group TEXT
  --workers INTEGER
  --output TEXT      The type to print report (json, table or database)  [default: json]

Note: Remember to execute command into folder './code>'

Example:
    > ciberc-ca alive --path=inventory/ --group=guatemala --workers=4 --output=json > alive-report.json
    > ciberc-ca alive --path=inventory/ --group=guatemala --workers=4 --output=database
```

### Interfaces command:

```
Description: report interfaces of cisco ios devices currently, generates report in json as a summary in excel. When --output=database must be establish database connection
    - BVI
    - Vlans
    - trunk interfaces
    - bridge-domain
    - mac-address-table dynamic

Options:
  --path PATH        The path to inventory  [required]
  --group TEXT       The groups to filter inventory [required]
  --workers INTEGER  The parallel execution  [default: 2]
  --output TEXT      The type to print report (json, excel and database) [default: json]
  --mechanism TEXT   The excel mechanism to print report
  --name TEXT        The name of excel report

Note: Remember to execute command into folder './code>'

Example:
    > ciberc-ca interfaces --path=core/inventory/ --group=guatemala --output=json > interfaces.json
    > ciberc-ca interfaces --path=core/inventory/ --output=excel --mechanism=row --name=interfaces > interfaces.json
    > ciberc-ca interfaces --path=core/inventory/ --group=guatemala --output=database
```


### Ping command:

```
Description: report por vrf and ping results for inventory devices

Options:
  --path PATH        The path to inventory  [required]
  --group TEXT       The groups to filter inventory  [required]
  --workers INTEGER  The parallel execution  [default: 2]
  --output TEXT      The type to print report  [default: json]
  --name TEXT        The name of the excel file
  --process TEXT     what type of process for the vrf report [src, dst] [required]
  --help             Show this message and exit.

Note: Remember to execute command into folder './code>'

Example:
    > ciberc-ca ping --path=core/inventory/ --group=src,guatemala,escuintla --output=json --name=ReportPingSource --process=src
    > ciberc-ca ping --path=core/inventory/ --group=dst,guatemala,escuintla --output=json --name=ReportPingDestinations --process=dst
```

### Ping-Merge command:

```
Description: Command to merge the source vrf listing files and destination with validated report

Options:
  --file-src TEXT  Vrf origin listing file  [required]
  --file-dst TEXT  Target vrf listing file  [required]
  --output TEXT    The type to print report  [required]
  --name TEXT      The name of the excel file
  --help           Show this message and exit.

Note: Remember to execute command into folder './code>'

Example:
    > ciberc-ca ping-merge --file-src=file_vrfs_source.json --file-dst=file_vrf_destinations.json --output=excel --name=ReporteMigrations

```

### Records command:

```
Description: Return record list for type of command, just if exist data and connection with MongoDB (alive or interfaces)

Options:
  --command TEXT  Type of command (alive or interfaces)  [required]

Note: Remember to execute command into folder './code>'

Example:
    > ciberc-ca records ---command=alive
    > ciberc-ca records ---command=interfaces

```

# Structure

```
inventory/
├── dbconnect.yaml
├── defaults.yaml
├── groups.yaml
└── hosts.yaml


Inventory is based on nornir structure

  dbconnect.yaml: Contains url connection for MongoDB.

  defaults.yaml: Contains all the default variables for the devices.

  groups.yaml: Although based on nornir groups, two mandatory groups are needed for configuration, src, dst for the cross-validation ping-merge command.

  hosts.yaml: where all IOS devices are registered for interface reporting, source IOS and destination XR for VRF's migration
```


# Usage

Para implementar el servicio una vez que haya definido los equipos en el archivo de hosts (aquí se define el usuario y la contraseña que se aplicará por tipo de dispositivo), los nombres de los dispositivos de red correctamente (en el archivo etc/hosts) y los dispositivos tienen la configuración de SSH, entonces colocaría los comandos de ejemplo para activar el agente ssh y xml en XR.

# configuration example in XR device
```
# default.yaml
---
data:
  domain: local.local


# groups.yaml
---
# {} => ejemplo
guatemala: {}

# for the ping report, it contains all the source computers
src: {}

# for the ping report, it contains all the destination computers
dst: {}


# hosts.yaml
---
R1:
  hostname: localhost
  port: 22
  username: user
  password: secret
  platform: ios
  groups:
    - guatemala
    - src # used to separate the source computers from the migration

R2:
  hostname: localhost
  port: 22
  username: user
  password: secret
  platform: iosxr
  data:
    source: R1 # to which device does the migration belong, virtual link to compare reports
  groups:
    - guatemala
    - dst # used to separate the migration destination computers


```


# How to test the software

you can check the configuration in the devices in the generated report

# Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository, or send me an email to: Dev.auto@ciberc.com

# Link Video Example
https://youtu.be/Ca5pvCZadhg
