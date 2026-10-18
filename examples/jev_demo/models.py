"""Model IDs in one place. Retirements (Vertex): 2.5 on 2026-10-20, 3.6 Flash on 2026-11-19,
3.7 Flash on 2027-01-28. See research/google-a-gemini-vertex.md; re-check before running."""

ARGON_ID = "gemini-4-argon"  # stable flagship (released 2026-10-13)
FLASH_ID = "gemini-3.8-flash"  # cheap tier, used where a router needs something to downshift to

DEFAULT = f"google_genai:{ARGON_ID}"
FAST = f"google_genai:{FLASH_ID}"
POWERFUL = DEFAULT
CHEAP_FALLBACK = "google_genai:gemini-3.5-flash-lite"
