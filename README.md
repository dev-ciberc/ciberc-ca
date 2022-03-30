# ciberc-ca

CiberC Code Automation

# Commands:

```
Commands:
  alive       Alive for all device filter with groups
  interfaces  Device interface information
  inventory   Create files for inventory system
  login       Login on (CiberC Code Automations) [not required]
  ping        report por vrf and ping results for inventory devices
  ping-merge  Command to merge the source vrf listing files and...
```

### Login command:

```
Description: login on ciberc-ca for use

Options:
  --name TEXT      The name user for ciberc-ca  [required]
  --password TEXT  [required]

Example:
    $ ciberc-ca login --name=name-example
        $ password:
        $ Repeat for confirmation:
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