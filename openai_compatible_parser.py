import requests
import json
from prompts import build_extraction_prompt


def parse_entry(text, base_url, api_key, model):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": build_extraction_prompt(text)}
        ]
    }

    response = requests.post(base_url, headers=headers, json=payload)

    response.raise_for_status()

    data = response.json()
    reply_text = data["choices"][0]["message"]["content"]
    reply_text = reply_text.replace("```json", "").replace("```", "").strip()

    return json.loads(reply_text)

# This means other four new apis im about to add share same structure as open ai style of layout so we set this as a common spawn point