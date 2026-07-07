from app.rag.embeddings import HashingEmbeddingProvider


def test_hashing_embedding_dimension_and_type():
    provider = HashingEmbeddingProvider(vector_size=384)

    vector = provider.embed_text("PLC 16DI 8DO RS485 industrial automation")

    assert len(vector) == 384
    assert all(isinstance(value, float) for value in vector)


def test_hashing_embedding_is_stable_for_same_text():
    provider = HashingEmbeddingProvider(vector_size=384)
    text = "VFD 7.5kW 380V Modbus motor drive"

    assert provider.embed_text(text) == provider.embed_text(text)


def test_hashing_embedding_document_batch():
    provider = HashingEmbeddingProvider(vector_size=16)

    vectors = provider.embed_documents(["PLC", "HMI"])

    assert len(vectors) == 2
    assert all(len(vector) == 16 for vector in vectors)
