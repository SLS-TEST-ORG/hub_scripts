# Blackduck Inactive Project Versions and Users Management

This repository contains scripts to manage inactive project versions and users in Blackduck hub. The scripts can authenticate to the Blackduck hub, look for inactive project versions and users, and provide options to archive or delete them. The default behavior is to list them and the number of days since their last activity.

## Prerequisites

- Python 3.6 or higher
- `requests` library
- `pyyaml` library

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/blackduck-management.git
   cd blackduck-management
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
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
python inactive_user.py --hub-url <HUB_URL> --access-token <ACCESS_TOKEN> --days-inactive 30 --deactivate
```

### Configuration File Support

You can also use a configuration file to specify the command-line arguments. Create a `config.yaml` file with the following structure:

```yaml
hub_url: <HUB_URL>
access_token: <ACCESS_TOKEN>
days_inactive: 30
deactivate: true
delete: false
```

Then run the script with the `--config` argument:

```sh
python inactive_user.py --config config.yaml
```

## Logging

The scripts use Python's built-in logging module to log information. By default, the logging level is set to `INFO`. You can change the logging level by modifying the `logging.basicConfig(level=logging.INFO)` line in the script.

## Testing

Unit tests are provided in the `tests` directory. To run the tests, use the following command:

```sh
pytest
```

## Continuous Integration

This project uses GitHub Actions for continuous integration. The CI configuration is located in the `.github/workflows/ci.yml` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Contact

For any questions or issues, please contact Dylan at dylanm@blackduck.com.