
import tiktoken
import csv
from pathlib import Path

# Use an OpenAI tokenizer encoding
encoding = tiktoken.get_encoding("cl100k_base")

# Five sample texts required by the assignment
texts = {
    "Sentence": "Large language models can answer questions.",
    "Paragraph": (
        "Large language models are trained on large amounts of text. "
        "They can summarize documents, classify messages, and generate answers."
    ),
    "Page": (
        "Artificial intelligence helps computers perform tasks that usually "
        "require human intelligence. Language models learn patterns from text "
        "and use those patterns to generate responses. They are useful for "
        "summarization, translation, classification, question answering, and "
        "information extraction. However, their answers can contain errors, "
        "so important information should be verified."
    ) * 8,
    "JSON": (
        '{"name":"Arun","skills":["Python","SQL","Machine Learning"],'
        '"years_experience":3}'
    ),
    "Tamil": "வணக்கம்! நான் செயற்கை நுண்ணறிவைக் கற்றுக்கொள்கிறேன்."
}

results = []

for text_type, text in texts.items():
    tokens = encoding.encode(text)
    words = text.split()

    token_count = len(tokens)
    word_count = len(words)
    words_per_token = word_count / token_count if token_count else 0

    results.append({
        "Text Type": text_type,
        "Words": word_count,
        "Tokens": token_count,
        "Words per Token": round(words_per_token, 3)
    })

print("\nTOKEN COUNT RESULTS")
print("-" * 65)

for result in results:
    print(
        f"{result['Text Type']:<12} "
        f"Words: {result['Words']:<5} "
        f"Tokens: {result['Tokens']:<5} "
        f"Words/Token: {result['Words per Token']}"
    )

# Save results to a CSV file
output_file = Path(__file__).with_name("token_results.csv")

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"\nResults saved to: {output_file}")
