from conftest import choice, make_classifier, noul, score
from jev_demo.gating import QUESTIONS, decide


def run(answers):
    return decide(make_classifier(answers).invoke({"state": "x", "questions": QUESTIONS}))


def test_low_confidence_goes_to_human():
    d = run({"urgent": noul(0.99), "team": choice("infra", 0.4), "severity": score(2.0)})
    assert d.action == "human_triage"


def test_other_team_goes_to_human():
    d = run({"urgent": noul(0.1), "team": choice("other", 0.95), "severity": score(0.2)})
    assert d.action == "human_triage"


def test_urgent_outage_pages_oncall():
    d = run({"urgent": noul(0.95), "team": choice("infra", 0.9), "severity": score(1.9)})
    assert (d.action, d.team) == ("page_oncall", "infra")


def test_confident_routine_ticket_auto_routes():
    d = run({"urgent": noul(0.2), "team": choice("billing", 0.9), "severity": score(0.5)})
    assert (d.action, d.team) == ("auto_route", "billing")


def test_evaluate_reports_accuracy_and_misses():
    from jev_demo.evaluation import evaluate

    data = [("a", "x"), ("b", "y"), ("c", "x")]
    result = evaluate(lambda t: "x", data)
    assert result["accuracy"] == 2 / 3
    assert result["misses"] == {("y", "x"): 1}
