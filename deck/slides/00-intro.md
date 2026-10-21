# Jev
### Decisions you can gate on

TypeSafe's decision model, LangChain middleware, and where Google fits

Note: Press `s` for speaker notes. Serve with `python -m http.server` from `deck/`; markdown sections need http, not file://.

---

## The problem

An agent makes dozens of small decisions per task:

- Which team owns this?
- Is this tool call safe?
- Which model is worth paying for?

Asking a chat model and parsing its prose gives you **an answer, not a degree of belief**.

--

## What we want from a decision

| Need | Why |
|---|---|
| Typed output | Code branches on it |
| A probability | Set thresholds by cost of being wrong |
| Confidence | Know when to hand off to a human |
| Cheap + fast | Runs on every message and tool call |

--

## Agenda

1. **Jev**: Noul, Choice, Score
2. **Middleware**: where decisions belong in an agent
3. **Google**: decision-model offerings in production
4. **Choosing**: matrix and production checklist

Every code slide maps to a runnable file in `examples/`.
