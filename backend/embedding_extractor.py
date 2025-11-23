from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
model = AutoModel.from_pretrained("xlm-roberta-base")

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element: token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def get_embedding(text):
    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=64,
        padding=True
    )

    with torch.no_grad():
        model_output = model(**encoded)

    embedding = mean_pooling(model_output, encoded["attention_mask"])
    return embedding.squeeze().numpy()

# Test
if __name__ == "__main__":
    emb = get_embedding("Hola, quiero saber el estado de mi pedido.")
    print("Embedding shape:", emb.shape)
