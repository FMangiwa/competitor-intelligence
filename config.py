import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# API Keys & Endpoints
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Model Names
DEFAULT_OPENAI_MODEL = "gpt-5-mini"
DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-lite"

# Max characters limit for text truncation to manage token limits
MAX_CONTENT_CHARS = 5_000

# Prompts
LINK_SELECTION_SYSTEM_PROMPT = """
You are provided with a list of links found on a webpage.
Decide which links are most relevant for building an executive company profile (e.g., About, Products, Careers, Pricing).

IMPORTANT: Only select valid HTTP or HTTPS web URLs. Ignore email links (mailto:), phone numbers (tel:), social share links, and anchor tags (#).

Respond strictly in JSON format as follows:
{
    "links": [
        {"type": "about page", "url": "https://full.url/about"},
        {"type": "careers page", "url": "https://full.url/careers"}
    ]
}
"""

BROCHURE_SYSTEM_PROMPTS = {
    "Professional": """You are an executive business analyst. Analyze company pages and produce a concise, structured business overview markdown report focusing on mission, products, market position, and culture.

IMPORTANT RULE: Do NOT include offers for follow-up actions (e.g., "If you want, I can...", "Let me know if you need..."). Stop generating immediately after the report ends.""",

    "Snarky/Humorous": """You are a sarcastic tech critic. Analyze company pages and produce a witty, satirical markdown summary of the company for prospective investors and recruits.

IMPORTANT RULE: Do NOT include offers for follow-up actions (e.g., "If you want, I can...", "Let me know if you need..."). Stop generating immediately after the report ends."""
}