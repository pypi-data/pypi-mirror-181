![Header-Image](https://user-images.githubusercontent.com/70367776/188263859-0034b5f1-4e61-4f79-b34d-f7744f972810.png)

----
![PyPI](https://img.shields.io/pypi/v/nornir-maze?label=pypi%20version&style=plastic)
![PyPI - License](https://img.shields.io/pypi/l/nornir-maze?label=license&style=plastic)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/nornir-maze?label=wheel&style=plastic)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nornir-maze?label=python&style=plastic)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/nornir-maze?label=implementation&style=plastic)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/willikubny/nornir-maze?label=code%20size&style=plastic)
![Lines of code](https://img.shields.io/tokei/lines/github/willikubny/nornir-maze?label=total%20lines&style=plastic)


# Nornir-Maze

```diff
! Documentation under construction ...
```

### Introduction

Nornir_maze is a collection of Nornir tasks and general functions in Nornir stdout style.

By now nornir_maze contains the following modules:

#### General Modules with Helper Functions
* nornir_maze.git
* nornir_maze.utils

#### Cisco Software Upgrade
* nornir_maze.software_upgrade.utils
* nornir_maze.software_upgrade.nr_software_upgrade (ready-to-use script)

#### Cisco Support API
* nornir_maze.cisco_support.utils
* nornir_maze.cisco_support.api_calls
* nornir_maze.cisco_support.reports

#### Cisco Configuration Management
* nornir_maze.configuration_management.utils
* nornir_maze.configuration_management.pyats
* nornir_maze.configuration_management.cli.show_tasks
* nornir_maze.configuration_management.cli.config_tasks
* nornir_maze.configuration_management.cli.config_workflow
* nornir_maze.configuration_management.restconf.tasks
* nornir_maze.configuration_management.restconf.cisco_rpc
* nornir_maze.configuration_management.restconf.config_workflow
* nornir_maze.configuration_management.netconf.ops_tasks
* nornir_maze.configuration_management.netconf.config_tasks
* nornir_maze.configuration_management.netconf.config_workflow

## Installation

In order to use the tasks and functions from nornir-maze you will need to install the library from Pypi.

```bash
pip install nornir-maze
```

## Scripts Ready-to-Use

### nr_software_upgrade.py

The module `nornir_maze.software_upgrade.nr_software_upgrade` of nornir-maze is a ready-to-use script which can be imported and executed as shown below. The nr_software_upgrade script should work for the whole Cisco Catalys 9000 series. There are two options available to copy the software to the switches, which are an upload with SCP or a download with HTTP. Every task that is possible is first executed with RESTCONF and in case RESTCONF fails for any reason, then a CLI fallback task will be started only for the failed hosts.

```python3
#!/usr/bin/env python3
"""
OWN DESCRIPTION
"""

from nornir_maze.software_upgrade import nr_software_upgrade


def main() -> None:
    """
    This is the main function and is executed when the file is directly executed.
    """
    nr_software_upgrade.main()


if __name__ == "__main__":
    main()
```

The script needs from the Nornir inventory a dictionary called `software` with three key value pairs. The `version` specifies the desired version which will be verified in the beginning in order to only taget host which really needs a software upgrade. The `filepath` specifies the path and filename and is needed of the SCP upload argument `local_upload` is used. The `http_url` is used as the default method if the `local_upload` argument is not used. Only one of both key value pairs are mandatory depending which method is used. Please read the comment below regading the dependencie of the `filepath` and the `http_url` key value pair.

To structure the Nornir inventory for different versions or files the `software` dictionary can be used in groups for the specific device us usecase.

```yaml
#### Cisco IOS-XE Software ###################################################################################

# The key "filepath" is mandatory for SCP upload and the key "http_url" is mandatory for HTTP download. If
# both keys "http_url" and "filepath" are present, then the md5 hash verification is made with "filepath"
# rather then with "http_url". This is much faster as the md5 hash can be computed directly on the local disk.

iosxe_c9200:
  data:
    software:
      version: 17.03.04
      filepath: docker_srv_httpd_nr_cm/htdocs/cat9k_lite_iosxe.17.03.04.SPA.bin
      http_url: http://10.1.10.180:9999/cat9k_lite_iosxe.17.03.04.SPA.bin

iosxe_c9300_c9600:
  data:
    software:
      version: 17.03.04
      filepath: docker_srv_httpd_nr_cm/htdocs/cat9k_iosxe.17.03.04.SPA.bin
      http_url: http://10.1.10.180:9999/cat9k_iosxe.17.03.04.SPA.bin
```
