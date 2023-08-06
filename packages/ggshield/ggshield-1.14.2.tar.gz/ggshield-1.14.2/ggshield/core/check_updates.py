import logging
import os.path
import time
from typing import Optional, Tuple

import requests

from ggshield import __version__
from ggshield.core.dirs import get_cache_dir

from .config.utils import load_yaml_dict, save_yaml_dict


logger = logging.getLogger(__name__)
CACHE_FILE = os.path.join(
    get_cache_dir(),
    "update_check.yaml",
)


# Use a short timeout to prevent blocking
CHECK_TIMEOUT = 5


def _split_version(version: str) -> Tuple[int, ...]:
    return tuple([int(x) for x in version.split(".")])


def check_for_updates() -> Optional[str]:
    """
    Check for ggshield updates on GitHub. Return the latest version if available.
    Query GitHub API at most once per day and save locally the latest version in a file.
    """
    check_at = -1.0
    # Load the last time we checked
    try:
        cached_data = load_yaml_dict(CACHE_FILE)
    except ValueError:
        # Swallow the error
        cached_data = None
    if cached_data is not None:
        try:
            check_at = cached_data["check_at"]
        except Exception as e:
            logger.warning("Could not load cached latest version: %s", e)

    if check_at > 0 and (time.time() - check_at < 24 * 60 * 60):
        # We checked today, no need to check again
        return None

    logger.debug("Checking the latest released version of ggshield...")

    # Save check time now so that it is saved even if the check fails. This ensures we
    # don't try for every command if the user does not have network access.
    try:
        save_yaml_dict({"check_at": time.time()}, CACHE_FILE)
    except Exception as e:
        logger.error("Could not save time of version check to cache: %s", e)
        # Do not continue if we can't save check time. If we continue we are going to
        # send requests to api.github.com every time ggshield is called.
        return None

    try:
        resp = requests.get(
            "https://api.github.com/repos/GitGuardian/GGShield/releases/latest",
            timeout=CHECK_TIMEOUT,
        )
    except Exception as e:
        logger.error("Failed to connect to api.github.com: %s", e)
        return None

    if resp.status_code != 200:
        logger.error("Failed to check: %s", resp.text)
        return None

    try:
        data = resp.json()
        latest_version: str = data["tag_name"][1:]

        current_version_split = _split_version(__version__)
        latest_version_split = _split_version(latest_version)
    except Exception as e:
        logger.error("Failed to parse response: %s", e)
        return None

    if current_version_split < latest_version_split:
        return latest_version
    return None
