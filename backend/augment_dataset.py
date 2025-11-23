import json, random
from pathlib import Path

DATA_PATH = Path("../data/sample_chats.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

random.seed(42)

actions = ["check","cancel","change","track","return","refund","pay","update","reschedule","complain","ask"]
objects = ["my order","the order","my subscription","the product","my payment","shipment","my address","my account"]
phrases = [
    "Hi, can you {action} {object}?",
    "Hello, I want to {action} {object}.",
    "hey, pls {action} {object}",
    "Could you {action} {object} for me?",
    "{action_cap} {object} please",
    "Is it possible to {action} {object}?",
    "When will {object} be {action}ed?",
    "Am I able to {action} {object} now?"
]

action_to_intent = {
    "check": ["order","status"],
    "cancel": ["order","cancel"],
    "change": ["order","change"],
    "track": ["delivery","track"],
    "return": ["product","return"],
    "refund": ["refund","request"],
    "pay": ["payment","issue"],
    "update": ["account","update_info"],
    "reschedule": ["delivery","reschedule"],
    "complain": ["feedback","complaint"],
    "ask": ["help"]
}

existing = {(s['text'], tuple(s['intent']), s['language']) for s in data}
attempts = 0

while len(data) < 1000 and attempts < 50000:
    action = random.choice(actions)
    obj = random.choice(objects)
    template = random.choice(phrases)
    action_cap = action.capitalize()
    text = template.format(action=action, object=obj, action_cap=action_cap)

    if random.random() < 0.35:
        text = random.choice(["hii ", "hey ", ""]) + text
    if random.random() < 0.25:
        text = text + " #" + str(random.randint(1,9999))
    if random.random() < 0.18:
        text = text + " " + random.choice(["pls", "por favor", "porfa", "thanks"])
    if random.random() < 0.12:
        text = text.replace("order", random.choice(["order","ordr","odrer"]))

    intent = action_to_intent.get(action, ["unknown"])
    lang = "en"
    if random.random() < 0.12:
        text = text + " " + random.choice(["por favor","gracias","obrigado"])
        lang = "pt-es"

    sample = {"text": text, "intent": intent, "language": lang}
    key = (sample['text'], tuple(sample['intent']), sample['language'])

    if key not in existing:
        data.append(sample)
        existing.add(key)

    attempts += 1

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Augmented dataset size: {len(data)}")
