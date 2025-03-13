import requests
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from blackduck_utils.auth import AuthBase  

logger = logging.getLogger(__name__)

def get_users(session: requests.Session, auth: AuthBase, hub_url: str) -> List[Dict[str, Any]]:
    """Fetch users from the Blackduck hub, handling pagination."""
    users = []
    url = f"{hub_url}/api/users"
    params = {'offset': 0, 'limit': 100}  # Adjust limit as needed

    while True:
        try:
            response = session.get(url, auth=auth, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch users: {e}")
            raise RuntimeError("Failed to fetch users.") from e

        if response.status_code == 401:
            logger.error("Unauthorized access - check your API token and URL.")
            break

        data = response.json()
        items = data.get('items', [])
        users.extend(items)

        if len(items) < params['limit']:
            break  # No more pages

        params['offset'] += params['limit']

    return users

def find_inactive_users(users: List[Dict[str, Any]], days_inactive: int) -> List[Dict[str, Any]]:
    """Find users who have been inactive for a specified number of days."""
    inactive_users = []
    cutoff_date = datetime.now() - timedelta(days=days_inactive)
    for user in users:
        last_login = user.get('lastLogin')
        if last_login:
            last_login_date = datetime.strptime(last_login, '%Y-%m-%dT%H:%M:%S.%fZ')
            if last_login_date < cutoff_date:
                inactive_users.append(user)
        else:
            inactive_users.append(user)  # Users who never logged in
    return inactive_users

def deactivate_user(session: requests.Session, auth: AuthBase, user: Dict[str, Any], hub_url: str) -> None:
    """Deactivate a user."""
    url = f"{hub_url}/api/users/{user['userName']}/deactivate"
    try:
        response = session.post(url, auth=auth)
        response.raise_for_status()
        logger.info(f"User {user['userName']} deactivated successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to deactivate user {user['userName']}: {e}")

def delete_user(session: requests.Session, auth: AuthBase, user: Dict[str, Any], hub_url: str) -> None:
    """Delete a user."""
    url = f"{hub_url}/api/users/{user['userName']}"
    try:
        response = session.delete(url, auth=auth)
        response.raise_for_status()
        logger.info(f"User {user['userName']} deleted successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to delete user {user['userName']}: {e}")
