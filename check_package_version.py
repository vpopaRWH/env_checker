# pylint:disable=line-too-long
# pylint:disable=broad-exception-caught
"""
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
"""

import subprocess
import sys
import requests


def get_package_version(env_name: str, package_name: str) -> str:
    """
    Get the version of a specified package in a Conda environment.

    Args:
        env_name (str): Name of the Conda environment.
        package_name (str): Name of the package.

    Returns:
        str: Version of the specified package.
    """
    try:
        if sys.platform != "win32":
            activation_cmd = f"source activate {env_name}"
        else:
            activation_cmd = f"conda activate {env_name}"

        pip_show_cmd = f"pip show {package_name}"

        full_cmd = f"{activation_cmd} && {pip_show_cmd}"
        process = subprocess.run(
            full_cmd,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        if process.returncode != 0:
            sys.exit(f"Error activating environment {env_name}: {process.stderr}")

        output = process.stdout
        version_line = [
            line for line in output.split("\n") if line.startswith("Version:")
        ]

        if not version_line:
            sys.exit(f"Package {package_name} not found in environment {env_name}")

        package_version = version_line[0].split(":", 1)[1].strip()
        return package_version

    except Exception as e:
        sys.exit(f"Error getting package version: {str(e)}")


def send_to_teams(
    package_name: str, package_version: str, teams_webhook_url: str
) -> None:
    """
    Send the package name and version information to Microsoft Teams in markdown table format.

    Args:
        package_name (str): Name of the package.
        package_version (str): Version of the package.
        teams_webhook_url (str): Microsoft Teams webhook URL.
    """
    teams_message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "008000",  # Green theme color
        "summary": f"Package Version Check: {package_name}",
        "sections": [
            {
                "activityTitle": f"Package Version Check: {package_name}",
                "markdown": True,
                "text": f"| Package | Version |\n| ------- | ------- |\n| {package_name} | {package_version} |",
            }
        ],
    }

    try:
        response = requests.post(teams_webhook_url, json=teams_message, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        sys.exit(f"Error sending Teams message: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise AttributeError(
            "Usage: python check_package_version.py <env_name> <package_name> <teams_webhook_url>"
        )

    env_name_ = sys.argv[1]
    package_name_ = sys.argv[2]
    TEAMS_WEBHOOK_URL = sys.argv[3]
    package_version_ = get_package_version(
        env_name=env_name_, package_name=package_name_
    )
    send_to_teams(
        package_name=package_name_,
        package_version=package_version_,
        teams_webhook_url=TEAMS_WEBHOOK_URL,
    )
