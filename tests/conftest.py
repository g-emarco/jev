import httpx2
import pytest
from langchain_typesafe import TypeSafeClassifier


def make_classifier(answers: dict) -> TypeSafeClassifier:
    """A real TypeSafeClassifier whose HTTP layer returns canned answers."""

    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json={"model": "jev-latest", "answers": answers})

    return TypeSafeClassifier(
        api_key="test", client=httpx2.Client(transport=httpx2.MockTransport(handler))
    )


def noul(p: float) -> dict:
    return {"type": "noul", "noul": p}


def choice(label: str, confidence: float, labels=("infra", "billing", "other")) -> dict:
    probs = {name: (0.8 if name == label else 0.1) for name in labels}
    return {"type": "choice", "choice": label, "probabilities": probs, "confidence": confidence}


def score(level: float) -> dict:
    return {
        "type": "score",
        "score": level,
        "legend": {"0": "a", "1": "b", "2": "c"},
        "probabilities": {"0": 0.1, "1": 0.2, "2": 0.7},
        "confidence": 0.6,
    }


@pytest.fixture
def typesafe_env(monkeypatch):
    monkeypatch.setenv("TYPESAFE_API_KEY", "test")
