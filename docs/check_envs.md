Module check_envs
=================

check_conda_env.py

This script checks the compatibility of installed packages in a Conda environment with the versions specified in a requirements file. If any incompatibilities are found, it sends an alert to a Microsoft Teams webhook.

Usage:
    python check_conda_env.py <env_name> <requirements_file> <required_python_version>

Parameters:
    - env_name (str): Name of the Conda environment to be checked.
    - requirements_file (str): Path to the requirements file containing package requirements.
    - required_python_version (str): Required Python version (major version only).

The script performs the following steps:

1. Activates the specified Conda environment.
2. Retrieves a list of installed packages and their versions in the environment using 'pip freeze.'
3. Compares the installed packages with the requirements specified in the requirements file.
4. Checks for compatibility issues, including Python major version mismatch.
5. Sends an alert to a Microsoft Teams webhook if incompatibilities are found.

The Microsoft Teams alert message includes details about the incompatibilities detected.

To run the script, provide the necessary command-line arguments as specified in the 'Usage' section.

Dependencies:

- The script uses the 'subprocess', 're', 'sys', 'packaging.requirements', and 'requests' modules.
Author: [Your Name]
Date: [Date]

Functions
---------

`check_env_compatibility(env_name: str, requirements_file: str, teams_webhook_url: str, required_python_version: str) ‑> None`
:   Check compatibility of installed packages in a Conda environment with the versions specified in the requirements file.
    Send an alert to a Microsoft Teams webhook with incompatibilities found.

    Args:
        env_name (str): Name of the Conda environment.
        requirements_file (str): Path to the requirements file.
        teams_webhook_url (str): Microsoft Teams webhook URL.
        required_python_version (str): Required Python version (major version only).

`get_installed_packages(env_name: str, teams_webhook_url: str) ‑> dict[str, str]`
:   Get a dictionary of installed packages and their versions in a Conda environment.

    Args:
        env_name (str): Name of the Conda environment.

    Returns:
        dict[str, str]: Dictionary of installed packages and their versions.

`parse_requirements_file(requirements_file: str) ‑> list[str]`
:   Parse a requirements file and return a list of requirements.

    Args:
        requirements_file (str): Path to the requirements file.

    Returns:
        list[str]: List of requirements.
