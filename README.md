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
python inactive_user.py --days-inactive 180 --clean-up --delete
```

### Command-Line Arguments

- `--days-inactive`: Number of days to check for inactivity (default: 180).
- `--clean-up`: Deactivate or delete inactive users.
- `--delete`: Delete users instead of deactivating them.
- `--no-clean-up`: Do not perform any cleanup.

### Examples

1. **Check for inactive users without performing any cleanup:**

    ```sh
    python inactive_user.py --days-inactive 180 --no-clean-up
    ```

2. **Deactivate users who have been inactive for more than 180 days:**

    ```sh
    python inactive_user.py --days-inactive 180 --clean-up
    ```

3. **Delete users who have been inactive for more than 180 days:**

    ```sh
    python inactive_user.py --days-inactive 180 --clean-up --delete
    ```

## Logging

The script uses Python's built-in logging module to log information and errors. Logs are printed to the console.

## License

This project is licensed under the MIT License.
