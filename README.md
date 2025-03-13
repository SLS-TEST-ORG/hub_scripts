# Hub Scripts

This repository contains scripts for managing inactive project versions and users in the Blackduck hub. The scripts can archive or delete inactive project versions and deactivate or delete inactive users based on a specified number of days of inactivity. Created by dc-moses dylanm@blackduck.com for questions. 

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/hub-scripts.git
    cd hub-scripts
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

## Usage

### Inactive Project Versions

The `inactive_project_versions.py` script can archive or delete inactive project versions from the Blackduck hub.

```sh
python inactive_project_versions.py --hub-url <HUB_URL> --access-token <ACCESS_TOKEN> --days-inactive <DAYS_INACTIVE> [--archive | --delete] [--log-level <LOG_LEVEL>]
```

- `--hub-url`: Blackduck hub URL
- `--access-token`: Access token for authentication
- `--days-inactive`: Number of days to check for inactivity
- `--archive`: Archive inactive project versions
- `--delete`: Delete project versions instead of archiving them
- `--log-level`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Inactive Users

The `inactive_user.py` script can deactivate or delete inactive users from the Blackduck hub.

```sh
python inactive_user.py --hub-url <HUB_URL> --access-token <ACCESS_TOKEN> --days-inactive <DAYS_INACTIVE> [--deactivate | --delete] [--log-level <LOG_LEVEL>]
```

- `--hub-url`: Blackduck hub URL
- `--access-token`: Access token for authentication
- `--days-inactive`: Number of days to check for inactivity
- `--deactivate`: Deactivate inactive users
- `--delete`: Delete users instead of deactivating them
- `--log-level`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Testing

To run the tests, use the following command:

```sh
pytest -v
```

Ensure that you have the `pytest` and `pytest-mock` packages installed. The tests are located in the `tests` directory.

### Example Test Files

- `tests/test_projects.py`: Tests for project-related functionality.
- `tests/test_users.py`: Tests for user-related functionality.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
