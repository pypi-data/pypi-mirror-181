#!/usr/bin/env python3
"""
This module contains general functions and tasks related to the Cisco Support APIs with Nornir.

The functions are ordered as followed:
- Helper Functions
- Static or Dynamic Nornir Serial Numbers Gathering
"""


import os
import sys
import json
import argparse
import pandas as pd
import numpy as np
from colorama import Fore, Style, init
from nornir.core import Nornir
from nornir_maze.configuration_management.cli.show_tasks import (
    cli_get_serial_numbers,
    cli_get_software_version,
)
from nornir_maze.utils import (
    CustomArgParse,
    CustomArgParseWidthFormatter,
    print_result,
    print_task_name,
    task_info,
    task_error,
    exit_error,
)

init(autoreset=True, strip=False)


#### Helper Functions ########################################################################################


def init_args(argparse_prog_name: str) -> argparse.Namespace:
    """
    This function initialze all arguments which are needed for further script execution. The default
    arguments will be supressed. Returned will be the argparse Namespace with all arguments.
    """
    task_text = "ARGPARSE verify arguments"
    print_task_name(text=task_text)

    # Define the arguments which needs to be given to the script execution
    argparser = CustomArgParse(
        prog=argparse_prog_name,
        description="Gather information dynamically with Nornir or use static provided information",
        epilog="Only one of the mandatory arguments can be specified.",
        argument_default=argparse.SUPPRESS,
        formatter_class=CustomArgParseWidthFormatter,
    )

    # Create a mutually exclusive group.
    # Argparse will make sure that only one of the arguments in the group is present on the command line
    arg_group = argparser.add_mutually_exclusive_group(required=True)

    # Add arg_group exclusive group parser arguments
    arg_group.add_argument(
        "--tag", type=str, metavar="<VALUE>", help="nornir inventory filter on a single tag"
    )
    arg_group.add_argument(
        "--hosts", type=str, metavar="<VALUE>", help="nornir inventory filter on comma seperated hosts"
    )
    arg_group.add_argument(
        "--serials", type=str, metavar="<VALUE>", help="comma seperated list of serial numbers"
    )
    arg_group.add_argument("--excel", type=str, metavar="<VALUE>", help="excel file with serial numbers")

    # Add the optional client_key argument that is only needed if Nornir is not used
    argparser.add_argument(
        "--api_key", type=str, metavar="<VALUE>", help="specify Cisco support API client key"
    )
    # Add the optional client_key argument that is only needed if Nornir is not used
    argparser.add_argument(
        "--api_secret", type=str, metavar="<VALUE>", help="specify Cisco support API client secret"
    )
    # Add the optional tss argument
    argparser.add_argument(
        "--tss", type=str, default=False, metavar="<VALUE>", help="add a IBM TSS Excel report file"
    )
    # Add the optional verbose argument
    argparser.add_argument(
        "-r", "--report", action="store_true", default=False, help="create and Excel report file"
    )
    # Add the optional verbose argument
    argparser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="show extensive result details"
    )

    # Verify the provided arguments and print the custom argparse error message in case of an error
    args = argparser.parse_args()

    # Verify that --api_key and --api_secret is present when --serials or --excel is used
    if ("serials" in vars(args) or "excel" in vars(args)) and (
        "api_key" not in vars(args) or "api_secret" not in vars(args)
    ):
        # Raise an ArgParse error if --api_key or --api_secret is missing
        argparser.error("The --api_key and --api_secret argument is required for static provided data")

    print(task_info(text=task_text, changed=False))
    print(f"'{task_text}' -> ArgparseResponse <Success: True>")

    if hasattr(args, "tag") or hasattr(args, "hosts"):
        print("-> Gather data dynamically with Nornir")
        vars(args).update(nornir=True)
    else:
        print("-> Use static provided data")
        vars(args).update(nornir=False)

    return args


#### Static or Dynamic Nornir Serial Numbers Gathering #######################################################


def prepare_nornir_data(nr_obj: Nornir, verbose: bool = False) -> dict:
    """
    This function use Nornir to gather and prepare the serial numbers and more data and returns the
    serials dictionary.
    """
    # Run the Nornir task cli_get_serial_number to get all serial numbers
    cli_get_serial_number_result = nr_obj.run(
        task=cli_get_serial_numbers, name="NORNIR prepare serial numbers", verbose=verbose
    )
    # Print the Nornir task result
    print_result(cli_get_serial_number_result)

    # Run the Nornir task cli_get_software_version to get all software versions
    cli_get_software_version_result = nr_obj.run(
        task=cli_get_software_version, name="NORNIR prepare software version", verbose=verbose
    )
    # Print the Nornir task result
    print_result(cli_get_software_version_result)

    # Exit the script if one of the Nornir tasks have been failed
    if cli_get_serial_number_result.failed or cli_get_software_version_result.failed:
        exit_error(task_text="NORNIR cisco maintenance status", text="Bad news! The script failed!")

    # Create a dict to fill with the serial numbers and other data from all hosts
    serials = {}
    for host, multiresult in cli_get_serial_number_result.items():
        # Get the serial number from the task result cli_get_serial_number_result attribut serial
        for switch_num, serial in multiresult.serials.items():
            # Add the hostname and Nornir data key value pair to the serial in the data dict
            data = {
                serial: {
                    "host": host,
                    "nr_data": {},
                },
            }
            # Add the switch number key value pair to the serial in the data dict
            data[serial]["nr_data"]["switch_num"] = switch_num
            # Add the desired version key value pair to the serial in the data dict
            data[serial]["nr_data"]["desired_version"] = nr_obj.inventory.hosts[host]["software"]["version"]
            # Add the software version key value pair to the serial in the data dict
            data[serial]["nr_data"]["current_version"] = cli_get_software_version_result[host].version
            # Update the serials dict with the serial dict
            serials.update(data)

    return serials


def prepare_static_serials(args: argparse.Namespace) -> tuple[dict, str, tuple]:
    """
    This function prepare all static serial numbers which can be applied with the serials ArgParse argument
    or within an Excel document. It returns the serials dictionary.
    """
    # pylint: disable=invalid-name

    task_text = "ARGPARSE verify static provided data"
    print_task_name(text=task_text)

    # Create a dict to fill with all serial numbers
    serials = {}

    # If the --serials argument is set, verify that the tag has hosts assigned to
    if hasattr(args, "serials"):
        print(task_info(text=task_text, changed=False))
        print(f"'{task_text}' -> ArgparseResult <Success: True>")

        # Add all serials from args.serials to the serials dict, as well as the hostname None
        for sr_no in args.serials.split(","):
            serials[sr_no.upper()] = {}
            serials[sr_no.upper()]["host"] = None

        print(task_info(text="PYTHON prepare static provided serial numbers", changed=False))
        print("'PYTHON prepare static provided serial numbers' -> ArgparseResult <Success: True>")
        if args.verbose:
            print("\n" + json.dumps(serials, indent=4))

    # If the --excel argument is set, verify that the tag has hosts assigned to
    elif hasattr(args, "excel"):
        # Verify that the excel file exists
        if not os.path.exists(args.excel):
            # If the excel don't exist -> exit the script properly
            print(task_error(text=task_text, changed=False))
            print(f"'{task_text}' -> ArgparseResult <Success: False>")
            print("\n\U0001f4a5 ALERT: FILE NOT FOUND! \U0001f4a5\n")
            print(
                f"{Style.BRIGHT}{Fore.RED}-> Excel file {args.excel} not found\n"
                "-> Verify the file path and the --excel argument\n\n"
            )
            sys.exit(1)

        print(task_info(text=task_text, changed=False))
        print(f"'{task_text}' -> ArgparseResult <Success: True>")

        # Read the excel file into a pandas dataframe -> Row 0 is the title row
        df = pd.read_excel(rf"{args.excel}", skiprows=[0])

        # Make all serial numbers written in uppercase letters
        df.sr_no = df.sr_no.str.upper()

        # The first fillna will replace all of (None, NAT, np.nan, etc) with Numpy's NaN, then replace
        # Numpy's NaN with python's None
        df = df.fillna(np.nan).replace([np.nan], [None])

        # Add all serials and hostnames from pandas dataframe to the serials dict
        for sr_no, host in zip(df.sr_no, df.host):
            serials[sr_no] = {}
            serials[sr_no]["host"] = host

        # Print the static provided serial numbers
        print(task_info(text="PANDAS prepare static provided Excel", changed=False))
        print("'PANDAS prepare static provided Excel' -> ArgparseResult <Success: True>")
        if args.verbose:
            print("\n" + json.dumps(serials, indent=4))

    else:
        print(task_error(text=task_text, changed=False))
        print(f"'{task_text}' -> ArgparseResult <Success: False>")
        print("\n\n\U0001f4a5 ALERT: NOT SUPPORTET ARGPARSE ARGUMENT FOR FURTHER PROCESSING! \U0001f4a5")
        print(f"\n{Style.BRIGHT}{Fore.RED}-> Analyse the python function for missing Argparse processing\n\n")
        sys.exit(1)

    # return the serials dict
    return serials
