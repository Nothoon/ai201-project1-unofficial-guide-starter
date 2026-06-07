"""Stage 1 + 2 of the SDSU Off-Campus Housing RAG pipeline.

Ingests raw ``.txt`` sources from the ``documents/`` folder and chunks them
according to the Chunking Strategy in ``planning.md``:

    Chunk size: 800 characters
    Overlap:    150 characters

Strategy: each document is first split into *natural units* (Reddit
comments, Yelp reviews, article paragraphs) on blank lines. Any unit that
is <= 800 characters is kept intact (most short reviews stay whole). Units
longer than 800 characters are split into overlapping windows of 800
characters with 150 characters of overlap so apartment names and complaints
near a boundary are preserved.

Each chunk is returned as a dictionary labeled with metadata (source URL,
platform, apartment name, and a unique chunk id) ready for Stage 3
(embedding + ChromaDB).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

# --- Chunking parameters (from planning.md "Chunking Strategy") --------------
CHUNK_SIZE = 800   # characters
OVERLAP = 150      # characters

# Folder containing the manually-collected raw .txt sources.
DOCUMENTS_DIR = Path(__file__).parent / "documents"

# The raw .txt files do not carry metadata headers, so we map each filename
# to the source metadata recorded in the planning.md "Documents" table.
# apartment=None means the source is a general thread/article, not tied to a
# single complex.
SOURCE_METADATA: dict[str, dict[str, Optional[str]]] = {
    "5025_Yelp_Reviews.txt": {
        "platform": "Yelp",
        "apartment": "5025",
        "source_url": "https://www.yelp.com/biz/fifty-twenty-five-san-diego-4",
    },
    "The_Rive_Yelp_Reviews.txt": {
        "platform": "Yelp",
        "apartment": "The Rive",
        "source_url": "https://www.yelp.com/biz/the-rive-san-diego-4",
    },
    "Union_Grantville_Yelp_Reviews.txt": {
        "platform": "Yelp",
        "apartment": "Union Grantville",
        "source_url": "https://www.yelp.com/biz/union-grantville-san-diego",
    },
    "Housing_Article.txt": {
        "platform": "Article",
        "apartment": None,
        "source_url": "https://www.unishack.com/blog/top-5-best-apartments-near-sdsu-for-off-campus-student-housing",
    },
    "Reddit_Thread_One.txt": {
        "platform": "Reddit",
        "apartment": None,
        "source_url": "https://www.reddit.com/r/SDSU/comments/1rd1srd/off_campus_housing",
    },
    "Reddit_Thread_Two.txt": {
        "platform": "Reddit",
        "apartment": None,
        "source_url": "https://www.reddit.com/r/SDSU/comments/1jvomnt/trying_to_find_off_campus_housing_as_a_transfer/",
    },
    "Reddit_Thread_Three.txt": {
        "platform": "Reddit",
        "apartment": None,
        "source_url": "https://www.reddit.com/r/SDSU/comments/1jjml66/where_to_live_offcampus/",
    },
    "Reddit_Thread_Four.txt": {
        "platform": "Reddit",
        "apartment": None,
        "source_url": "https://www.reddit.com/r/SDSU/comments/1s3vvzl/i_got_accepted_housing/",
    },
    "Reddit_Thread_Five.txt": {
        "platform": "Reddit",
        "apartment": None,
        "source_url": "https://www.reddit.com/r/SDSU/comments/1r63ttx/off_campus_living/",
    },
    "Reddit_Thread_Six.txt": {
        "platform": "Reddit",
        "apartment": None,
        "source_url": "https://www.reddit.com/r/SDSU/comments/1lq9pjr/im_panicking/",
    },
}

# Standalone structural labels that are not content units themselves.
_MARKER_LINES = {"post:", "replies:", "reply:", "pros:", "cons:", "con's:"}


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Split a single string into overlapping fixed-size character windows.

    Text at or below ``chunk_size`` is returned unchanged as a single chunk.
    Longer text is sliced into windows of ``chunk_size`` characters that each
    overlap the previous window by ``overlap`` characters.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    if len(text) <= chunk_size:
        return [text] if text else []

    step = chunk_size - overlap
    chunks: list[str] = []
    start = 0
    while start < len(text):
        window = text[start:start + chunk_size].strip()
        if window:
            chunks.append(window)
        if start + chunk_size >= len(text):
            break
        start += step
    return chunks


def split_into_units(raw_text: str) -> list[str]:
    """Split a document into natural units (paragraphs / comments / reviews).

    Units are separated by one or more blank lines. Standalone structural
    markers such as ``Post:`` or ``Replies:`` are dropped, and a leading
    marker on the same line as content (e.g. ``Post:\\nSrsly...``) is removed.
    """
    raw_units = re.split(r"\n\s*\n", raw_text)
    units: list[str] = []
    for unit in raw_units:
        unit = unit.strip()
        if not unit:
            continue
        # Drop a leading standalone marker line if content follows it.
        lines = unit.split("\n")
        if lines[0].strip().lower() in _MARKER_LINES:
            lines = lines[1:]
            unit = "\n".join(lines).strip()
        # Drop the unit entirely if it is nothing but a marker.
        if not unit or unit.lower() in _MARKER_LINES:
            continue
        units.append(unit)
    return units


def chunk_file(file_path: Path) -> list[dict]:
    """Ingest one ``.txt`` file and return a list of labeled chunk dicts."""
    filename = file_path.name
    metadata = SOURCE_METADATA.get(filename)
    if metadata is None:
        # Fall back to deriving metadata from the filename so unknown files
        # still ingest rather than crash.
        metadata = {
            "platform": "Unknown",
            "apartment": None,
            "source_url": None,
        }

    stem = file_path.stem
    raw_text = file_path.read_text(encoding="utf-8")
    units = split_into_units(raw_text)

    chunks: list[dict] = []
    for unit_index, unit in enumerate(units):
        for chunk_index, piece in enumerate(chunk_text(unit)):
            chunks.append(
                {
                    "chunk_id": f"{stem}__u{unit_index}__c{chunk_index}",
                    "text": piece,
                    "char_count": len(piece),
                    "source_file": filename,
                    "source_url": metadata["source_url"],
                    "platform": metadata["platform"],
                    "apartment": metadata["apartment"],
                    "unit_index": unit_index,
                    "chunk_index": chunk_index,
                }
            )
    return chunks


def ingest_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[dict]:
    """Ingest and chunk every ``.txt`` file in ``documents_dir``."""
    all_chunks: list[dict] = []
    for file_path in sorted(documents_dir.glob("*.txt")):
        all_chunks.extend(chunk_file(file_path))
    return all_chunks


if __name__ == "__main__":
    chunks = ingest_documents()

    # Summary, so the output can be eyeballed against the spec.
    print(f"Ingested {len(chunks)} chunks from {DOCUMENTS_DIR}")
    by_file: dict[str, int] = {}
    oversized = 0
    for chunk in chunks:
        by_file[chunk["source_file"]] = by_file.get(chunk["source_file"], 0) + 1
        if chunk["char_count"] > CHUNK_SIZE:
            oversized += 1

    print("\nChunks per source file:")
    for filename, count in sorted(by_file.items()):
        print(f"  {filename}: {count}")

    print(f"\nChunks over {CHUNK_SIZE} chars (should be 0): {oversized}")

    if chunks:
        print("\nExample chunk:")
        example = chunks[0]
        preview = {k: v for k, v in example.items() if k != "text"}
        print(json.dumps(preview, indent=2))
        print("  text:", example["text"][:200], "...")

    # Persist the chunks so Stage 3 (embedding + ChromaDB) can load them.
    out_path = Path(__file__).parent / "chunks.json"
    out_path.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    print(f"\nWrote {len(chunks)} chunks to {out_path}")
