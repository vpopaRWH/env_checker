Module check_package_version
============================

check_package_version.py

This script checks the version of a specific package in a Conda environment and sends the information to a Microsoft Teams webhook in markdown table format.

Usage:
    python check_package_version.py <env_name> <package_name> <teams_webhook_url>

Parameters:
    - env_name (str): Name of the Conda environment to be checked.
    - package_name (str): Name of the package to check.
    - teams_webhook_url (str): Microsoft Teams webhook URL.

The script performs the following steps:

1. Activates the specified Conda environment.
2. Retrieves the version of the specified package using 'pip show.'
3. Sends the package name and version to a Microsoft Teams webhook in markdown table format.

To run the script, provide the necessary command-line arguments as specified in the 'Usage' section.

Dependencies:

- The script uses the 'subprocess', 'sys', and 'requests' modules.
Author: [Your Name]
Date: [Date]

Functions
---------

`get_package_version(env_name: str, package_name: str) ‑> str`
:   Get the version of a specified package in a Conda environment.

    Args:
        env_name (str): Name of the Conda environment.
        package_name (str): Name of the package.

    Returns:
        str: Version of the specified package.

`send_to_teams(package_name: str, package_version: str, teams_webhook_url: str) ‑> None`
:   Send the package name and version information to Microsoft Teams in markdown table format.

    Args:
        package_name (str): Name of the package.
        package_version (str): Version of the package.
        teams_webhook_url (str): Microsoft Teams webhook URL.
