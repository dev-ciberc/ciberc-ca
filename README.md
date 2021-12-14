# ciberc-ca

CiberC Code Automation

# Commands:

```
  alive       alive for all device filter with groups
  interfaces  informacion de las interfaces de los dispositivos:
  inventory   create files for inventory system
  login       Login on (CiberC Code Automations)
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
  --group TEXT       The groups to filter inventory
  --workers INTEGER  The parallel execution  [default: 2]
  --output TEXT      The type to print report  [default: json]
  --mechanism TEXT   The excel mechanism to print report
  --name TEXT        The name of excel report

Example:
    $ ciberc-ca interfaces --path=core/inventory/ --output=json > interfaces.json
    $ ciberc-ca interfaces --path=core/inventory/ --output=excel --mechanism=row --name=interfaces > interfaces.json
```
