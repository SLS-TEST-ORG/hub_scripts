import requests
import logging
from datetime import datetime, timedelta
import argparse
from typing import List, Dict, Any
from blackduck_utils import BearerAuth, get_project_versions, find_inactive_project_versions, archive_project_version, delete_project_version

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
