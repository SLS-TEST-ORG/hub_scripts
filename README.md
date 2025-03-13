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

## Usage

Run the script with the desired command-line arguments:

```sh
python inactive_user.py --hub-url <HUB_URL> --access-token <ACCESS_TOKEN> --days-inactive <DAYS_INACTIVE> [--deactivate] [--delete]
```

### Command-Line Arguments

- `--hub-url`: The URL of the Blackduck hub (required).
- `--access-token`: The access token for authentication (required).
- `--days-inactive`: Number of days to check for inactivity (required).
- `--deactivate`: Deactivate inactive users (optional).
- `--delete`: Delete users instead of deactivating them (optional).

### Examples

1. **Check for inactive users without performing any cleanup:**

    ```sh
    python inactive_user.py --hub-url https://your-blackduck-hub-url --access-token your-access-token --days-inactive 180
    ```

2. **Deactivate users who have been inactive for more than 180 days:**

    ```sh
    python inactive_user.py --hub-url https://your-blackduck-hub-url --access-token your-access-token --days-inactive 180 --deactivate
    ```

3. **Delete users who have been inactive for more than 180 days:**

    ```sh
    python inactive_user.py --hub-url https://your-blackduck-hub-url --access-token your-access-token --days-inactive 180 --delete
    ```

## Logging

The script uses Python's built-in logging module to log information and errors. Logs are printed to the console.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
