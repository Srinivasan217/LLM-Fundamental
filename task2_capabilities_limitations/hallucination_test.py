import os
from dotenv import load_dotenv
from google import genai    

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GENINI_API_kEY is missing from .env")

client = genai.client(api_key=api_key)

question = (
    "summarize the finding of the 2024 research paper"
    "'Quatum penguins and Their Effect on Lunar Agriculture'"
    "by Dr.Alex Example. Include its main consclusion."
)


prompts = [
    ("without uncertainty instruction", question),
    (
        "with uncertainty instruction",
        question
        + "\nOnly give factual information.If you cannot verify"
        "that this paper exists, say you don't know. DO not invent details."
    ),
]

for label , prompt in prompts:
    print(f"\n --- {label} ---")

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    print(response.output_text)

    