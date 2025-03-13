# Inactive User Cleanup Script

This script deactivates or deletes inactive users from the Blackduck hub based on the specified number of days of inactivity.

## Prerequisites

- Python 3.6+
- `requests` library

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies using pip:

    ```sh
    pip install requests
    ```

## Environment Variables

Ensure the following environment variables are set:

- `HUB_URL`: The URL of the Blackduck hub.
- `ACCESS_TOKEN`: The access token for authentication.

## Usage

Run the script with the desired command-line arguments:

```sh
python [inactive_user.py](http://_vscodecontentref_/0) --days-inactive 180 --clean-up --delete
