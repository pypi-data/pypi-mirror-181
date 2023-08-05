#!/usr/bin/env python3
"""
The main function will verify the source software file which should be installed on the switches, uploads
this file to the switches. After the uploaded file has been verified the user will be asked if the script
should start the installation process with RESTCONF in a one-shot approach. This means by answering with
YES, the uploaded software will be installed, commited and the switch will be rebooted without any further
user interaction. If the user ansewers NO, the script will terminate and the installation process can be
started at a later time. If RESTCONF fails for any reason, there is a CLI fallback for each task in place
which tries the same procedure as RESTCONF.
"""

import os
from colorama import Fore, Style, init
from nornir import InitNornir
from nornir.core import Nornir
from nornir_maze.configuration_management.cli.show_tasks import (
    cli_verify_destination_md5_hash,
    cli_install_remove_inactive_task,
)
from nornir_maze.configuration_management.restconf.tasks import (
    rc_verify_current_software_version_fallback_cli,
    rc_software_install_one_shot_fallback_cli,
    rc_install_remove_inactive_fallback_cli,
)
from nornir_maze.software_upgrade.utils import (
    init_args,
    prepare_upgrade_data,
    scp_upload_software_file,
    cli_http_download_software_file,
    fping_track_upgrade_process,
)
from nornir_maze.utils import (
    exit_info,
    print_result,
    exit_error,
    print_script_banner,
    print_task_title,
    nr_filter_args,
    nr_transform_default_creds_from_env,
    nr_transform_inv_from_env,
    nr_filter_inventory_from_host_list,
)

init(autoreset=True, strip=False)


def copy_software(nr_obj: Nornir, local_upload: bool, verbose: bool = False) -> None:
    """
    TBD
    """
    print_task_title("Verify destination software file md5 hash")
    # Verify if the destination file exists and verify the md5 hash.
    failed_hosts = cli_verify_destination_md5_hash(nr_obj=nr_obj)

    # If the failed_hosts list is empty -> Return None
    if not failed_hosts:
        return

    # The failed_hosts list is not empty -> Clean-up all not needed software package files
    print_task_title("Remove inactive software package files for filesystem clean-up")
    # Run the custom Nornir task cli_install_remove_inactive_task
    cli_task_result = nr_obj.run(
        task=cli_install_remove_inactive_task,
        name="CLI install remove inactive",
        verbose=verbose,
        on_failed=True,
    )
    # Print the Nornir cli_install_remove_inactive_task task result
    print_result(cli_task_result)
    # Exit the script is the task failed
    if cli_task_result.failed:
        exit_error(
            task_text="NORNIR software upgrade status",
            text="ALERT: NETMIKO install remove inactive failed!",
        )

    # If the failed_hosts are identical with the Nornir inventory -> All hosts need a software upload
    if sorted(failed_hosts) == sorted(list(nr_obj.inventory.hosts.keys())):
        if local_upload:
            print_task_title("Upload software image file with SCP")
            if not scp_upload_software_file(nr_obj=nr_obj):
                exit_error(
                    task_text="NORNIR software upgrade status",
                    text="ALERT: NETMIKO upload file with SCP failed!",
                )
        else:
            print_task_title("Download software image file with HTTP")
            if not cli_http_download_software_file(nr_obj=nr_obj, verbose=verbose):
                exit_error(
                    task_text="NORNIR software upgrade status",
                    text="ALERT: NETMIKO download file with HTTP failed!",
                )

    # Elif the failed_hosts are not identical with the Nornir inventory -> Some hosts needs software upload
    elif sorted(failed_hosts) != sorted(list(nr_obj.inventory.hosts.keys())):
        if local_upload:
            print_task_title("Upload software image file with SCP")
            # Re-filter the Nornir inventory to the failed_hosts only
            nr_obj_upload = nr_filter_inventory_from_host_list(
                nr_obj=nr_obj,
                filter_reason="Exclude good hosts to upload the software file only on the following hosts:",
                host_list=failed_hosts,
            )
            if not scp_upload_software_file(nr_obj=nr_obj_upload):
                exit_error(
                    task_text="NORNIR software upgrade status",
                    text="ALERT: NETMIKO upload file with SCP failed!",
                )
        else:
            print_task_title("Download software image file with HTTP")
            # Re-filter the Nornir inventory to the failed_hosts only
            nr_obj_upload = nr_filter_inventory_from_host_list(
                nr_obj=nr_obj,
                filter_reason="Exclude good hosts to download the software file only on the following hosts:",
                host_list=failed_hosts,
            )
            if not cli_http_download_software_file(nr_obj=nr_obj_upload, verbose=verbose):
                exit_error(
                    task_text="NORNIR software upgrade status",
                    text="ALERT: NETMIKO download file with HTTP failed!",
                )


def main() -> None:
    """
    This is the main function and is executed when the file is directly executed.
    """
    # pylint: disable=invalid-name

    #### Initialize Script and Nornir ######################################################################

    print_script_banner(
        title="ZIS Nornir CM",
        text="Update software version with Nornir, RESTCONF, CLI, HTTP, SCP and fping.",
    )

    print_task_title("Initialize ArgParse")
    # Initialize the script arguments with ArgParse to define the further script execution
    args = init_args(argparse_prog_name=os.path.basename(__file__))

    print_task_title("Initialize Nornir")
    # Initialize Nornir Object with a config File
    nr = InitNornir(config_file="inventory/nr_config.yaml")

    # Transform the Nornir default username and password from environment variables
    nr_transform_default_creds_from_env(nr_obj=nr, verbose=args.verbose)

    # Transform the Nornir inventory and load all env variables staring with "_env" in default.yaml
    nr_transform_inv_from_env(iterable=nr.inventory.defaults.data, verbose=args.verbose)

    # Filter the Nornir inventory based on the provided arguments from init_args
    nr_obj = nr_filter_args(nr_obj=nr, args=args)

    #### Prepare software upgrade details and verify current version #######################################

    print_task_title("Prepare software version upgrade details")
    # Get the desired version from the Nornir inventory and verify the software file from the inventory in
    # case local image upload is enabled. The inventory will be filled later with more data
    upgrade_type = "scp" if args.local_upload else "http"
    if not prepare_upgrade_data(nr_obj=nr_obj, upgrade_type=upgrade_type):
        exit_error(
            task_text="NORNIR software upgrade status", text="ALERT: NORNIR prepare upgrade data failed!"
        )

    print_task_title("Verify current software version")
    # Verify the desired software version against the installed software version with RESTCONF and a fallback
    # with CLI in case the RESTCONF task would fail. Returns a list of hosts which needs a software upgrade
    failed_hosts = rc_verify_current_software_version_fallback_cli(nr_obj=nr_obj, verbose=args.verbose)

    # If the failed_host list is empty, all hosts match the desired software version and exit the script
    if not failed_hosts:
        exit_info(
            task_text="NORNIR software upgrade status",
            text="The desired software version is up to date on all hosts",
            changed=False,
        )

    # If the failed_host list is not empty and not identical with the Nornir inventory
    if sorted(failed_hosts) != sorted(list(nr_obj.inventory.hosts.keys())):
        print_task_title("Re-Filter nornir inventory")
        # Re-filter the Nornir inventory to the failed_hosts only
        nr_obj = nr_filter_inventory_from_host_list(
            nr_obj=nr_obj,
            filter_reason="Exclude good hosts to run the software upgrade only on the following hosts:",
            host_list=failed_hosts,
        )

    #### Verify destination software file / Upload software file only if not already exists ##################

    # Verify destination md5 hash with cli and upload software file if needed with SCP or HTTP
    # The nornir inventory will be re-filtered if only some hosts needs a software upload and the upload
    # method is SCP or HTTP depending on the args.local_upload argument
    copy_software(nr_obj=nr_obj, local_upload=args.local_upload, verbose=args.verbose)

    #### Start software installation process ###############################################################

    print_task_title("Execute software version upgrade")
    # Create an empty answer variable to be filled with the input and validated until it  is "yes" or "no"
    answer = ""
    while answer not in ("yes", "no"):
        answer = input(
            f"\n{Style.BRIGHT}{Fore.RED}Continue to install the software and reboot the switch?\n"
            f"{Fore.RESET}{Style.RESET_ALL}<yes/no>: "
        )
    # If the answer is no -> Exit the script with exit code 0
    if answer == "no":
        exit_info(
            task_text="NORNIR software upgrade status",
            text="The software upgrade process is ready for install, but has not been started yet",
            changed=False,
        )

    # Install the new software RESTCONF in a one-shot process and a fallback with CLI in case the RESTCONF
    # task would fail. Returns True or False weather the task was successfull or not.
    if not rc_software_install_one_shot_fallback_cli(nr_obj=nr_obj, verbose=args.verbose):
        exit_error(
            task_text="NORNIR software upgrade status",
            text="ALERT: RESTCONF and CLI one-shot install failed!",
        )

    #### Monitor and verify version update status ##########################################################

    # Software upgrade tracking loop with fping until all hosts are upgraded with a max time. The max_time
    # defines how long fping track until the IP connectivity should be back again and the refresh_timer
    # defines the interval where the fping is executed to update the status
    fping_track_upgrade_process(nr_obj=nr_obj, refresh_timer=30, max_time=2400)

    print_task_title("Verify current software version")
    # Verify the desired software version against the installed software version with RESTCONF and a fallback
    # with CLI in case the RESTCONF task would fail. Returns a list of hosts which needs a software upgrade
    failed_hosts = rc_verify_current_software_version_fallback_cli(nr_obj=nr_obj, verbose=args.verbose)

    # If the failed_hosts list is not empty
    if failed_hosts:
        exit_error(
            task_text="NORNIR software upgrade status",
            text="ALERT: RESTCONF and CLI software upgrade failed!",
        )

    #### Cleanup old version files ##########################################################################

    # Remove all not needed software package files on the filesystem with RESTCONF and a fallback with CLI in
    # case the RESTCONF task would fail. Returns a list of hosts which needs a software upgrade
    if not rc_install_remove_inactive_fallback_cli(nr_obj=nr_obj, verbose=args.verbose):
        exit_error(
            task_text="NORNIR software upgrade status",
            text="ALERT: RESTCONF and CLI install remove inactive failed!",
        )

    # The software upgrade was successful on all hosts
    exit_info(
        task_text="NORNIR software upgrade status",
        text="The software upgrade was successful on all hosts",
        changed=True,
    )


if __name__ == "__main__":
    main()
