# Task 3: Transformer Concepts

Small, dependency-free demonstrations of self-attention, multi-head attention, and sinusoidal positional encodings.

## Run

```powershell
python self_attention.py
python multi_head_attention.py
python positional_encoding.py
```

`positional_encoding.py` writes `outputs/positional_encoding.png`. `huggingface_examples.py` shows optional Hugging Face usage and imports its dependencies only when run.

## Hugging Face Examples

The `huggingface_examples.py` script demonstrates three pretrained language-model tasks:

1. **Sentiment Analysis:** Uses DistilBERT to classify sentences as positive or negative.
2. **BERT Fill-Mask:** Uses BERT to predict missing words. For the sentence "The capital of France is [MASK].", the top prediction was `paris` with a score of 0.4168.
3. **GPT-2 Text Generation:** Generates additional text from a starting sentence using a pretrained GPT-2 model.

### Execution

Run from the project root:

```powershell
python .\task3_transformer_concepts\huggingface_examples.py
```

### Results

All three examples executed successfully. The models were loaded from Hugging Face and produced outputs. Results are illustrative and do not represent a complete evaluation of model accuracy.
