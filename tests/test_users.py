import pytest
import requests
from blackduck_utils.users import get_users, find_inactive_users

@pytest.fixture
def mock_session(mocker):
    session = requests.Session()
    mocker.patch.object(session, 'get')
    return session

def test_get_users(mock_session):
    mock_session.get.return_value.json.return_value = {
        'items': [
            {'userName': 'user1', 'lastLogin': '2022-01-01T00:00:00.000Z'},
            {'userName': 'user2', 'lastLogin': '2023-01-01T00:00:00.000Z'}
        ]
    }
    mock_session.get.return_value.status_code = 200
    auth = None  # Replace with appropriate AuthBase instance
    hub_url = 'http://example.com'
    users = get_users(mock_session, auth, hub_url)
    assert len(users) == 2

def test_find_inactive_users():
    users = [
        {'userName': 'user1', 'lastLogin': '2022-01-01T00:00:00.000Z'},
        {'userName': 'user2', 'lastLogin': '2023-01-01T00:00:00.000Z'}
    ]
    days_inactive = 365
    inactive_users = find_inactive_users(users, days_inactive)
    assert len(inactive_users) == 1
    assert inactive_users[0]['userName'] == 'user1'