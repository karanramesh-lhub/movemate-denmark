from langfuse import get_client

from movemate.config import settings


def get_langfuse_client():
    """Return the configured Langfuse client."""
    if not settings.langfuse_public_key or not settings.langfuse_secret_key:
        return None

    return get_client()