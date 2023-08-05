#!/usr/bin/env python3
"""
This module contains screen-scraping functions and tasks related to Nornir.

The functions are ordered as followed:
- Single Nornir Screen-Scraping Tasks
- Nornir Screen-Scraping Tasks in regular Functions
"""

import sys
import json
from colorama import Fore, Style, init
from nornir_utils.plugins.tasks.files import write_file
from nornir.core import Nornir
from nornir.core.task import Task, Result
from nornir_maze.utils import (
    print_result,
    print_task_name,
    task_host,
    task_info,
    task_error,
)

init(autoreset=True, strip=False)


#### Single Nornir Screen Scraping Tasks #####################################################################


def cli_verify_current_software_version_task(task: Task, verbose=False) -> Result:
    """
    TBD
    """
    # Get the desired version from the Nornir inventory
    desired_version = task.host["software"]["version"]

    # Manually create Scrapli connection
    conn = task.host.get_connection("scrapli", task.nornir.config)
    # Run Scrapli send_command to get show version
    output = conn.send_command(command="show version")
    # Parse the show version scrapli response with the genie parser
    output_parsed = output.genie_parse_output()

    # Find xe software version of the device
    if "xe_version" in output_parsed["version"]:
        # Write the current version from the genie parsed result into a variable
        current_version = output_parsed["version"]["xe_version"]
        # Write the current version into the Nornir inventory
        task.host["software"]["current_version"] = current_version

        # If the desired version and the current version are the same
        if desired_version in current_version:
            result = (
                f"'{task.name}' -> CliResponse <Success: True>\n"
                f"-> Desired version {desired_version} match installed version {current_version}"
            )
            # Define the result variable for print_result
            result = result + "\n\n" + json.dumps(output_parsed, indent=4) if verbose else result

            # Return the Nornir result as success
            return Result(host=task.host, result=result)

        # Else the desired version and the current version are not the same
        result = (
            f"'{task.name}' -> CliResponse <Success: False>\n"
            f"-> Desired version {desired_version} don't match installed version {current_version}"
        )
        # Define the result variable for print_result
        result = result + "\n\n" + json.dumps(output_parsed, indent=4) if verbose else result

        # Return the Nornir result as failed
        return Result(host=task.host, result=result, failed=True, need_upgrade=True)

    result = (
        f"'{task.name}' -> CliResponse <Success: False>\n"
        f"-> Genie parser dict key 'xe_version' could not be found\n"
        f"{json.dumps(output_parsed, indent=4)}"
    )

    # If the xe software version was not found -> The task failed and set the overall_task_failed to True
    return Result(host=task.host, result=result, failed=True, overall_task_failed=True)


def cli_install_one_shot_task(task: Task, verbose=False) -> Result:
    """
    TBD
    """
    # Get the host destination file from the Nornir inventory
    dest_file = task.host["software"]["dest_file"]

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)

    # As the command is really long Netmiko stops when the expect_string is seen. When the package activating
    # start the software is added, nothing should go wrong anymore and the fping_track_upgrade_process()
    # can be started to verify the upgrade and reload process.
    output = net_connect.send_command(
        command_string=f"install add file flash:{dest_file} activate commit prompt-level none",
        expect_string="install_add_activate_commit: Activating PACKAGE",
        read_timeout=1200,
    )

    if "install_add_activate_commit: Activating PACKAGE" in output:
        result_summary = f"'{task.name}' -> CliResponse <Success: True>"
        # Define the result variable for print_result
        result = result_summary + "\n\n" + output if verbose else result_summary

        # Return the  Nornir result as success
        return Result(host=task.host, result=result)

    # Else the cli one-shot software install failed
    result = f"'{task.name}' -> CliResponse <Success: False>\n\n" f"{result}"

    # Return the custom Nornir result as failed
    return Result(host=task.host, result=result, failed=True)


def cli_install_remove_inactive_task(task: Task, verbose=False) -> Result:
    """
    TBD
    """
    # Set the result_summary for a successful task
    result_summary = f"'{task.name}' -> CliResponse <Success: True>"

    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)

    # Execute send_command with an expect_string to finish. Netmiko feeds the expect_string into pythons RE
    # library and therefor the pipe can be used as logical "or" statement.
    output = net_connect.send_command(
        command_string="install remove inactive",
        expect_string="Do you want to remove the above files?|SUCCESS: install_remove",
        read_timeout=600,
    )

    if "Do you want to remove the above files?" in output:
        output += net_connect.send_command(
            command_string="y",
            expect_string=f"{task.host}#",
            read_timeout=600,
        )
        # Define the result variable for print_result
        result = result_summary + "\n\n" + output if verbose else result_summary

        # Return the custom Nornir result as success
        return Result(host=task.host, result=result)

    if "SUCCESS: install_remove" in output:
        # Define the result variable for print_result
        result = result_summary + "\n\n" + output if verbose else result_summary

        # Return the custom Nornir result as success
        return Result(host=task.host, result=result)

    # Else the command install remove inactive failed without traceback exception
    result = f"'{task.name}' -> CliResponse <Success: False>\n\n{output}"
    # Return the Nornir result as failed
    return Result(host=task.host, result=result, failed=True)


def cli_get_serial_numbers(task: Task, verbose: bool = False) -> Result:
    """
    TBD
    """
    # Manually create Scrapli connection
    conn = task.host.get_connection("scrapli", task.nornir.config)
    # Run Scrapli send_command to get show version
    output = conn.send_command(command="show version")

    # Parse the show version scrapli response with the genie parter
    output_parsed = output.genie_parse_output()
    verbose_result = json.dumps(output_parsed, indent=4)

    # Find the correct serial numbers of the device (multiple serials if its a stack)
    serials = {}
    if "nxos" in conn.genie_platform:
        serials["1"] = output_parsed["platform"]["hardware"]["processor_board_id"].upper()
    elif "iosxe" in conn.genie_platform:
        for switch_num, switch_details in output_parsed["version"]["switch_num"].items():
            if "system_sn" in switch_details:
                serials[switch_num] = switch_details["system_sn"].upper()
    else:
        result = (
            f"'{task.name}' -> CliResponse <Success: False>\n"
            f"-> Unsupport scrapli genie platform: {conn.genie_platform}\n\n"
            f"\n{verbose_result}"
        )
        # Return the Nornir result as failed
        return Result(host=task.host, result=result, failed=True)

    # Order the serials dict by the switch_num in ascending order
    order_list = sorted(list(serials.keys()))
    serials = {key: serials[key] for key in order_list}

    # If the serial number was found and and the serials list in not empty
    if serials:
        result = f"'{task.name}' -> CliResponse <Success: True>"
        for switch_num, serial in serials.items():
            result += f"\n-> Device {switch_num}: {serial}"
        # Set the result print level to summary or verbose
        result = result + "\n\n" + verbose_result if verbose else result

        # Return the Nornir result as successful
        return Result(host=task.host, result=result, serials=serials)

    # Else the serial number could not be found
    result = (
        f"'{task.name}' -> CliResponse <Success: False>\n"
        f"-> No serials identified\n\n"
        f"\n{verbose_result}"
    )
    # Return the Nornir result as failed
    return Result(host=task.host, result=result, failed=True)


def cli_get_software_version(task: Task, verbose: bool = False) -> Result:
    """
    TBD
    """
    # Manually create Scrapli connection
    conn = task.host.get_connection("scrapli", task.nornir.config)
    # Run Scrapli send_command to get show version
    output = conn.send_command(command="show version")

    # Parse the show version scrapli response with the genie parter
    output_parsed = output.genie_parse_output()
    verbose_result = json.dumps(output_parsed, indent=4)

    # Find the correct software version of the device
    version = None
    if "nxos" in conn.genie_platform:
        version = output_parsed["platform"]["software"]["system_version"].upper()
    elif "iosxe" in conn.genie_platform:
        if "version" in output_parsed["version"]:
            version = output_parsed["version"]["version"]
        elif "xe_version" in output_parsed["version"]:
            # Replace all 0 in the xe_version to normalizing iosxe and non-iosxe version format
            # -> Make 17.03.05 to 17.3.5
            version = output_parsed["version"]["xe_version"].replace("0", "")
    else:
        result = (
            f"'{task.name}' -> CliResponse <Success: False>\n"
            f"-> Unsupport scrapli genie platform: {conn.genie_platform}\n\n"
            f"\n{verbose_result}"
        )
        # Return the Nornir result as failed
        return Result(host=task.host, result=result, failed=True)

    # If the software version was found and is not None
    if version:
        result = f"'{task.name}' -> CliResponse <Success: True>\n" f"-> Device software version {version}"
        # Set the result print level to summary or verbose
        result = result + "\n\n" + verbose_result if verbose else result

        # Return the custom Nornir result as successful
        return Result(host=task.host, result=result, version=version)

    # Else the software version could not be found
    result = (
        f"'{task.name}' -> CliResponse <Success: False>\n"
        f"-> No software version identified\n\n"
        f"\n{verbose_result}"
    )
    # Return the Nornir result as failed
    return Result(host=task.host, result=result, failed=True)


def cli_verify_destination_md5_hash_task(task: Task) -> Result:
    """
    TBD
    """

    # Prepare all needed variables form the Nornir inventory
    dest_file = task.host["software"]["dest_file"]
    source_md5 = task.host["software"]["source_md5"]

    # Manually create Scrapli connection
    conn = task.host.get_connection("scrapli", task.nornir.config)
    # Run the Scrapli Nornir task send_command to verify the destination file md5 hash
    output = conn.send_command(
        command=f"verify /md5 flash:{dest_file} {source_md5}",
        strip_prompt=True,
        timeout_ops=180,
    )

    # Extract the md5 hash from the output string
    for line in output.result.splitlines():
        # Source and destination md5 hast are identical
        if line.startswith("Verified"):
            # Split the line string into words
            dest_md5 = line.split()
            # Slicing the list -> -1 means the last element of the list which is the md5 hash
            dest_md5 = dest_md5[-1]
            result = (
                f"'{task.name}' -> CliResponse <Success: True>\n"
                "MD5-Hashes are identical:\n"
                f"-> Source MD5-Hash: {source_md5}\n"
                f"-> Destination MD5-Hash: {dest_md5}"
            )
            # Return the custom Nornir result as successful
            return Result(host=task.host, result=result)

        # Source and destination md5 hash are different -> Upload failed
        if line.startswith("Computed signature"):
            # Split the string into words
            dest_md5 = line.split()
            # Slicing the list -> -1 means the last element of the list which is the md5 hash
            dest_md5 = dest_md5[-1]
            result = (
                f"'{task.name}' -> CliResponse <Success: False>\n"
                "MD5-Hashes are not identical:\n"
                f"-> Source MD5-Hash: {source_md5}\n"
                f"-> Destination MD5-Hash: {dest_md5}"
            )
            # Return the custom Nornir result as failed
            return Result(host=task.host, result=result, failed=True)

        # There is an %Error as the file don't exist
        if line.startswith("%Error"):
            result = f"'{task.name}' -> CliResponse <Success: False>\n" + f"-> {line}"
            # Return the custom Nornir result as failed
            return Result(host=task.host, result=result, failed=True)

    # If no if statement match the whole for loop -> Return the custom Nornir result as failed
    result = f"'{task.name}' -> CliResponse <Success: False>\n" + f"-> {output.result}"
    return Result(host=task.host, result=result, failed=True, overall_task_failed=True)


def custom_write_file(
    task: Task, commands: list, path: str, filename_suffix: str, backup_config: bool = False
) -> Result:
    """
    This custom Nornir task takes a list of commands to execute, a path and a filename suffix as arguments and
    writes the output of the commands to that file. The start of the filename is the hostname and as suffix
    can any text be added.
    """
    # Manually create Scrapli connection
    conn = task.host.get_connection("scrapli", task.nornir.config)

    # The emtpy string will be filled and written to file
    content = ""

    # Execute each command individual to add custom content for each command
    for command in commands:
        output = conn.send_command(command=command, strip_prompt=True, timeout_ops=180)

        if backup_config:
            # If the file should be a backup of the configuration, then remove unwanted lines which are not
            # real configurations and to avoid unwanted git commits
            for line in output.result.splitlines():
                if line.startswith("Building configuration..."):
                    continue
                if line.startswith("Current configuration :"):
                    continue
                if line.startswith("! Last configuration change"):
                    continue
                if line.startswith("! NVRAM config last updated"):
                    continue

                # If no line to exclude matched, add the line to the content
                content += f"{line}\n"

        else:
            # Add the promt with the command and then the command result
            content += f"{task.host}#{command}\n{output.result}\n\n"

        # Remove any possible starting or ending blank lines
        content = content.rstrip()
        content = content.lstrip()

    # Write the content variable to the file specified by the arguments
    task.run(task=write_file, filename=f"{path}/{task.host}{filename_suffix}", content=content, append=False)


#### Nornir Task in regular Functions ########################################################################


def cli_verify_destination_md5_hash(nr_obj):
    """
    TBD
    """

    # Run the custom Nornir task verify_destination_md5_hash
    task_result = nr_obj.run(
        task=cli_verify_destination_md5_hash_task,
        name="CLI verify destination file",
        on_failed=True,
    )

    # Print the Nornir task result
    print_result(task_result)

    # If the task overall task result failed -> Print results and exit the script
    for host in task_result:
        if hasattr(task_result[host], "overall_task_failed"):
            print("\n")
            print(task_error(text="CLI verify destination file", changed=False))
            print("\U0001f4a5 ALERT: CLI DESTINATION FILE MD5 HASH VERIFICATION FAILED! \U0001f4a5")
            print(
                f"\n{Style.BRIGHT}{Fore.RED}-> Analyse the Nornir output for failed task results\n"
                "-> May apply Nornir inventory changes and run the script again\n"
            )
            sys.exit(1)

    # List to fill with hosts with not matching destination file md5 hash or not existing destination file
    failed_hosts = list(task_result.failed_hosts)

    return failed_hosts


def write_commands_to_file(
    nr_obj: Nornir,
    name: str,
    commands: list,
    path: str,
    filename_suffix: str,
    backup_config: bool = False,
    verbose: bool = False,
) -> bool:
    """
    #### CODE REFACTORING NEEDED -> INTRODUCE print_result ####

    This function takes a list of commands to execute, a path and a filename suffix as arguments and writes
    the output of the commands to that file. The start of the filename is the hostname and as suffix can any
    text be added.
    """
    # pylint: disable=too-many-arguments,too-many-locals

    # Set the variable to return at the end of the function to True
    config_status = True

    print_task_name(text=name)

    task_result = nr_obj.run(
        task=custom_write_file,
        commands=commands,
        path=path,
        filename_suffix=filename_suffix,
        backup_config=backup_config,
        on_failed=True,
    )

    for host, multi_result in task_result.items():
        print(task_host(host=host, changed=task_result[host].changed))

        # Print first all Scrapli send_command results
        for result in multi_result:
            # Get the attribute scrapli_response from result into a variable -> Return None if don't exist
            scrapli_result = getattr(result, "scrapli_response", None)

            if scrapli_result is None:
                continue

            task_text = "Execute command"
            cmd = str(scrapli_result.channel_input)

            if scrapli_result.failed:
                print(task_error(text=task_text, changed=scrapli_result.failed))
                print(f"'{cmd}' -> CliResponse <Success: False>\n")
                print(f"{host}#{cmd}")
                print(scrapli_result.result)
            else:
                print(task_info(text=task_text, changed=scrapli_result.failed))
                print(f"'{cmd}' -> CliResponse <Success: True>")
                if verbose:
                    print(f"{host}#{cmd}")
                    print(scrapli_result.result)

        # The write_file result is only present if all Scrapli send_command tasks were successful
        filepath = f"{path}/{host}{filename_suffix}"

        # pylint: disable=undefined-loop-variable
        if [True for result in multi_result if result.name == "write_file"]:
            # The write_file result is present and no exception exists
            if result.exception is None:
                print(task_info(text="Save command(s) to file", changed=False))
                print(f"'{filepath}' -> NornirResponse <Success: True>")

            # An exception is raised when the folder don't exist
            else:
                print(task_error(text="Save command(s) to file", changed=False))
                print(f"'{filepath}' -> NornirResponse <Success: False>\n")
                print(result.exception)
                config_status = False

        # The write_file result is not present as one or more commands have failed
        else:
            print(task_error(text="Save command(s) to file", changed=False))
            print(f"'{filepath}' -> NornirResponse <Success: False>\n")
            print("Command(s) failed -> Command(s) have not been written to file\n")
            print(result.exception)
            print(result.result)
            config_status = False

    return config_status
