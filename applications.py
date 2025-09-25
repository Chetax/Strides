from google import genai 
from google.genai import types
from dotenv import load_dotenv
import os
import requests
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
    
# FUNCTION TO GET WATHER OF A CITY.

def get_weather_info(city: str):
    """
    Fetches weather data for a given city by first getting its coordinates.
    """
    try:
        api_key = os.getenv("openweathermapapi")
        if not api_key:
            return {"error": "OpenWeatherMap API key not set."}

        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()

        geo_data = geo_response.json()
        if not geo_data:
            return {"error": f"Could not find location for city: {city}"}
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()

        return weather_response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error: {http_err}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"A network error occurred: {e}"}
    except (IndexError, KeyError):
        return {"error": "Failed to parse location data. The city may be invalid."}
   


# write the function for gemini to getInfo for the same weather 


def get_weather_report_using_gemini(city:str):
     system_instructions="""
    You are given weather data in JSON format from the OpenWeather API.
    Your job is to convert it into a clear, human-friendly weather update.
    Guidelines:
    1. Always mention the city and country.
    2. Convert temperature from Kelvin to Celsius (°C), rounded to 1 decimal.
    3. Include: current temperature, feels-like temperature, main weather description, humidity, wind speed, and sunrise/sunset times (converted from UNIX timestamp).
    4. Use natural, conversational language.
    5. Based on the current conditions, suggest what the person should carry or wear.
    - If rain/clouds: suggest umbrella/raincoat.
    - If very hot (>30°C): suggest light cotton clothes, sunglasses, stay hydrated.
    - If cold (<15°C): suggest warm clothes, jacket.
    - If windy: suggest windbreaker, secure loose items.
    - If humid: suggest breathable clothes, water bottle.
    6. If any field is missing, gracefully ignore

    """
   
     response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Generate a clear lfriendly weather report with temperatures in °C, humidity, wind, sunrise/sunset for the {city} and practical suggestions on what to wear or carry.",
        config=types.GenerateContentConfig(system_instruction=system_instructions,tools=[get_weather_info])
     )
     return response.text


print(get_weather_report_using_gemini("nagpur"))