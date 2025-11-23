import json
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    processed = []
    for item in data:
        text = item['text'].lower()
        try:
            lang = detect(text)
        except:
            lang = item.get('language', 'unknown')
        processed.append({
            'text': text,
            'intent': item['intent'],
            'language': lang
        })
    return processed

# Example usage
if __name__ == "__main__":
    data = load_data('../data/sample_chats.json')
    print(data)