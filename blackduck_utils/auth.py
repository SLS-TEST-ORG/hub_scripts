import requests
from requests.auth import AuthBase
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

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
