from datetime import date


def build_extraction_prompt(text):
    today = date.today()

    return f"""You are a data extraction system for a personal tracker.

Determine what type of entry the user is providing.

Possible types:
- "book_purchase" = a book the user has already bought
- "buy_list" = something the user wants to buy
- "build_list" = something the user wants to build or make

Return ONLY valid JSON. No markdown. No explanation.

For a book purchase:
{{
    "type": "book_purchase",
    "title": "",
    "author": null,
    "price": 0,
    "date_purchased": null,
    "category": null,
    "format": null
}}

For a buy list item:
{{
    "type": "buy_list",
    "item": "",
    "category": null,
    "est_price": null,
    "priority": "medium",
    "status": "pending",
    "date_added": "{today.isoformat()}"
}}

For a build list item:
{{
    "type": "build_list",
    "name": "",
    "description": null,
    "status": "idea",
    "date_added": "{today.isoformat()}",
    "date_updated": "{today.isoformat()}"
}}

Rules:
- Do not invent information.
- Dates may be written in various formats: DD/MM/YYYY, D/M/YY, DD-MM-YYYY, "29/9/2026", "29/2/26", "2-5-2027", etc.
- Always interpret ambiguous numeric dates as DD/MM/YYYY (day first, then month), never MM/DD/YYYY.
- 2-digit years (e.g. "26") should be interpreted as 20XX (e.g. 2026).
- Always convert the final date to YYYY-MM-DD format for storage, regardless of how it was written in the input.
- If information is not mentioned, use null.
- For book purchases, if no purchase date is mentioned, use null.
- Resolve relative dates such as "today" and "yesterday" using today's date: {today.isoformat()}.
- Buy list priority must be high, medium, or low.
- Build list status must be idea, in progress, done, or abandoned.

User input:
"{text}"
"""