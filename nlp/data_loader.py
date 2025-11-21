import json

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texts = [item['text'] for item in data]
    intents = [item['intent'] for item in data]
    return texts, intents

# Example usage
if __name__ == "__main__":
    texts, intents = load_data('../data/sample_chats.json')
    print(texts)
    print(intents)