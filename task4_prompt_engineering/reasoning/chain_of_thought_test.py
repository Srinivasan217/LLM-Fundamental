
"""Compare direct answers and auditable reasoning summaries.

Offline demonstration only; this script does not call an LLM.
"""

import csv
from pathlib import Path

QUESTIONS = [
    {
        "question": "A team has 18 tickets. It resolves 7 in the morning and 5 in the afternoon. How many remain?",
        "numbers": (18, 7, 5),
        "operation": "subtract",
        "answer": 6,
    },
    {
        "question": "A shop has 24 notebooks and buys 13 more. How many notebooks are there?",
        "numbers": (24, 13),
        "operation": "add",
        "answer": 37,
    },
    {
        "question": "Five boxes contain 6 items each. How many items are there?",
        "numbers": (5, 6),
        "operation": "multiply",
        "answer": 30,
    },
    {
        "question": "A bill of 56 dollars is shared equally among 8 people. How much does each pay?",
        "numbers": (56, 8),
        "operation": "divide",
        "answer": 7,
    },
    {
        "question": "Maya has 40 points, earns 15 more, then spends 12. How many points remain?",
        "numbers": (40, 15, 12),
        "operation": "add_subtract",
        "answer": 43,
    },
]


def calculate(problem):
    numbers = problem["numbers"]
    operation = problem["operation"]

    if operation == "subtract":
        return numbers[0] - numbers[1] - numbers[2]
    if operation == "add":
        return numbers[0] + numbers[1]
    if operation == "multiply":
        return numbers[0] * numbers[1]
    if operation == "divide":
        return numbers[0] // numbers[1]
    if operation == "add_subtract":
        return numbers[0] + numbers[1] - numbers[2]


def main():
    output = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "reasoning_results.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="", encoding="utf-8") as file:
        fields = [
            "question",
            "prompt_condition",
            "answer",
            "expected_answer",
            "correct",
            "reasoning_summary",
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for problem in QUESTIONS:
            answer = calculate(problem)
            expected = problem["answer"]

            writer.writerow({
                "question": problem["question"],
                "prompt_condition": "Without step-by-step instruction",
                "answer": answer,
                "expected_answer": expected,
                "correct": answer == expected,
                "reasoning_summary": "Direct answer only.",
            })

            writer.writerow({
                "question": problem["question"],
                "prompt_condition": "With step-by-step instruction",
                "answer": answer,
                "expected_answer": expected,
                "correct": answer == expected,
                "reasoning_summary": (
                    f"Calculate using {problem['operation']}; "
                    f"the result is {answer}."
                ),
            })

    print(f"Problems tested: {len(QUESTIONS)}")
    print(f"Total result rows: {len(QUESTIONS) * 2}")
    print(f"Results saved to: {output}")
    print("Note: This is a deterministic offline simulation, not an LLM test.")


if __name__ == "__main__":
    main()
