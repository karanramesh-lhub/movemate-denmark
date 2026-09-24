from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"

_embedding_model = TextEmbedding(model_name=MODEL_NAME)


def embed_text(text: str) -> list[float]:
   
    embedding = next(_embedding_model.embed([text]))
    return embedding.tolist()