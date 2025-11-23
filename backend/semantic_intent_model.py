import joblib
import numpy as np
from data_loader import load_data
from embedding_extractor import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import re

MODEL_PATH = "semantic_intents.joblib"


# --------------------------
# Text normalization
# --------------------------
def clean_text(text: str) -> str:
    """
    Lowercase the text, remove non-alphanumeric characters, and strip spaces.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()


# --------------------------
# Train semantic intent model
# --------------------------
def train_semantic_intent() -> None:
    """
    Load chat data, generate embeddings, and save a semantic intent model.
    """
    data = load_data("../data/sample_chats.json")

    sentences = [clean_text(item["text"]) for item in data]
    intents = [item["intent"] for item in data]

    print("Generating embeddings...")
    embeddings = np.array([get_embedding(text) for text in sentences])

    joblib.dump({
        "sentences": sentences,
        "intents": intents,
        "embeddings": embeddings
    }, MODEL_PATH)

    print("Semantic model trained & saved!")


# --------------------------
# Predict intent using semantic similarity
# --------------------------
def predict_intent_semantic(
    message: str, 
    top_k: int = 3, 
    min_similarity: float = 0.42,
    return_scores: bool = False
) -> list:
    """
    Predict intents for a user message based on semantic similarity.

    Args:
        message (str): User message to predict intent for.
        top_k (int): Number of top similar sentences to consider.
        min_similarity (float): Minimum cosine similarity threshold.
        return_scores (bool): Whether to return similarity scores with intents.

    Returns:
        list: Matched intent(s). If return_scores=True, returns list of tuples (intent, score)
    """
    model = joblib.load(MODEL_PATH)

    sentences = model["sentences"]
    intents = model["intents"]
    embeddings = model["embeddings"]

    message_clean = clean_text(message)
    user_emb = get_embedding(message_clean).reshape(1, -1)

    sims = cosine_similarity(user_emb, embeddings)[0]

    # Sort indices descending by similarity
    idx = sims.argsort()[::-1]
    best_scores = [(i, sims[i]) for i in idx[:top_k]]

    matched_intents = set()
    matched_with_scores = []

    for i, score in best_scores:
        if score >= min_similarity:
            matched_intents.update(intents[i])
            if return_scores:
                matched_with_scores.extend([(label, score) for label in intents[i]])

    if not matched_intents:
        return [("no_intent_detected", 0.0)] if return_scores else ["no_intent_detected"]

    return matched_with_scores if return_scores else list(matched_intents)


# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    # Train the model
    train_semantic_intent()

    # Predict sample intents
    test_message = "I want to reset my password"
    print(predict_intent_semantic(test_message))
