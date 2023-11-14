# pylint:disable=line-too-long
# pylint:disable=broad-exception-caught
"""
check_conda_env.py

This script checks the compatibility of installed packages in a Conda environment with the versions specified in a requirements file. If any incompatibilities are found, it sends an alert to a Microsoft Teams webhook.

Usage:
    python check_conda_env.py <env_name> <requirements_file> <required_python_version> <teams_webhook_url>

Parameters:
    - env_name (str): Name of the Conda environment to be checked.
    - requirements_file (str): Path to the requirements file containing package requirements.
    - required_python_version (str): Required Python version (major version only).
    - teams_webhook_url (str): Microsoft Teams webhook URL.

The script performs the following steps:
1. Activates the specified Conda environment.
2. Retrieves a list of installed packages and their versions in the environment using 'pip freeze.'
3. Compares the installed packages with the requirements specified in the requirements file.
4. Checks for compatibility issues, including Python major version mismatch.
5. Sends an alert to a Microsoft Teams webhook if incompatibilities are found.

The Microsoft Teams alert message includes details about the incompatibilities detected in a table format.

To run the script, provide the necessary command-line arguments as specified in the 'Usage' section.

Dependencies:
- The script uses the 'subprocess', 're', 'sys', 'packaging.requirements', and 'requests' modules.
Author: [Your Name]
Date: [Date]
"""
print("Start")
import subprocess
import re
import sys
from packaging.requirements import Requirement
import requests


def parse_requirements_file(requirements_file: str) -> list[str]:
    """
    Parse a requirements file and return a list of requirements.

    Args:
        requirements_file (str): Path to the requirements file.

    Returns:
        list[str]: List of requirements.
    """
    with open(requirements_file, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def get_installed_packages(env_name: str) -> dict[str, str]:
    """
    Get a dictionary of installed packages and their versions in a Conda environment.

    Args:
        env_name (str): Name of the Conda environment.

    Returns:
        dict[str, str]: Dictionary of installed packages and their versions.
    """
    try:
        if sys.platform != "win32":
            activation_cmd = f"source activate {env_name}"
        else:
            activation_cmd = f"conda activate {env_name}"

        pip_freeze_cmd = "pip freeze"

        full_cmd = f"{activation_cmd} && {pip_freeze_cmd}"
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
        lines = output.split("\n")
        installed_packages = {}

        for line in lines:
            if line.strip() and "==" in line.strip():
                parts = line.split("==", 1)
                package_name, package_version = parts
                installed_packages[package_name] = package_version

        return installed_packages

    except Exception as e:
        sys.exit(f"Error getting installed packages: {str(e)}")


def check_env_compatibility(
    env_name: str,
    requirements_file: str,
    required_python_version: str,
    teams_webhook_url: str,
) -> None:
    """
    Check compatibility of installed packages in a Conda environment with the versions specified in the requirements file.
    Send an alert to a Microsoft Teams webhook with incompatibilities found.

    Args:
        env_name (str): Name of the Conda environment.
        requirements_file (str): Path to the requirements file.
        required_python_version (str): Required Python version (major version only).
        teams_webhook_url (str): Microsoft Teams webhook URL.
    """
    installed_packages = get_installed_packages(env_name)
    requirements = parse_requirements_file(requirements_file)
    incompatibilities = []

    # Check Python major version
    python_version_major = re.match(r"\d+\.\d+", sys.version).group(0)
    if python_version_major != required_python_version:
        incompatibilities.append(
            f"**CRITICAL: Python major version {required_python_version} is required, but you are using {python_version_major}.**"
        )

    table_rows = []
    table_rows.append("| Package | Current Version | Required Version | Mismatch |")
    table_rows.append("| ------- | --------------- | ----------------- | -------- |")

    for req in requirements:
        req_obj = Requirement(req)
        pkg_name = req_obj.name

        if pkg_name in installed_packages:
            installed_version = installed_packages[pkg_name]
            mismatch = not req_obj.specifier.contains(installed_version)
            table_rows.append(
                f"| {pkg_name} | {installed_version} | {str(req_obj.specifier)} | {str(mismatch)} |"
            )
        else:
            table_rows.append(f"| {pkg_name} | - | {str(req_obj.specifier)} | True |")

    teams_message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FF0000",
        "summary": "Package Compatibility Alert",
        "sections": [
            {
                "activityTitle": "Incompatibilities Found:",
                "text": "\n".join(table_rows),
            }
        ],
    }

    try:
        response = requests.post(teams_webhook_url, json=teams_message, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        sys.exit(f"Error sending Teams message: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise AttributeError(
            "Usage: python check_conda_env.py <env_name> <requirements_file> <required_python_version> <teams_webhook_url>"
        )

    env_name_ = sys.argv[1]
    requirements_file_ = sys.argv[2]
    required_python_version_ = sys.argv[3]
    TEAMS_WEBHOOK_URL = sys.argv[4]

    check_env_compatibility(
        env_name=env_name_,
        requirements_file=requirements_file_,
        required_python_version=required_python_version_,
        teams_webhook_url=TEAMS_WEBHOOK_URL,
    )
    print("Done")
