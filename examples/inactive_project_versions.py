import requests
from requests.auth import AuthBase
import logging
from datetime import datetime, timedelta
import argparse
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Archive or delete inactive project versions from Blackduck hub.")
    parser.add_argument('--hub-url', type=str, required=True, help='Blackduck hub URL')
    parser.add_argument('--access-token', type=str, required=True, help='Access token for authentication')
    parser.add_argument('--days-inactive', type=int, required=True, help='Number of days to check for inactivity')
    parser.add_argument('--archive', action='store_true', help='Archive inactive project versions')
    parser.add_argument('--delete', action='store_true', help='Delete project versions instead of archiving them')
    return parser.parse_args()

class NoAuth(AuthBase):
    def __call__(self, r):
        return r

class BearerAuth(AuthBase):
    """Authenticate with Blackduck hub using access token"""

    def __init__(self, session: requests.Session, token: str, hub_url: str):
        if not session or not token or not hub_url:
            raise ValueError('session, token, and hub_url are required')

        self.session = session
        self.access_token = token
        self.hub_url = hub_url
        self.bearer_token = None
        self.csrf_token = None
        self.valid_until = datetime.now()

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        if not self.bearer_token or datetime.now() > self.valid_until - timedelta(minutes=5):
            self.authenticate()

        request.headers.update({
            "authorization": f"bearer {self.bearer_token}",
            "X-CSRF-TOKEN": self.csrf_token
        })

        return request

    def authenticate(self):
        if not self.session.verify:
            requests.packages.urllib3.disable_warnings()
            logger.warning("SSL verification disabled, connection insecure. Do verify=False in production!")

        try:
            response = self.session.post(
                url=f"{self.hub_url}/api/tokens/authenticate",
                auth=NoAuth(),
                headers={"Authorization": f"token {self.access_token}"}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Invalid URL or network issue.")
            raise RuntimeError("Invalid URL or network issue.") from e

        if response.status_code == 200:
            try:
                content = response.json()
                self.bearer_token = content['bearerToken']
                self.csrf_token = response.headers['X-CSRF-TOKEN']
                self.valid_until = datetime.now() + timedelta(milliseconds=int(content['expiresInMilliseconds']))
                logger.info(f"Success: Auth granted until {self.valid_until.astimezone()}")
            except (json.JSONDecodeError, KeyError):
                logger.exception("HTTP response status code 200 but unable to obtain bearer token")
                raise RuntimeError("Failed to parse authentication response")

        elif response.status_code == 401:
            logger.error("HTTP response status code = 401 (Unauthorized)")
            try:
                logger.error(response.json()['errorMessage'])
            except (json.JSONDecodeError, KeyError):
                logger.exception("Unable to extract error message")
                logger.error("HTTP response headers: %s", response.headers)
                logger.error("HTTP response text: %s", response.text)
            raise RuntimeError("Unauthorized access token", response)

        else:
            logger.error("Unhandled HTTP response")
            logger.error("HTTP response status code %i", response.status_code)
            logger.error("HTTP response headers: %s", response.headers)
            logger.error("HTTP response text: %s", response.text)
            raise RuntimeError("Unhandled HTTP response", response)

def get_project_versions(session: requests.Session, auth: AuthBase, hub_url: str) -> List[Dict[str, Any]]:
    """Fetch project versions from the Blackduck hub, handling pagination."""
    project_versions = []
    url = f"{hub_url}/api/projects"
    params = {'offset': 0, 'limit': 100}  # Adjust limit as needed

    while True:
        try:
            response = session.get(url, auth=auth, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Invalid URL or network issue.")
            raise RuntimeError("Invalid URL or network issue.") from e

        if response.status_code == 401:
            logger.error("Unauthorized access - check your API token and URL.")
            break

        data = response.json()
        items = data.get('items', [])
        for project in items:
            project_url = project['_meta']['href']
            project_name = project['name']
            project_versions.extend(get_versions_for_project(session, auth, project_url, project_name))

        if len(items) < params['limit']:
            break  # No more pages

        params['offset'] += params['limit']

    return project_versions

def get_versions_for_project(session: requests.Session, auth: AuthBase, project_url: str, project_name: str) -> List[Dict[str, Any]]:
    """Fetch versions for a specific project."""
    versions = []
    url = f"{project_url}/versions"
    params = {'offset': 0, 'limit': 100}  # Adjust limit as needed

    while True:
        try:
            response = session.get(url, auth=auth, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Invalid URL or network issue.")
            raise RuntimeError("Invalid URL or network issue.") from e

        if response.status_code == 401:
            logger.error("Unauthorized access - check your API token and URL.")
            break

        data = response.json()
        items = data.get('items', [])
        for version in items:
            version['projectName'] = project_name
        versions.extend(items)

        if len(items) < params['limit']:
            break  # No more pages

        params['offset'] += params['limit']

    return versions

def find_inactive_project_versions(versions: List[Dict[str, Any]], days_inactive: int) -> List[Dict[str, Any]]:
    """Find project versions that have been inactive for a specified number of days."""
    inactive_versions = []
    cutoff_date = datetime.now() - timedelta(days=days_inactive)
    for version in versions:
        last_scan = version.get('lastScanDate')
        if last_scan:
            last_scan_date = datetime.strptime(last_scan, '%Y-%m-%dT%H:%M:%S.%fZ')
            if last_scan_date < cutoff_date:
                inactive_versions.append(version)
        else:
            inactive_versions.append(version)  # Versions that never had a scan
    return inactive_versions

def archive_project_version(session: requests.Session, auth: AuthBase, version: Dict[str, Any], hub_url: str):
    """Archive a project version."""
    url = f"{hub_url}/api/projects/{version['projectId']}/versions/{version['versionId']}/archive"
    response = session.post(url, auth=auth)
    if response.status_code == 204:
        logger.info(f"Project version {version['versionName']} archived successfully.")
    else:
        logger.error(f"Failed to archive project version {version['versionName']}. Status code: {response.status_code}")

def delete_project_version(session: requests.Session, auth: AuthBase, version: Dict[str, Any], hub_url: str):
    """Delete a project version."""
    url = f"{hub_url}/api/projects/{version['projectId']}/versions/{version['versionId']}"
    response = session.delete(url, auth=auth)
    if response.status_code == 204:
        logger.info(f"Project version {version['versionName']} deleted successfully.")
    else:
        logger.error(f"Failed to delete project version {version['versionName']}. Status code: {response.status_code}")

def main():
    """Main function to execute the script."""
    args = parse_args()

    with requests.Session() as session:
        try:
            auth = BearerAuth(session, args.access_token, args.hub_url)
            project_versions = get_project_versions(session, auth, args.hub_url)
            logger.info(f"Total project versions fetched: {len(project_versions)}")
            if not project_versions:
                logger.info("No project versions found or unable to fetch project versions.")
                return
            inactive_versions = find_inactive_project_versions(project_versions, args.days_inactive)
            logger.info(f"Total inactive project versions found: {len(inactive_versions)}")
            logger.info(f"Project versions inactive for more than {args.days_inactive} days:")
            for version in inactive_versions:
                last_scan = version.get('lastScanDate', 'Never')
                logger.info(f"Project: {version['projectName']}, Version: {version['versionName']}, Last Scan: {last_scan}")
            if args.archive or args.delete:
                for version in inactive_versions:
                    if args.delete:
                        delete_project_version(session, auth, version, args.hub_url)
                    elif args.archive:
                        archive_project_version(session, auth, version, args.hub_url)
        except RuntimeError as e:
            logger.error(e)
        except Exception as e:
            logger.exception("An error occurred during execution")

if __name__ == "__main__":
    main()
