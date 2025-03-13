import requests
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from blackduck_utils.auth import AuthBase

logger = logging.getLogger(__name__)

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
            logger.error(f"Failed to fetch project versions: {e}")
            raise RuntimeError("Failed to fetch project versions.") from e

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
            logger.error(f"Failed to fetch versions for project {project_name}: {e}")
            raise RuntimeError(f"Failed to fetch versions for project {project_name}.") from e

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

def archive_project_version(session: requests.Session, auth: AuthBase, version: Dict[str, Any], hub_url: str) -> None:
    """Archive a project version."""
    url = f"{hub_url}/api/projects/{version['projectId']}/versions/{version['versionId']}/archive"
    try:
        response = session.post(url, auth=auth)
        response.raise_for_status()
        logger.info(f"Project version {version['versionName']} archived successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to archive project version {version['versionName']}: {e}")

def delete_project_version(session: requests.Session, auth: AuthBase, version: Dict[str, Any], hub_url: str) -> None:
    """Delete a project version."""
    url = f"{hub_url}/api/projects/{version['projectId']}/versions/{version['versionId']}"
    try:
        response = session.delete(url, auth=auth)
        response.raise_for_status()
        logger.info(f"Project version {version['versionName']} deleted successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to delete project version {version['versionName']}: {e}")
