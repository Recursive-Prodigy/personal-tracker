import os
import requests
import json
from dotenv import load_dotenv
from prompts import build_extraction_prompt

load_dotenv(override=True)
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")


def parse_entry(text):
    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": build_extraction_prompt(text)}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    reply_text = data["content"][0]["text"]
    reply_text = reply_text.replace("```json", "").replace("```", "").strip()

    return json.loads(reply_text)