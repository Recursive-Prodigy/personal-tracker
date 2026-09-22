import os
import requests
import json
from dotenv import load_dotenv
from prompts import build_extraction_prompt

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def parse_entry(text):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": build_extraction_prompt(text)}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

# Temporary line for status check
    print("OpenAI response body:", response.text)
    response.raise_for_status()

    data = response.json()
    reply_text = data["choices"][0]["message"]["content"]
    reply_text = reply_text.replace("```json", "").replace("```", "").strip()

    return json.loads(reply_text)