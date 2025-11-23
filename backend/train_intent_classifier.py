import joblib
from embedding_extractor import get_embedding

# Load the trained model
clf, all_labels = joblib.load("intent_classifier.joblib")


def predict_intent_semantic(texts):
    """
    Predicts intents for a list of texts using the trained classifier.

    Args:
        texts (list of str): List of text inputs.

    Returns:
        list of list of str: Predicted intents for each text.
    """
    if isinstance(texts, str):
        texts = [texts]

    # Extract embeddings
    X = [get_embedding(text) for text in texts]

    # Predict
    preds = clf.predict(X)

    # Convert binary predictions to label names
    results = []
    for pred in preds:
        predicted_labels = [label for label, flag in zip(all_labels, pred) if flag]
        results.append(predicted_labels)

    return results


# Example usage
if __name__ == "__main__":
    sample_texts = [
        "I want to check my account balance",
        "How do I reset my password?"
    ]
    predictions = predict_intent_semantic(sample_texts)
    for text, pred in zip(sample_texts, predictions):
        print(f"Text: {text}\nPredicted intents: {pred}\n")
