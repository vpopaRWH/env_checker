# Conda Environment Compatibility Checker

**check_conda_env.py** is a Python script designed to check the compatibility of installed packages in a Conda environment with the versions specified in a requirements file. If any incompatibilities are found, it sends an alert to a Microsoft Teams webhook.

## Usage

### Parameters

- `env_name` (str): Name of the Conda environment to be checked.
- `requirements_file` (str): Path to the requirements file containing package requirements.
- `required_python_version` (str): Required Python version (major version only).

### Steps

1. Activate the specified Conda environment.
2. Retrieve a list of installed packages and their versions in the environment using 'pip freeze.'
3. Compare the installed packages with the requirements specified in the requirements file.
4. Check for compatibility issues, including Python major version mismatch.
5. Send an alert to a Microsoft Teams webhook if incompatibilities are found.

## Dependencies

The script uses the following Python libraries:

- `subprocess`
- `re`
- `sys`
- `packaging.requirements`
- `requests`
