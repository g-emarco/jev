"""Score a decision function against labeled examples, with a per-label breakdown."""

from collections import Counter
from collections.abc import Callable, Sequence


def evaluate(
    decide: Callable[[str], str], dataset: Sequence[tuple[str, str]]
) -> dict[str, object]:
    """Return accuracy and the (expected -> got) misses for (text, expected_label) pairs."""
    misses: Counter[tuple[str, str]] = Counter()
    correct = 0
    for text, expected in dataset:
        got = decide(text)
        if got == expected:
            correct += 1
        else:
            misses[(expected, got)] += 1
    return {"accuracy": correct / len(dataset), "n": len(dataset), "misses": dict(misses)}
