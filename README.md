# ciberc-ca

CiberC Code Automation

Generation of interface reports for IOS devices in parallel, cross validations for migration of VRFs from IOS devices to XR

# https://www.ciberc.com

#  Technology stack

Python 3.6 or higher

#  Status

latest version validated and tested

# Use Case Description

One of our clients generated the VRF migration report in an exhausting time, in terms of the client, one week to validate each piece of equipment, ciberc-ca generates a comparative cross-validation report saving a lot of time and avoiding human errors.

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

  mkdir code & cd code
  python3 -m venv .venv
  source .venv/bin/activate
  python3 -m pip install cibercca

```


# Configuration

The first step is to create the inventory files, in these will go the record of the devices assigned to evaluate

# Examples

## Commands:

```
Commands:
  alive       Alive for all device filter with groups
  interfaces  Device interface information
  inventory   Create files for inventory system
  ping        report por vrf and ping results for inventory devices
  ping-merge  Command to merge the source vrf listing files and...
```

### Alive command:

```
Description: ping report of all inventory devices

Options:
  --path TEXT
  --group TEXT
  --workers INTEGER
  --output TEXT

Example:
    $ ciberc-ca alive --path=inventory/ --group=guatemala --workers=4 --output=json > alive-report.json
```

### Inventory files command:

```
Description: create the necessary files to create the cyberc-ca system inventory

Options:
  --create / --no-create  create files from inventory examples  [default: no-create]

Example:
    $ ciberc-ca inventory --create
```

### Interfaces command:

```
Description: report interfaces of cisco ios devices currently, generates report in json as a summary in excel
    - BVI
    - Vlans
    - trunk interfaces
    - bridge-domain
    - mac-address-table dynamic

Options:
  --path PATH        The path to inventory  [required]
  --group TEXT       The groups to filter inventory [required]
  --workers INTEGER  The parallel execution  [default: 2]
  --output TEXT      The type to print report  [default: json]
  --mechanism TEXT   The excel mechanism to print report
  --name TEXT        The name of excel report

Example:
    $ ciberc-ca interfaces --path=core/inventory/ --output=json > interfaces.json
    $ ciberc-ca interfaces --path=core/inventory/ --output=excel --mechanism=row --name=interfaces > interfaces.json
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

Example:
    $ ciberc-ca ping --path=core/inventory/ --group=src,guatemala,escuintla --output=json --name=ReportPingSource --process=src
    $ ciberc-ca ping --path=core/inventory/ --group=dst,guatemala,escuintla --output=json --name=ReportPingDestinations --process=dst
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

Example:
    $ ciberc-ca ping-merge --file-src=file_vrfs_source.json --file-dst=file_vrf_destinations.json --output=excel --name=ReporteMigrations

```

# Structure

```
inventory/
├── defaults.yaml
├── groups.yaml
└── hosts.yaml


Inventory is based on nornir structure

  defaults.yaml: Contains all the default variables for the devices.

  groups.yaml: Although based on nornir groups, two mandatory groups are needed for configuration, src, dst for the cross-validation ping-merge command.

  hosts.yaml: where all IOS devices are registered for interface reporting, source IOS and destination XR for VRF's migration
```


# Usage

To implement the service once you have defined the computers in the hosts file (here you define the user and password that will be applied per device type), the names of the network devices correctly (in the etc/hosts file) and the devices have SSH setup, then I would put the example commands to activate the ssh and xml agent in XR.

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
https://www.youtube.com/watch?v=d_Vwdx62hG8
