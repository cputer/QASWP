import torch
import torch.nn as nn

# A simple vocabulary for demonstration purposes (e.g., HTTP requests)
VOCAB = {
    "<pad>": 0, "GET": 1, "POST": 2, "/api/v1/profile": 3, "/api/v1/data": 4, 
    "HTTP/1.1": 5, "Host:": 6, "example.com": 7,
}
VOCAB_SIZE = len(VOCAB)
REV_VOCAB = {v: k for k, v in VOCAB.items()}


class TinyLLM(nn.Module):
    """
    A simplified Transformer-based model to simulate neural semantic prediction.
    In a real implementation, this would be a pre-trained, fine-tuned model.
    """
    def __init__(self, vocab_size=VOCAB_SIZE, embed_dim=32, num_heads=2, hidden_dim=64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.transformer_encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads, dim_feedforward=hidden_dim, batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(self.transformer_encoder_layer, num_layers=1)
        self.output_layer = nn.Linear(embed_dim, vocab_size)

    def forward(self, src):
        embedded = self.embedding(src)
        encoded = self.transformer_encoder(embedded)
        # We only care about the prediction for the *next* token
        last_token_embedding = encoded[:, -1, :]
        logits = self.output_layer(last_token_embedding)
        return logits

    def predict_next_token(self, history_tokens):
        """Predicts the next token ID based on a sequence of previous token IDs."""
        if not isinstance(history_tokens, torch.Tensor):
            history_tokens = torch.tensor([history_tokens], dtype=torch.long)
        
        self.eval()  # Set model to evaluation mode
        with torch.no_grad():
            logits = self.forward(history_tokens)
            prediction = torch.argmax(logits, dim=-1)
        return prediction.item()
    
    def get_model_diff_hash(self):
        """Simulates creating a hash of model parameter differences for federated updates."""
        # In a real scenario, this would involve complex diffing (e.g., LoRA).
        # Here, we just hash the state dict for simplicity.
        import hashlib
        model_bytes = str(self.state_dict()).encode()
        return hashlib.sha256(model_bytes).digest()


if __name__ == "__main__":
    # Initialize and pre-train the model on some example sequences
    model = TinyLLM()
    # Example: A typical request is GET -> /api/v1/profile -> HTTP/1.1
    history = [VOCAB["GET"], VOCAB["/api/v1/profile"]]
    
    predicted_token_id = model.predict_next_token(history)
    predicted_token = REV_VOCAB.get(predicted_token_id, "<unk>")
    
    print(f"History: {[REV_VOCAB.get(t, '<unk>') for t in history]}")
    print(f"Model Prediction for next token: '{predicted_token}' (ID: {predicted_token_id})")
    print(f"Model Diff Hash (simulated): {model.get_model_diff_hash().hex()[:16]}...")
