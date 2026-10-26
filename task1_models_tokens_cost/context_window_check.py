
# Check whether texts fit within context windows

import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

sample_texts = {
    "Sentence": "AI can help people solve problems.",
    "Paragraph": (
        "Large language models process text as tokens. "
        "They can summarize documents, answer questions, "
        "and generate text."
    ),
    "JSON": '{"name": "Arun", "skills": ["Python", "AI"]}',
}

context_windows = [8000, 128000]

for name, text in sample_texts.items():
    token_count = len(encoding.encode(text))

    print(f"\n{name}")
    print(f"Token count: {token_count}")

    for limit in context_windows:
        fits = token_count <= limit
        print(f"Fits within {limit:,} tokens: {fits}")
