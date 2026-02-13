import os

from duplocloud.client import DuploClient
from duplocloud.errors import DuploError

_client: DuploClient | None = None


def get_client() -> DuploClient:
    """Return a singleton DuploClient, lazily initialized from environment variables."""
    global _client
    if _client is not None:
        return _client

    host = os.environ.get("DUPLO_HOST", "").strip()
    token = os.environ.get("DUPLO_TOKEN", "").strip()
    tenant = os.environ.get("DUPLO_TENANT", "").strip() or None

    if not host:
        raise DuploError("DUPLO_HOST environment variable is required", 500)
    if not token:
        raise DuploError("DUPLO_TOKEN environment variable is required", 500)

    _client = DuploClient.from_creds(host=host, token=token, tenant=tenant)
    return _client


def reset_client() -> None:
    """Reset the singleton client. Used in testing."""
    global _client
    _client = None
