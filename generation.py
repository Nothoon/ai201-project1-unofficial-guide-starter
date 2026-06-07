"""Stage 5 of the SDSU Off-Campus Housing RAG pipeline: grounded generation.

Implements the **Generation** stage from ``planning.md`` (see the
"Architecture" diagram and "AI Tool Plan" -> Generation):

    LLM: llama-3.3-70b-versatile (served by Groq)

    prompt = system grounding instructions
           + [6 retrieved chunks as context]
           + user question

The model is constrained to answer ONLY from the retrieved chunks and to cite
its sources. If the retrieved context does not contain the answer, it is
instructed to say it does not have enough information.

The Groq API key is read from ``GROQ_API_KEY`` in ``.env``.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from embedding import TOP_K, retrieve

# --- Configuration (from planning.md "Architecture") -------------------------
LLM_MODEL = "llama-3.3-70b-versatile"  # served by Groq

load_dotenv(Path(__file__).parent / ".env")

_client: Groq | None = None


def get_groq_client() -> Groq:
    """Load (once) and return a Groq client authenticated from GROQ_API_KEY."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_key_here":
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add your key to the .env file."
            )
        _client = Groq(api_key=api_key)
    return _client


# --- Grounding prompt --------------------------------------------------------
# The system prompt forces the model to stay inside the retrieved context,
# attribute its claims, and refuse to answer when the context is insufficient.
SYSTEM_PROMPT = """\
You are the Unofficial Guide to off-campus housing for SDSU students. You \
answer questions using ONLY the retrieved context provided below, which is \
drawn from student posts, reviews, and articles.

Rules you must follow:
1. Answer ONLY using information found in the retrieved context. Do not use \
outside knowledge, and do not guess or infer beyond what the context says.
2. If the retrieved context does not contain enough information to answer the \
question, respond with exactly: "I don't have enough information to answer \
that." Do not try to fill the gap.
3. Attribute your claims. When you state something, indicate which source it \
came from (apartment name and/or platform).
4. Distinguish between a single review and a repeated pattern when the context \
supports it.
5. After your answer, include a "Sources:" section listing the distinct \
sources you used, formatted as: "- <apartment or platform> (<source_url>)". \
Only list sources you actually drew from.

Keep the answer concise and grounded in the evidence."""


def format_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a numbered context block for the prompt."""
    blocks: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]
        apartment = meta.get("apartment") or "General"
        platform = meta.get("platform") or "Unknown"
        source_url = meta.get("source_url") or "n/a"
        blocks.append(
            f"[Source {index}] apartment: {apartment} | platform: {platform} "
            f"| url: {source_url}\n{chunk['text']}"
        )
    return "\n\n".join(blocks)


def build_user_prompt(question: str, chunks: list[dict]) -> str:
    """Assemble the user message: retrieved context + the question."""
    if not chunks:
        context = "(no relevant context was retrieved)"
    else:
        context = format_context(chunks)
    return (
        "Retrieved context:\n"
        "----------------------------------------\n"
        f"{context}\n"
        "----------------------------------------\n\n"
        f"Question: {question}"
    )


def generate_answer(question: str, top_k: int = TOP_K) -> dict:
    """Run the full retrieve -> ground -> generate pipeline for one question.

    Returns a dict with the model ``answer`` and the ``chunks`` that were
    retrieved and used as context (useful for the interface and evaluation).
    """
    chunks = retrieve(question, top_k=top_k)
    user_prompt = build_user_prompt(question, chunks)

    client = get_groq_client()
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,  # low temperature keeps the answer close to the text
    )
    answer = response.choices[0].message.content.strip()
    return {"answer": answer, "chunks": chunks}


if __name__ == "__main__":
    # Quick smoke test against an evaluation question.
    result = generate_answer("What amenities are mentioned for The Rive?")
    print(result["answer"])
    print("\n--- retrieved", len(result["chunks"]), "chunks ---")
