import os
from dotenv import load_dotenv
from google import genai    

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GENINI_API_kEY is missing from .env")
client = genai.Client(api_key=api_key)  

tests =[
    {
        "name": "Arithmetic",
        "prompt": (
            "A shop sells 3 notebooks for 40 rupees each and 2 pens"
            "for 15 rupees each. What is the total cost?"
            "Show the calculation."
        ),
        "expected": "150 rupees"
    },
    {
        "name": "Logic puzzle",
        "prompt": (
            "All roses are flowers. Some flowers fade quickly."
            "can we conclude that some roses fade quickly?"
            "Explain why or why not."
        ),
        "expected": "NO; the premises do not establish that any roses fade quickly."   },
]

for test in tests:
    print(f"\n---{test['name']}---")
    print("Expected reasoning check:", test["expected"])

    response = client.interactions.create(
        model="gemini-3.8-flash",   
        input=test["prompt"]
    )

    print("Model answer:", response.output_text) 

    