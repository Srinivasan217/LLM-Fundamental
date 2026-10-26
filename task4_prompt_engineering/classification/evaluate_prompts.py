
"""Compare three prompt versions using an offline keyword baseline.

Note: This does not call an LLM. All prompt versions use the same
classifier, so their scores are baseline results, not prompt effects.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KEYWORDS = {
    "billing": {"charged", "charge", "payment", "refund", "invoice", "billed"},
    "technical": {"crash", "crashes", "error", "bug", "upload", "app"},
    "account": {"account", "email", "cancel", "plan", "login", "profile"},
    "shipping": {"package", "arrived", "tracking", "delivery", "ship"},
}


def classify(text: str) -> str:
    words = set(text.lower().replace(".", " ").replace(",", " ").split())
    scores = {
        label: len(words & keywords)
        for label, keywords in KEYWORDS.items()
    }
    return max(KEYWORDS, key=lambda label: scores[label])


def main() -> None:
    data_file = ROOT / "datasets" / "support_tickets.json"
    output_file = ROOT / "results" / "classification_results.csv"

    with data_file.open(encoding="utf-8") as file:
        tickets = json.load(file)

    rows = []

    for version in ("v1", "v2", "v3"):
        prompt_file = ROOT / "prompts" / f"classification_{version}.txt"

        if not prompt_file.exists():
            raise FileNotFoundError(f"Missing prompt file: {prompt_file}")

        prompt = prompt_file.read_text(encoding="utf-8")

        for ticket in tickets:
            prediction = classify(ticket["text"])

            rows.append({
                "prompt_version": version,
                "ticket_id": ticket["id"],
                "expected": ticket["label"],
                "predicted": prediction,
                "correct": prediction == ticket["label"],
                "uses_few_shot_examples": (
                    "Examples:" in prompt if version == "v3" else False
                ),
            })

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Tickets evaluated per version: {len(tickets)}")
    print(f"Total evaluation rows: {len(rows)}")
    print("Important: these are offline keyword-baseline results,")
    print("not measurements of actual LLM prompt performance.")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()
