#!/usr/bin/env python3
"""
This module contains complete RESTCONF configuration workflows from multiple nornir_maze functions.

The functions are ordered as followed:
- Complete RESTCONF configuration workflows
"""

from nornir.core import Nornir
from nornir_maze.utils import print_task_title
from nornir_maze.configuration_management.restconf.cisco_rpc import (
    rc_cisco_rpc_is_syncing,
    rc_cisco_rpc_rollback_config,
)


#### Complete RESTCONF Configuration Workflow 01 #############################################################


def rc_replace_config_01(
    config_status: bool, nr_obj: Nornir, rebuild: bool = False, verbose: bool = False
) -> bool:
    """
    This function replace the configuration with the golden-config by default or the day0-config if the
    rebuild argument is set to True and returns True or False wheather the function was successful or not.
    """

    # Return False if config_status argument is False
    if not config_status:
        return False

    # Set rollback_config to day0-config if rebuild is True, else set it to golden-config
    rollback_config = "day0-config" if rebuild else "golden-config"

    print_task_title(f"Replace current config with {rollback_config}")

    # Checks if an active datastore sync in ongoing and wait until is finish
    rc_cisco_rpc_is_syncing(nr_obj=nr_obj, silent=False, verbose=verbose)

    # Replace the running-config with the rollback_config from the switch flash:
    config_status = rc_cisco_rpc_rollback_config(
        nr_obj=nr_obj,
        name=f"RESTCONF rollback {rollback_config}",
        target_url=f"flash:{rollback_config}",
        verbose=verbose,
    )

    return config_status
