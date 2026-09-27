import torch
from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"

_model = None


def get_embedding_model():

    global _model

    if _model is None:

        if torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"

        print(f"Loading embedding model on: {device}")

        _model = SentenceTransformer(
            MODEL_NAME,
            device=device
        )

    return _model


def embed_texts(
    texts: list[str],
    batch_size: int = 32
):

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings.tolist()