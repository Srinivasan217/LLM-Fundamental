
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

problems = [
    "A shirt costs 500 rupees after a 20% discount. What was its original price?",
    "A train travels 180 km in 3 hours. What is its average speed?",
    "Ravi has 24 chocolates and gives one-third to his friend. How many remain?",
    "A shop sells 4 books for 120 rupees each. What is the total cost?",
    "A tank holds 100 litres and is 35% full. How many litres are inside?"
]

for i, problem in enumerate(problems, start=1):
    print(f"\n{'=' * 45}")
    print(f"Problem {i}: {problem}")

    for label, instruction in [
        ("Direct prompt", "Give only the final answer."),
        (
            "Step-by-step prompt",
            "Solve carefully. Show the calculation briefly, then give the final answer."
        ),
    ]:
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=f"{problem}\n{instruction}"
        )

        print(f"\n{label}:")
        print(response.output_text)
