"""Small, testable helper for selecting credential sources."""

def resolve_api_key(environment_key=None, streamlit_key=None, manual_key=None):
    """Choose a configured key, otherwise a manually provided key.

    Returns (key, source). Credentials are never logged or persisted here.
    """
    for key, source in ((streamlit_key, "Streamlit secret"), (environment_key, "environment variable"), (manual_key, "manual input")):
        if isinstance(key, str) and key.strip():
            return key.strip(), source
    return None, None
