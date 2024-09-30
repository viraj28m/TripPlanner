import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

def city_chatgpt_request(city, num_days, location_prefs):
    location_prefs_prompt = ""
    if location_prefs != '[]':
        location_prefs_prompt = f"Please do NOT include the following activities in the list: {location_prefs}"

    activities_per_day = 3

    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(os.path.join(BASE_DIR.parent.absolute(), '.env'))

    api_key = os.environ.get('OPENAI_API_KEY')

    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key
    )

    prompt_text = f"""
imagine you are a tourist, can you give me the top {activities_per_day * num_days + 5} attractions to visit in {city} in a list without any extra text or descriptions. 
{location_prefs_prompt}
Please include only the list with no numbers in your response and please give the official names of the attractions. 
Make sure to include at least {activities_per_day * num_days + 5} attractions. Please do not include any repeated locations. 

Use this as an example:
Attraction 1
Attraction 2
Attraction 3
Attraction 4
Attraction 5
Attraction 6
Attraction 7
Attraction 8
Attraction 9
Attraction 10
"""

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt_text,
        }
    ],
    model="gpt-3.5-turbo",
    )

    generated_text = chat_completion.choices[0].message.content
    return generated_text

def attraction_desc(attraction):
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(os.path.join(BASE_DIR.parent.absolute(), '.env'))

    api_key = os.environ.get('OPENAI_API_KEY')

    client = OpenAI(
        api_key=api_key
    )

    prompt_text = f"""
    Please do not include the attraction name in the description. 
    Please capitalize the first word of the description.
    Please give me a short one-sentence description of the following attraction: {attraction}
    """

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt_text,
        }
    ],
    model="gpt-3.5-turbo",
    )

    generated_text = chat_completion.choices[0].message.content
    return generated_text

