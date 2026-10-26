"""A small, standard-library self-attention demonstration."""

import math


def softmax(scores: list[float]) -> list[float]:
    peak = max(scores)
    exponentials = [math.exp(score - peak) for score in scores]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def self_attention(tokens: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
    """Use each token as its own query, key, and value for a toy example."""
    if not tokens or not tokens[0]:
        raise ValueError("tokens must contain non-empty vectors")
    width = len(tokens[0])
    if any(len(token) != width for token in tokens):
        raise ValueError("all token vectors must have the same width")

    outputs = []
    all_weights = []
    scale = math.sqrt(width)
    for query in tokens:
        weights = softmax([sum(a * b for a, b in zip(query, key)) / scale for key in tokens])
        outputs.append([
            sum(weight * token[column] for weight, token in zip(weights, tokens))
            for column in range(width)
        ])
        all_weights.append(weights)
    return outputs, all_weights


if __name__ == "__main__":
    vectors = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    output, attention = self_attention(vectors)
    print("Attention weights:")
    for row in attention:
        print([round(value, 3) for value in row])
    print("Context vectors:")
    for row in output:
        print([round(value, 3) for value in row])
