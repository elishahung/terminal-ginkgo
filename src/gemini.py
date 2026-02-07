import requests


def generate_content(
    api_key: str,
    prompt: str,
    system_instruction: str,
    model: str = "gemini-2.5-flash-lite",
) -> str | None:
    """
    Generate content using Gemini REST API.

    Args:
        api_key: Google Gemini API key
        prompt: User's input prompt
        system_instruction: System instruction for the model
        model: Model name to use (default: gemini-2.5-flash-lite)

    Returns:
        Generated text response, or None if generation failed
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        params={"key": api_key},
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    # Parse response and extract text from candidates
    candidates = data.get("candidates", [])
    if candidates:
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if parts:
            return parts[0].get("text")

    return None
