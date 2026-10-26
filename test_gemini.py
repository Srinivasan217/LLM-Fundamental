
import os
from dotenv import load_dotenv
from google import genai

# Load the API key from the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Send a test prompt using the current recommended API
response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Write a short poem about the beauty of nature."
)

# Display the model's answer
print("Gemini connection successful!")
print(response.output_text)
