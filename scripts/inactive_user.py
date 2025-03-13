import requests
import logging
import argparse
from typing import Any
from blackduck_utils.auth import BearerAuth
from blackduck_utils.users import get_users, find_inactive_users, deactivate_user, delete_user

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
    parser.add_argument('--log-level', type=str, default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    args = parser.parse_args()

    if args.deactivate and args.delete:
        parser.error("Specify either --deactivate or --delete, not both.")
    
    return args

def main() -> None:
    """Main function to execute the script."""
    args = parse_args()
    logging.getLogger().setLevel(args.log_level.upper())

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
        except RuntimeError as e:
            logger.error(e)
        except Exception as e:
            logger.exception("An error occurred during execution")

if __name__ == "__main__":
    main()
