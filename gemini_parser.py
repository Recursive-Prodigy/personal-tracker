import os
from dotenv import load_dotenv
from openai_compatible_parser import parse_entry as base_parse_entry

load_dotenv(override=True)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def parse_entry(text):
    return base_parse_entry(
        text,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        api_key=GEMINI_API_KEY,
        model="gemini-3.5-flash-lite"
    )