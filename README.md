# Blackduck Inactive Project Versions and Users Management

This repository contains scripts to manage inactive project versions and users in Blackduck hub. The scripts can authenticate to the Blackduck hub, look for inactive project versions and users, and provide options to archive or delete them. The default behavior is to list them and the number of days since their last activity.

## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/blackduck-management.git
   cd blackduck-management
   ```

2. Install the required dependencies:

   ```sh
   pip install requests
   ```

## Usage

### Inactive Project Versions

The `inactive_project_versions.py` script can be used to manage inactive project versions.

#### Command-line Arguments

- `--hub-url`: The URL of the Blackduck hub (required).
- `--access-token`: The access token for authentication (required).
- `--days-inactive`: Number of days to check for inactivity (required).
- `--archive`: Archive inactive project versions (optional).
- `--delete`: Delete project versions instead of archiving them (optional).

#### Example

```sh
python inactive_project_versions.py --hub-url <HUB_URL> --access-token <ACCESS_TOKEN> --days-inactive 30
```

### Inactive Users

The `inactive_user.py` script can be used to manage inactive users.

#### Command-line Arguments

- `--hub-url`: The URL of the Blackduck hub (required).
- `--access-token`: The access token for authentication (required).
- `--days-inactive`: Number of days to check for inactivity (required).
- `--deactivate`: Deactivate inactive users (optional).
- `--delete`: Delete users instead of deactivating them (optional).

#### Example

```sh
python inactive_user.py --hub-url <HUB_URL> --access-token <ACCESS_TOKEN> --days-inactive 30
```

## Project Structure

```
blackduck-management/
│
├── blackduck_utils/
│   ├── __init__.py
│   ├── auth.py
│   ├── projects.py
│   └── users.py
├── scripts/
│   ├── inactive_user.py
│   └── inactive_project_versions.py
├── README.md
└── setup.py
```

### `blackduck_utils/auth.py`

Contains the `BearerAuth` class for authenticating with the Blackduck hub.

### `blackduck_utils/projects.py`

Contains functions for managing project versions:
- `get_project_versions`
- `find_inactive_project_versions`
- `archive_project_version`
- `delete_project_version`

### `blackduck_utils/users.py`

Contains functions for managing users:
- `get_users`
- `find_inactive_users`
- `deactivate_user`
- `delete_user`

## License

This project is licensed under the MIT License.
```

### Explanation

1. **Prerequisites**: Lists the required Python version and dependencies.
2. **Installation**: Provides instructions to clone the repository and install dependencies.
3. **Usage**: Describes how to use the inactive_project_versions.py and inactive_user.py scripts, including command-line arguments and examples.
4. **Project Structure**: Explains the structure of the project and the purpose of each file.
5. **License**: Specifies the license for the project.

This README should help users understand how to set up and use the scripts to manage inactive project versions and users in the Blackduck hub.
