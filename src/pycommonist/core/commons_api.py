"""Authenticated HTTP client helpers for the Wikimedia Commons API.

Security notes:
- Every request carries a descriptive User-Agent (Wikimedia API policy).
- Every request has an explicit timeout so the UI can never hang forever.
- Credentials and tokens are never written to the logs.
- Bot passwords (username of the form ``User@BotName``) use ``action=login``,
  as recommended by MediaWiki; regular accounts use ``action=clientlogin``.
- Authenticated requests use ``assert=user`` so a silently expired session
  fails loudly instead of uploading anonymously.
"""

import logging

import requests

from pycommonist.core.constants import PYCOMMONIST_VERSION, URL

logger = logging.getLogger(__name__)

USER_AGENT = (
    f"PyCommonist/{PYCOMMONIST_VERSION} "
    "(https://github.com/thepriben/PyCommonist)"
)

# (connect, read) timeouts in seconds.
DEFAULT_TIMEOUT = (10, 30)
UPLOAD_TIMEOUT = (10, 600)


def create_http_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def _fetch_token(http_session: requests.Session, token_type: str) -> str:
    params = {
        "action": "query",
        "meta": "tokens",
        "type": token_type,
        "format": "json",
    }
    if token_type == "csrf":
        params["assert"] = "user"
    response = http_session.get(URL, params=params, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()["query"]["tokens"][f"{token_type}token"]


def login(http_session: requests.Session, username: str, password: str):
    """Authenticate against Commons. Returns ``(ok, message)``.

    Never logs or returns the password or any token.
    """
    try:
        login_token = _fetch_token(http_session, "login")
    except (requests.RequestException, KeyError, ValueError):
        logger.exception("Could not fetch login token")
        return False, "Network error: could not reach Wikimedia Commons"

    is_bot_password = "@" in username
    try:
        if is_bot_password:
            data = {
                "action": "login",
                "lgname": username,
                "lgpassword": password,
                "lgtoken": login_token,
                "format": "json",
            }
            response = http_session.post(URL, data=data, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            result = response.json().get("login", {})
            if result.get("result") == "Success":
                logger.info("Bot-password login succeeded for %s", username)
                return True, "Signed in (bot password)"
            reason = result.get("reason") or result.get("result") or "unknown"
            logger.warning("Bot-password login failed: %s", reason)
            return False, f"Sign-in failed: {reason}"

        data = {
            "action": "clientlogin",
            "username": username,
            "password": password,
            "loginreturnurl": URL,
            "logintoken": login_token,
            "format": "json",
        }
        response = http_session.post(URL, data=data, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        result = response.json().get("clientlogin", {})
        status = result.get("status")
        if status == "PASS":
            logger.info("Login succeeded for %s", username)
            return True, "Signed in"
        message = result.get("message") or result.get("messagecode") or status
        logger.warning("Login failed with status %s", status)
        if status == "UI":
            message = (
                "Two-factor authentication detected: use a bot password "
                "(Special:BotPasswords) as User@BotName"
            )
        return False, f"Sign-in failed: {message}"
    except (requests.RequestException, ValueError):
        logger.exception("Login request failed")
        return False, "Network error during sign-in"


def fetch_csrf_token(http_session: requests.Session):
    """Return a CSRF token for the logged-in user, or None on failure."""
    try:
        return _fetch_token(http_session, "csrf")
    except (requests.RequestException, KeyError, ValueError):
        logger.exception("Could not fetch CSRF token")
        return None
