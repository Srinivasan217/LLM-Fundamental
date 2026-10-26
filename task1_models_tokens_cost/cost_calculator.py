"""Estimate an API call cost from token counts and per-million-token rates."""


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_million: float,
    output_price_per_million: float,
) -> float:
    """Return estimated cost in the same currency as the supplied rates."""
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("token counts cannot be negative")
    if input_price_per_million < 0 or output_price_per_million < 0:
        raise ValueError("token prices cannot be negative")
    return (
        input_tokens * input_price_per_million
        + output_tokens * output_price_per_million
    ) / 1_000_000


if __name__ == "__main__":
     # Assignment requirements
    chats_per_day = 1000
    days_per_month = 30

    input_tokens_per_chat = 1500
    output_tokens_per_chat = 400

    # Example prices per 1 million tokens (USD)
    input_price = 0.50
    output_price = 1.50

    # Calculate monthly token usage
    monthly_input = chats_per_day * days_per_month * input_tokens_per_chat
    monthly_output = chats_per_day * days_per_month * output_tokens_per_chat

    # Calculate monthly cost
    monthly_cost = calculate_cost(
        monthly_input,
        monthly_output,
        input_price,
        output_price,
    )

    print("MONTHLY API COST ESTIMATE")
    print(f"Chats per month: {chats_per_day * days_per_month:,}")
    print(f"Monthly input tokens: {monthly_input:,}")
    print(f"Monthly output tokens: {monthly_output:,}")
    print(f"Estimated monthly cost: ${monthly_cost:.2f}")
