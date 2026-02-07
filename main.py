import sys
from google import genai
from spinner import Spinner
from settings import Settings
from instruction import SYSTEM_PROMPT
from clipboard import copy_to_input


def main():
    if len(sys.argv) < 2:
        print("Usage: ai <your request>")
        sys.exit(1)

    user_message = " ".join(sys.argv[1:])

    settings = Settings()
    client = genai.Client(api_key=settings.GOOGLE_GEMINI_API_KEY)

    with Spinner(""):
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=user_message,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )
    
    if response.text:
        copy_to_input(response.text.strip())


if __name__ == "__main__":
    main()
