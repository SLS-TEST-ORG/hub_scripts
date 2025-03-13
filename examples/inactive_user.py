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
    parser = argparse.ArgumentParser(description="Deactivate or delete inactive users from Blackduck hub.")
    parser.add_argument('--hub-url', type=str, required=True, help='Blackduck hub URL')
    parser.add_argument('--access-token', type=str, required=True, help='Access token for authentication')
    parser.add_argument('--days-inactive', type=int, required=True, help='Number of days to check for inactivity')
    parser.add_argument('--deactivate', action='store_true', help='Deactivate inactive users')
    parser.add_argument('--delete', action='store_true', help='Delete users instead of deactivating them')
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

        response = self.session.post(
            url=f"{self.hub_url}/api/tokens/authenticate",
            auth=NoAuth(),
            headers={"Authorization": f"token {self.access_token}"}
        )

        if response.status_code == 200:
            try:
                content = response.json()
                self.bearer_token = content['bearerToken']
                self.csrf_token = response.headers['X-CSRF-TOKEN']
                self.valid_until = datetime.now() + timedelta(milliseconds=int(content['expiresInMilliseconds']))
                logger.info(f"Success: Auth granted until {self.valid_until.astimezone()}")
                return
            except (json.JSONDecodeError, KeyError):
                logger.exception("HTTP response status code 200 but unable to obtain bearer token")

        if response.status_code == 401:
            logger.error("HTTP response status code = 401 (Unauthorized)")
            try:
                logger.error(response.json()['errorMessage'])
            except (json.JSONDecodeError, KeyError):
                logger.exception("Unable to extract error message")
                logger.error("HTTP response headers: %s", response.headers)
                logger.error("HTTP response text: %s", response.text)
            raise RuntimeError("Unauthorized access token", response)

        logger.error("Unhandled HTTP response")
        logger.error("HTTP response status code %i", response.status_code)
        logger.error("HTTP response headers: %s", response.headers)
        logger.error("HTTP response text: %s", response.text)
        raise RuntimeError("Unhandled HTTP response", response)

def get_users(session: requests.Session, auth: AuthBase, hub_url: str) -> List[Dict[str, Any]]:
    """Fetch users from the Blackduck hub."""
    response = session.get(f"{hub_url}/api/users", auth=auth)
    if response.status_code == 401:
        logger.error("Unauthorized access - check your API token and URL.")
        return []
    response.raise_for_status()
    return response.json().get('items', [])

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

def deactivate_user(session: requests.Session, auth: AuthBase, user: Dict[str, Any], hub_url: str):
    """Deactivate a user."""
    url = f"{hub_url}/api/users/{user['userName']}/deactivate"
    response = session.post(url, auth=auth)
    if response.status_code == 204:
        logger.info(f"User {user['userName']} deactivated successfully.")
    else:
        logger.error(f"Failed to deactivate user {user['userName']}. Status code: {response.status_code}")

def delete_user(session: requests.Session, auth: AuthBase, user: Dict[str, Any], hub_url: str):
    """Delete a user."""
    url = f"{hub_url}/api/users/{user['userName']}"
    response = session.delete(url, auth=auth)
    if response.status_code == 204:
        logger.info(f"User {user['userName']} deleted successfully.")
    else:
        logger.error(f"Failed to delete user {user['userName']}. Status code: {response.status_code}")

def main():
    """Main function to execute the script."""
    args = parse_args()

    with requests.Session() as session:
        try:
            auth = BearerAuth(session, args.access_token, args.hub_url)
            users = get_users(session, auth, args.hub_url)
            logger.info(f"Total users fetched: {len(users)}")
            if not users:
                logger.info("No users found or unable to fetch users.")
                return
            inactive_users = find_inactive_users(users, args.days_inactive)
            logger.info(f"Total inactive users found: {len(inactive_users)}")
            logger.info(f"Users inactive for more than {args.days_inactive} days:")
            for user in inactive_users:
                logger.info(f"Username: {user['userName']}, Last Login: {user.get('lastLogin', 'Never')}")
            if args.deactivate or args.delete:
                for user in inactive_users:
                    if args.delete:
                        delete_user(session, auth, user, args.hub_url)
                    elif args.deactivate:
                        deactivate_user(session, auth, user, args.hub_url)
        except Exception as e:
            logger.exception("An error occurred during execution")

if __name__ == "__main__":
    main()
