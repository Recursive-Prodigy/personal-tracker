import os
from dotenv import load_dotenv
from openai_compatible_parser import parse_entry as base_parse_entry

load_dotenv(override=True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def parse_entry(text):
    return base_parse_entry(
        text,
        base_url="https://openrouter.ai/api/v1/chat/completions",
        api_key=OPENROUTER_API_KEY,
        model="openrouter/free"
    )