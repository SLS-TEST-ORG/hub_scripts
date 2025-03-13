import pytest
import requests
from datetime import datetime, timedelta
from blackduck_utils.projects import get_project_versions, find_inactive_project_versions

@pytest.fixture
def mock_session(mocker):
    session = requests.Session()
    mocker.patch.object(session, 'get')
    return session

def test_get_project_versions(mock_session):
    mock_session.get.side_effect = [
        # First call to get projects
        mocker.Mock(status_code=200, json=lambda: {
            'items': [
                {'_meta': {'href': 'http://example.com/project1'}, 'name': 'Project1'},
                {'_meta': {'href': 'http://example.com/project2'}, 'name': 'Project2'}
            ]
        }),
        # Second call to get versions for project1
        mocker.Mock(status_code=200, json=lambda: {
            'items': [
                {'versionName': 'v1', 'lastScanDate': '2022-01-01T00:00:00.000Z'}
            ]
        }),
        # Third call to get versions for project2
        mocker.Mock(status_code=200, json=lambda: {
            'items': [
                {'versionName': 'v2', 'lastScanDate': '2023-01-01T00:00:00.000Z'}
            ]
        })
    ]
    auth = None  # Replace with appropriate AuthBase instance
    hub_url = 'http://example.com'
    project_versions = get_project_versions(mock_session, auth, hub_url)
    assert len(project_versions) == 2
    assert project_versions[0]['versionName'] == 'v1'
    assert project_versions[1]['versionName'] == 'v2'

def test_find_inactive_project_versions():
    versions = [
        {'versionName': 'v1', 'lastScanDate': '2022-01-01T00:00:00.000Z'},
        {'versionName': 'v2', 'lastScanDate': '2023-01-01T00:00:00.000Z'}
    ]
    days_inactive = 365
    cutoff_date = datetime.now() - timedelta(days=days_inactive)
    inactive_versions = find_inactive_project_versions(versions, days_inactive)
    assert len(inactive_versions) == 1
    assert inactive_versions[0]['versionName'] == 'v1'