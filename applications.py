from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

# This is the new, correct way
client = genai.Client(api_key=gemini_api_key)


def prompt_for_quote():
    base_prompt = """
    **Goal:** Generate an original "Quote for the Day".

    **Instructions:**
    -   **Length:** The quote must be concise, ideally between 10 and 20 words.
    -   **Theme:** Focus on topics like inspiration, motivation, perseverance, or personal growth.
    -   **Tone:** The quote should have a positive, uplifting, and insightful tone.
    -   **Style:** It must be an original, impactful, and easy-to-understand statement. Do not use famous or existing quotes.
    """

    return base_prompt


def get_random_quotes():
    response=client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[prompt_for_quote()],
    )
    return response.text
    