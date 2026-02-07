"""
AI Terminal - A fast command-line AI assistant.

Translates natural language queries into shell commands using LLM.
"""

import sys

from instruction import SYSTEM_PROMPT
from settings import get_api_key
from spinner import Spinner


def main():
    """Main entry point for the AI Terminal."""
    if len(sys.argv) < 2:
        print("Usage: ai <your request>")
        sys.exit(1)

    user_message = " ".join(sys.argv[1:])

    # Import here to defer loading until needed
    from gemini import generate_content

    with Spinner(""):
        response_text = generate_content(
            api_key=get_api_key(),
            prompt=user_message,
            system_instruction=SYSTEM_PROMPT,
        )

    if response_text:
        from clipboard import copy_to_input
        copy_to_input(response_text.strip())


if __name__ == "__main__":
    main()
