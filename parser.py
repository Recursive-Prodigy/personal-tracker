from claude_parser import parse_entry as claude_parse_entry
from openai_parser import parse_entry as openai_parse_entry

PROVIDER = "claude"  # change to "openai" to switch providers


def parse_entry(text):
    print(f"[API selected: {PROVIDER}]")

    if PROVIDER == "claude":
        return claude_parse_entry(text)
    elif PROVIDER == "openai":
        return openai_parse_entry(text)
    else:
        raise ValueError(f"Unknown provider: {PROVIDER}")