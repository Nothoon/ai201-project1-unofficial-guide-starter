"""Gradio interface for the SDSU Off-Campus Housing RAG system.

Ties the whole pipeline together for end users: a question is embedded and
matched against the ChromaDB vector store (Stage 4), the top-k chunks are fed
to the grounded llama-3.3-70b-versatile prompt (Stage 5), and the answer is
displayed alongside the retrieved chunks it was grounded in.

Prerequisites:
    1. Build the vector store first:   python embedding.py
    2. Set GROQ_API_KEY in .env
    3. Launch the interface:           python app.py
"""

from __future__ import annotations

from embedding import TOP_K
from generation import generate_answer

import gradio as gr

EXAMPLE_QUESTIONS = [
    "What amenities are mentioned for The Rive?",
    "What do students/reviewers say about maintenance at 5025?",
    "What complaints are there about parking at Union Grantville?",
    "What rent range do students mention for off-campus housing near SDSU?",
    "Which apartment complexes are mentioned most often?",
]


def _format_sources(chunks: list[dict]) -> str:
    """Render the retrieved chunks as a readable markdown evidence list."""
    if not chunks:
        return "_No chunks were retrieved._"

    lines: list[str] = [f"### Retrieved context ({len(chunks)} chunks)\n"]
    for index, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]
        apartment = meta.get("apartment") or "General"
        platform = meta.get("platform") or "Unknown"
        source_url = meta.get("source_url") or ""
        similarity = chunk.get("similarity", 0.0)

        header = f"**[{index}] {apartment} · {platform} · similarity {similarity:.2f}**"
        if source_url:
            header += f"  \n{source_url}"
        snippet = chunk["text"].strip().replace("\n", " ")
        lines.append(f"{header}\n\n> {snippet}\n")
    return "\n".join(lines)


def answer_question(question: str) -> tuple[str, str]:
    """Gradio callback: return (answer markdown, retrieved-context markdown)."""
    question = (question or "").strip()
    if not question:
        return "Please enter a question.", ""

    try:
        result = generate_answer(question, top_k=TOP_K)
    except Exception as exc:  # surface config/API errors in the UI
        return f"**Error:** {exc}", ""

    return result["answer"], _format_sources(result["chunks"])


def build_interface() -> gr.Blocks:
    with gr.Blocks(title="SDSU Unofficial Housing Guide") as demo:
        gr.Markdown(
            "# 🏠 The Unofficial Guide — SDSU Off-Campus Housing\n"
            "Ask about off-campus apartments near SDSU. Answers are grounded "
            "**only** in collected student posts, reviews, and articles — "
            "with sources cited. If the sources don't cover your question, the "
            "guide will say so rather than guess."
        )

        with gr.Row():
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. What amenities are mentioned for The Rive?",
                lines=2,
                scale=4,
            )
            ask_button = gr.Button("Ask", variant="primary", scale=1)

        gr.Examples(examples=EXAMPLE_QUESTIONS, inputs=question_box)

        answer_box = gr.Markdown(label="Answer")
        with gr.Accordion("Show retrieved context", open=False):
            sources_box = gr.Markdown()

        ask_button.click(
            answer_question,
            inputs=question_box,
            outputs=[answer_box, sources_box],
        )
        question_box.submit(
            answer_question,
            inputs=question_box,
            outputs=[answer_box, sources_box],
        )

    return demo


if __name__ == "__main__":
    build_interface().launch()
