
"""Hugging Face examples: sentiment, BERT fill-mask, and GPT-2."""

def main():
    try:
        from transformers import pipeline
    except ImportError as error:
        raise SystemExit(
            "Install the packages with: "
            "python -m pip install transformers torch"
        ) from error

    # 1. Sentiment analysis
    print("\n=== Sentiment Analysis ===")
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    )

    results = classifier([
        "The explanation was clear.",
        "The service was frustrating."
    ])

    for result in results:
        print(result)

    # 2. BERT fill-mask
    print("\n=== BERT Fill-Mask ===")
    fill_mask = pipeline(
        "fill-mask",
        model="google-bert/bert-base-uncased"
    )

    results = fill_mask("The capital of France is [MASK].")

    for result in results[:3]:
        print(result["token_str"], round(result["score"], 4))

    # 3. GPT-2 text generation
    print("\n=== GPT-2 Text Generation ===")
    generator = pipeline(
        "text-generation",
        model="openai-community/gpt2"
    )

    results = generator(
        "Artificial intelligence can help people",
        max_new_tokens=30,
        do_sample=False,
        pad_token_id=50256
    )

    print(results[0]["generated_text"])


if __name__ == "__main__":
    main()
