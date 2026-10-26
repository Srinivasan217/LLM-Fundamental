import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")
client = genai.Client(api_key=api_key)

prompts =[
    (
        "Recent event without warning",
        "who won the most recent major international sporting event?"
        "Give the event data and winner"
    ),
     (
        "Recent event with uncertainty instruction",
        "Tell me who won a major international sporting event "
        "after your reliable knowledge may end. If you cannot verify "
        "the answer, say you don't know. Do not guess."
    ),
 ]   

for title,prompt in prompts:
    print(f"\n--- {title} ---")
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )
    print(response.output_text)