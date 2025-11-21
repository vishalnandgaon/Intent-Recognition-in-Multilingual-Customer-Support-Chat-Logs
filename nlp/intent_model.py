from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
from data_loader import load_data

def train_intent_classifier():
    texts, intents = load_data('../data/sample_chats.json')
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    clf = MultinomialNB()
    clf.fit(X, intents)
    joblib.dump((vectorizer, clf), 'intent_classifier.joblib')

def predict_intent(message):
    vectorizer, clf = joblib.load('intent_classifier.joblib')
    X = vectorizer.transform([message])
    intent = clf.predict(X)[0]
    return intent

# Train model (run once)
if __name__ == "__main__":
    train_intent_classifier()
    print(predict_intent("Hello, I need help with my order."))