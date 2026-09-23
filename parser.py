from claude_parser import parse_entry as claude_parse_entry
from openai_parser import parse_entry as openai_parse_entry
from groq_parser import parse_entry as groq_parse_entry
from gemini_parser import parse_entry as gemini_parse_entry
from openrouter_parser import parse_entry as openrouter_parse_entry

PROVIDER = "auto"  # claude / openai / groq / gemini / openrouter / auto

PROVIDERS = {
    "claude": claude_parse_entry,
    "openai": openai_parse_entry,
    "groq": groq_parse_entry,
    "gemini": gemini_parse_entry,
    "openrouter": openrouter_parse_entry,
}

# Priority order used only when PROVIDER = "auto"
AUTO_ORDER = ["claude", "groq", "openrouter", "gemini", "openai"]


def validate_entry(entry):
    if "type" not in entry:
        raise ValueError("Missing 'type' field in parsed entry")

    required_fields = {
        "book_purchase": {"title", "author", "price", "date_purchased", "category", "format"},
        "buy_list": {"item", "category", "est_price", "priority", "status", "date_added"},
        "build_list": {"name", "description", "status", "date_added", "date_updated"},
    }

    entry_type = entry["type"]
    if entry_type not in required_fields:
        raise ValueError(f"Unknown entry type: {entry_type}")

    missing = required_fields[entry_type] - entry.keys()
    if missing:
        raise ValueError(f"Entry missing fields: {missing}")

    return entry


def parse_entry(text):
    if PROVIDER == "auto":
        last_error = None
        for name in AUTO_ORDER:
            try:
                print(f"[Auto mode] Trying: {name}")
                raw_entry = PROVIDERS[name](text)
                return validate_entry(raw_entry)
            except Exception as e:
                print(f"[Auto mode] {name} failed: {e}")
                last_error = e
        raise RuntimeError(f"All providers failed. Last error: {last_error}")

    print(f"[API selected: {PROVIDER}]")
    if PROVIDER not in PROVIDERS:
        raise ValueError(f"Unknown provider: {PROVIDER}")

    raw_entry = PROVIDERS[PROVIDER](text)
    return validate_entry(raw_entry)