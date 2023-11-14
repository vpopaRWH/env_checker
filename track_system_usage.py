"""
track_system_resources.py

This module provides a function to track memory, CPU, and RAM usage on a machine and send the information to Microsoft Teams.

Usage:
    python track_system_resources.py <teams_webhook_url>

Parameters:
    - teams_webhook_url (str): Microsoft Teams webhook URL.

The module defines the following function:
- track_system_resources(teams_webhook_url): Track memory, CPU, and RAM usage and send the information to Microsoft Teams.

Dependencies:
- The module requires the 'psutil' and 'requests' libraries. Install them using:
    ```
    pip install psutil requests
    ```

Example:
    ```python
    from track_system_resources import track_system_resources

    # Replace 'YOUR_TEAMS_WEBHOOK_URL' with your actual Teams webhook URL
    TEAMS_WEBHOOK_URL = 'YOUR_TEAMS_WEBHOOK_URL'

    track_system_resources(TEAMS_WEBHOOK_URL)
    ```

Author: [Your Name]
Date: [Date]
"""
import socket
import psutil
import requests


def track_system_resources(teams_webhook_url):
    """
    Track memory, CPU, and RAM usage on a machine and send the information to Microsoft Teams.

    Args:
        teams_webhook_url (str): Microsoft Teams webhook URL.
    """
    # Get CPU usage
    machine_name = socket.gethostname()
    cpu_percent = psutil.cpu_percent()

    # Get memory usage
    memory_info = psutil.virtual_memory()
    used_memory_percent = memory_info.percent

    # Get RAM usage
    ram_info = psutil.swap_memory()
    used_ram_percent = ram_info.percent

    # Format the information as a markdown table
    markdown_table = (
        "| Metric | Usage |\n"
        "| ------- | ----- |\n"
        f"| Machine     | {machine_name}% |\n"
        f"| CPU     | {cpu_percent}% |\n"
        f"| Memory  | {used_memory_percent}% |\n"
        f"| RAM     | {used_ram_percent}% |"
    )

    # Send the information to Microsoft Teams
    teams_message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "008000",  # Green theme color
        "summary": "System Resource Usage",
        "sections": [
            {
                "activityTitle": "System Resource Usage",
                "markdown": True,
                "text": markdown_table,
            }
        ],
    }

    try:
        response = requests.post(teams_webhook_url, json=teams_message, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Teams message: {str(e)}")


if __name__ == "__main__":
    TEAMS_WEBHOOK_URL = ""
    track_system_resources(TEAMS_WEBHOOK_URL)
