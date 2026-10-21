import os

from langchain_google_genai import ChatGoogleGenerativeAI

# Every Gemini client (LangChain, google-genai, ADK) goes through Vertex AI with Application Default
# Credentials. Set GOOGLE_CLOUD_PROJECT yourself.
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")  # gemini-4-argon is not served regionally

# Several Gemini models retire soon (dates in research/google-a-gemini-vertex.md). Re-check before running.
ARGON_ID = "gemini-4-argon"
FLASH_ID = "gemini-3.8-flash"

DEFAULT = f"google_genai:{ARGON_ID}"
FAST = f"google_genai:{FLASH_ID}"
POWERFUL = DEFAULT
CHEAP_FALLBACK = "google_genai:gemini-3.5-flash-lite"


def gemini(schema, temperature=0):
    """Gemini on Vertex that answers in the shape of `schema`."""
    model = ChatGoogleGenerativeAI(model=ARGON_ID, vertexai=True, temperature=temperature)
    return model.with_structured_output(schema)
