import os
from dotenv import load_dotenv
from openai_compatible_parser import parse_entry as base_parse_entry

load_dotenv(override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def parse_entry(text):
    return base_parse_entry(
        text,
        base_url="https://api.groq.com/openai/v1/chat/completions",
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-20b"
    )