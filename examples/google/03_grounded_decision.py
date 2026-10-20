"""Gemini with Google Search grounding: for decisions that depend on fresh public facts."""

from dotenv import load_dotenv
from google import genai
from google.genai import types

from jev_demo.models import ARGON_ID

load_dotenv()

client = genai.Client(vertexai=True)  # ADC; project/location from GOOGLE_CLOUD_PROJECT/LOCATION
response = client.models.generate_content(
    model=ARGON_ID,
    contents="Is Gemini 2.5 Flash still available on Vertex AI? Answer yes or no, then cite.",
    config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]),
)
print(response.text)

metadata = response.candidates[0].grounding_metadata
if metadata and metadata.grounding_chunks:
    for chunk in metadata.grounding_chunks:
        print("-", chunk.web.title, chunk.web.uri[:70] + '...')
# Billed per executed search query (free tier, then per 1,000): see research/google-a-gemini-vertex.md.
