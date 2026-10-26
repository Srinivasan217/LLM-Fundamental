"""A toy multi-head attention example built from the local attention function."""

from self_attention import self_attention


def multi_head_attention(tokens: list[list[float]], head_count: int = 2) -> list[list[float]]:
    """Split token dimensions across heads, attend, then concatenate outputs."""
    if head_count < 1:
        raise ValueError("head_count must be positive")
    width = len(tokens[0]) if tokens else 0
    if width == 0 or width % head_count:
        raise ValueError("embedding width must be positive and divisible by head_count")

    head_width = width // head_count
    head_outputs = []
    for head in range(head_count):
        start = head * head_width
        head_tokens = [token[start:start + head_width] for token in tokens]
        output, _ = self_attention(head_tokens)
        head_outputs.append(output)

    return [
        [head_outputs[head][position][column]
         for head in range(head_count)
         for column in range(head_width)]
        for position in range(len(tokens))
    ]


if __name__ == "__main__":
    vectors = [[1.0, 0.0, 0.5, 0.5], [0.0, 1.0, 0.5, 1.0]]
    for vector in multi_head_attention(vectors):
        print([round(value, 3) for value in vector])
