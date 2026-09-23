import json

from parser import parse_entry
from database import insert_entry


# ----- Main program -----

while True:
    user_input = input("What are we tracking today sire?")

    if user_input.strip() == "":
        print("All noted, Have an awesome day/night! Exiting now.")
        break

    entry = parse_entry(user_input)

    print("Final entry:")
    print(json.dumps(entry, indent=2))

    insert_entry(entry)

    print(f"Added to {entry['type']} successfully :D")