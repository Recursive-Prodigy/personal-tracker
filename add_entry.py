import json

from parser import parse_entry
from database import insert_entry


# ----- Main program -----

user_input = input("What do you want to track? ")

entry = parse_entry(user_input)

entry = insert_entry(entry)

print("Final entry:")
print(json.dumps(entry, indent=2))

print(f"Added to {entry['type']} successfully :D")