
import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load the API key
load_dotenv()
print("Starting capabilities lab...")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found in .env")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)
print("Gemini client initialized.")

# Five capability tests
tests = [
    {
        "name": "Summarization",
        "prompt": (
            "Summarize in one sentence: Machine learning allows "
            "computers to learn patterns from data. It is used in "
            "healthcare, finance, transport, and customer service."
        )
    },
    {
        "name": "Classification",
        "prompt": (
            "Classify this ticket as Billing, Technical, or Account. "
            "Return only the category. "
            "Ticket: I was charged twice for my subscription."
        )
    },
    {
        "name": "Information Extraction",
        "prompt": (
            'Extract the name and skills as JSON: '
            '"Maya knows Python and SQL." '
            'Return {"name": "...", "skills": []}.'
        )
    },
    {
        "name": "Translation",
        "prompt": (
            "Translate into Tamil: "
            "Thank you for contacting customer support."
        )
    },
    {
        "name": "Code Generation",
        "prompt": (
            "Write a short Python function that returns "
            "the square of a number."
        )
    }
]

output_file = (
    Path("task2_capabilities_limitations")
    / "capability_results.csv"
)
output_file.parent.mkdir(parents=True, exist_ok=True)

fieldnames = ["Test", "Prompt", "Result", "Rating"]
results = []

# Save the CSV after every test so completed results are preserved.
def save_results():
    with output_file.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


print("Number of tests:", len(tests))

for test in tests:
    print(f"\nSending request for: {test['name']}", flush=True)

    try:
        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=test["prompt"]
        )

        answer = response.output_text or ""
        print("Result:", answer)

        rating = input(
            "Rate the result from 1 to 5: "
        ).strip()

    except Exception as error:
        print("Request failed for:", test["name"])
        print("Error type:", type(error).__name__)
        print("Error details:", error)

        answer = "Request failed: " + str(error)
        rating = "0"

    results.append({
        "Test": test["name"],
        "Prompt": test["prompt"],
        "Result": answer,
        "Rating": rating
    })

    save_results()
    print("Results saved to:", output_file, flush=True)

print("\nAll five capability tests have been processed.")
print("Final results file:", output_file)
