from jev_demo.present import pause, timed


def test_timed_returns_result_and_seconds():
    result, seconds = timed(lambda x: x + 1, 1)
    assert result == 2
    assert seconds >= 0


def test_pause_skips_when_disabled(monkeypatch):
    monkeypatch.setenv("DEMO_NOPAUSE", "1")
    monkeypatch.setattr("builtins.input", lambda *_: (_ for _ in ()).throw(AssertionError("blocked")))
    pause()
