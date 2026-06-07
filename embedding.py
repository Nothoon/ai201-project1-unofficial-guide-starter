"""Stage 3 + 4 of the SDSU Off-Campus Housing RAG pipeline.

Implements the **Embedding + Vector Store** and **Retrieval** stages from
``planning.md`` (see the "Retrieval Approach" and "Architecture" sections):

    Embedding model: sentence-transformers (all-MiniLM-L6-v2)
    Vector store:    ChromaDB (persisted on disk)
    Similarity:      cosine
    Top-k:           6 chunks

Stage 3 loads the labeled chunk dicts produced by
``ingestion_and_chunking.py`` (``chunks.json``), embeds each chunk's text with
all-MiniLM-L6-v2, and stores the vectors in a persistent ChromaDB collection
alongside the chunk metadata (source URL, platform, apartment, chunk id).

Stage 4 embeds an incoming user query with the same model and asks ChromaDB
for the 6 most similar chunks by cosine similarity.

Run this file directly to (re)build the vector store from ``chunks.json`` and
run a couple of sanity-check retrievals:

    python embedding.py
"""

from __future__ import annotations

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# --- Configuration (from planning.md "Retrieval Approach") -------------------
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"  # sentence-transformers
TOP_K = 6                              # chunks returned per query
COLLECTION_NAME = "sdsu_housing"

# ChromaDB persists to disk so the store survives between runs and the
# generation stage can reuse it without re-embedding.
PROJECT_DIR = Path(__file__).parent
CHROMA_DIR = PROJECT_DIR / "chroma_db"
CHUNKS_PATH = PROJECT_DIR / "chunks.json"

# Lazily-initialized singletons so the (slow) model load and the Chroma client
# connection only happen once per process.
_model: SentenceTransformer | None = None
_client: chromadb.ClientAPI | None = None


def get_model() -> SentenceTransformer:
    """Load (once) and return the all-MiniLM-L6-v2 embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model


def get_client() -> chromadb.ClientAPI:
    """Return a persistent ChromaDB client backed by ``CHROMA_DIR``."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings with all-MiniLM-L6-v2.

    Embeddings are L2-normalized so that ChromaDB's cosine space (and any
    downstream dot-product comparison) behaves as expected.
    """
    model = get_model()
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return embeddings.tolist()


def _clean_metadata(chunk: dict) -> dict:
    """Build a ChromaDB-safe metadata dict for a chunk.

    ChromaDB only accepts str / int / float / bool metadata values, so the
    ``apartment``/``source_url`` fields (which may be ``None`` for general
    threads and articles) are coerced to empty strings.
    """
    return {
        "source_file": chunk.get("source_file") or "",
        "source_url": chunk.get("source_url") or "",
        "platform": chunk.get("platform") or "",
        "apartment": chunk.get("apartment") or "",
        "char_count": int(chunk.get("char_count", 0)),
        "unit_index": int(chunk.get("unit_index", 0)),
        "chunk_index": int(chunk.get("chunk_index", 0)),
    }


def load_chunks(chunks_path: Path = CHUNKS_PATH) -> list[dict]:
    """Load the labeled chunk dicts produced by the chunking stage."""
    if not chunks_path.exists():
        raise FileNotFoundError(
            f"{chunks_path} not found. Run ingestion_and_chunking.py first."
        )
    return json.loads(chunks_path.read_text(encoding="utf-8"))


def build_vector_store(
    chunks: list[dict] | None = None,
    *,
    reset: bool = True,
) -> chromadb.Collection:
    """Embed every chunk and store it in ChromaDB (Stage 3).

    Args:
        chunks: Labeled chunk dicts. If ``None``, loaded from ``chunks.json``.
        reset:  When True, delete any existing collection first so the store is
                rebuilt cleanly (avoids stale/duplicate chunks).

    Returns:
        The populated ChromaDB collection.
    """
    if chunks is None:
        chunks = load_chunks()
    if not chunks:
        raise ValueError("No chunks to embed.")

    client = get_client()
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            # Collection didn't exist yet — nothing to delete.
            pass

    # cosine space matches the "cosine similarity" retrieval spec.
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [chunk["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [_clean_metadata(chunk) for chunk in chunks]

    print(f"Embedding {len(documents)} chunks with {EMBED_MODEL_NAME} ...")
    embeddings = embed_texts(documents)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )
    print(f"Stored {collection.count()} chunks in ChromaDB at {CHROMA_DIR}")
    return collection


def get_collection() -> chromadb.Collection:
    """Return the existing housing collection (built by build_vector_store)."""
    return get_client().get_collection(COLLECTION_NAME)


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Return the ``top_k`` chunks most similar to ``query`` (Stage 4).

    The query is embedded with the same all-MiniLM-L6-v2 model used for the
    chunks, then compared against the stored vectors by cosine similarity.

    Returns:
        A list of result dicts (most similar first), each containing the chunk
        ``chunk_id``, ``text``, ``metadata``, and a ``similarity`` score in
        ``[0, 1]`` (``1 - cosine_distance``).
    """
    collection = get_collection()
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # Chroma returns a list-per-query; we only sent one query, so take index 0.
    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved: list[dict] = []
    for chunk_id, document, metadata, distance in zip(
        ids, documents, metadatas, distances
    ):
        retrieved.append(
            {
                "chunk_id": chunk_id,
                "text": document,
                "metadata": metadata,
                "similarity": 1.0 - distance,  # cosine distance -> similarity
            }
        )
    return retrieved


if __name__ == "__main__":
    # Stage 3: (re)build the vector store from the chunked documents.
    build_vector_store()

    # Stage 4: sanity-check retrieval against a couple of evaluation questions.
    sample_queries = [
        "What amenities are mentioned for The Rive?",
        "What do reviewers say about maintenance at 5025?",
    ]
    for query in sample_queries:
        print("\n" + "=" * 70)
        print(f"QUERY: {query}")
        print("=" * 70)
        for rank, result in enumerate(retrieve(query), start=1):
            meta = result["metadata"]
            label = meta["apartment"] or meta["platform"]
            print(
                f"\n[{rank}] similarity={result['similarity']:.3f}  "
                f"({label} — {meta['source_file']})"
            )
            print("    " + result["text"][:200].replace("\n", " ") + " ...")
