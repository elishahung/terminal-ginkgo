import os


def get_api_key() -> str:
    """
    Retrieve the Gemini API key from environment variables.

    Checks AI_TERMINAL_API_KEY first, then falls back to GEMINI_API_KEY.

    Returns:
        str: The API key

    Raises:
        ValueError: If no API key is found in environment variables
    """
    key = os.getenv("AI_TERMINAL_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError(
            "API key not found. Set AI_TERMINAL_API_KEY or GEMINI_API_KEY environment variable."
        )
    return key
