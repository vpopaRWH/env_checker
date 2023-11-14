Module track_system_usage
=========================
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

Functions
---------

    
`track_system_resources(teams_webhook_url)`
:   Track memory, CPU, and RAM usage on a machine and send the information to Microsoft Teams.
    
    Args:
        teams_webhook_url (str): Microsoft Teams webhook URL.