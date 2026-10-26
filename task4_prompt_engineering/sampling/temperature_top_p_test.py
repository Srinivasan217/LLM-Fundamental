
"""Demonstrate temperature and top-p using a toy token distribution.

Offline simulation only; no LLM text is generated.
"""

import csv
import math
import random
from pathlib import Path

LOGITS = {"the": 2.4, "a": 1.7, "our": 0.9, "their": 0.4}
OUTPUT = Path(__file__).resolve().parents[1] / "results" / "sampling_results.csv"


def distribution(temperature, top_p):
    if temperature == 0:
        return {"the": 1.0}

    scaled = {token: score / temperature for token, score in LOGITS.items()}
    peak = max(scaled.values())
    weights = {token: math.exp(score - peak) for token, score in scaled.items()}
    total = sum(weights.values())
    probabilities = {
        token: weight / total for token, weight in weights.items()
    }

    ordered = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
    kept = {}
    cumulative = 0.0

    for token, probability in ordered:
        kept[token] = probability
        cumulative += probability
        if cumulative >= top_p:
            break

    total_kept = sum(kept.values())
    return {token: probability / total_kept for token, probability in kept.items()}


def choose_token(probabilities):
    tokens = list(probabilities.keys())
    weights = list(probabilities.values())
    return random.choices(tokens, weights=weights, k=1)[0]


def main():
    random.seed(42)
    rows = []

    # Five simulated generations at each temperature.
    for temperature in (0, 0.7, 1.2):
        probabilities = distribution(temperature, 0.95)

        for generation in range(1, 6):
            token = choose_token(probabilities)
            rows.append({
                "experiment": "temperature",
                "temperature": temperature,
                "top_p": 0.95,
                "generation": generation,
                "token": token,
                "probability": round(probabilities[token], 6),
            })

    # Compare two top-p settings at temperature 0.7.
    for top_p in (0.3, 0.95):
        probabilities = distribution(0.7, top_p)

        for generation in range(1, 6):
            token = choose_token(probabilities)
            rows.append({
                "experiment": "top_p",
                "temperature": 0.7,
                "top_p": top_p,
                "generation": generation,
                "token": token,
                "probability": round(probabilities[token], 6),
            })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Temperature generations: 15")
    print("Top-p comparison generations: 10")
    print(f"Total generations: {len(rows)}")
    print(f"Results saved to: {OUTPUT}")
    print("Note: These are sampled tokens from a toy distribution, not LLM generations.")


if __name__ == "__main__":
    main()
