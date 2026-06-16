import chromadb
import shutil
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

from app.config import load_config, Config
from app.embedding import get_embed_model
from app.time_marker import mark

logger = logging.getLogger(__name__)

_MARKER_RE = re.compile(r"^(#{1,6})\s+(.*)\s*$")


@dataclass
class RawDocument:
    text: str
    metadata: Dict[str, Any]


# ========== LOAD DOCUMENTS ==========
#
# The showcase dataset currently contains .txt files only.
def _load_documents(data_dir: str) -> List[RawDocument]:
    base = Path(data_dir)
    docs: list[RawDocument] = []

    for path in base.rglob("*"):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()
        if suffix == ".txt":
            doc_type = "txt"
        else:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if not text.strip():
                logger.warning(f"Empty document: {path}")
                continue

            metadata = {
                "source": str(path),
                "type": doc_type,
            }
            docs.append(RawDocument(text=text, metadata=metadata))
        except Exception as e:
            logger.error(f"Failed to load {path}: {e}")

    logger.info(f"Loaded {len(docs)} documents.")
    return docs


# ========== CHUNKING ==========
#
# Implemented chunking strategies:
# 1. _simple_chunk(): fixed token chunk size and overlap.
# 2. _structure_chunk(): token chunking based on document structure.

def _token_chunk_ranges(text: str, tokenizer: Any, chunk_size: int, chunk_overlap: int) -> List[tuple[int, int]]:
    encoded = tokenizer(
        text,
        add_special_tokens=False,
        return_offsets_mapping=True,
        truncation=False,
    )
    offsets = encoded["offset_mapping"]

    if not offsets:
        return []

    ranges: list[tuple[int, int]] = []
    start_token = 0
    step = max(1, chunk_size - chunk_overlap)

    while start_token < len(offsets):
        end_token = min(start_token + chunk_size, len(offsets))
        token_offsets = [(start, end) for start, end in offsets[start_token:end_token] if end > start]

        if token_offsets:
            ranges.append((token_offsets[0][0], token_offsets[-1][1]))

        if end_token == len(offsets):
            break

        start_token += step

    return ranges


def _simple_chunk(doc: RawDocument, chunk_size: int, chunk_overlap: int, tokenizer: Any) -> List[RawDocument]:
    """
    Simple token-based chunking strategy with fixed chunk size and fixed chunk overlap.
    :param doc: Raw text document.
    :param chunk_size: Chunk size in tokens.
    :param chunk_overlap: Overlap between chunks in tokens.
    :param tokenizer: Tokenizer used by the embedding model.
    :return: List of chunked documents.
    """
    text = doc.text
    chunks: list[RawDocument] = []
    chunk_index = 0

    for start, end in _token_chunk_ranges(text, tokenizer, chunk_size, chunk_overlap):
        chunk_text = text[start:end]
        metadata = dict(doc.metadata)
        metadata["chunk_index"] = chunk_index
        metadata["chunk_start"] = start
        metadata["chunk_end"] = end
        if chunk_text.strip():
            chunks.append(RawDocument(text=chunk_text, metadata=metadata))
        chunk_index += 1

    return chunks


def _structure_chunk(doc: RawDocument, chunk_size: int, chunk_overlap: int, tokenizer: Any) -> List[RawDocument]:
    """
    Chunking based on the Markdown structure of the arXiv documents.
    Sections use # through ##### markers; special blocks use ###### markers
    such as Abstract, Theorem, Definition, Proof, and similar labels.
    Block information such as type and title is stored as chunk metadata
    together with the chunk start and end offsets.
    :param doc: Raw text document.
    :param chunk_size: Maximum chunk size in tokens.
    :param chunk_overlap: Overlap between chunks in tokens.
    :param tokenizer: Tokenizer used by the embedding model.
    :return: List of chunked documents.
    """
    from app.block_types import ALLOWED_BLOCK_TYPES, BLOCK_TYPES_ALIASES

    text = doc.text
    chunks: List[RawDocument] = []
    chunk_index = 0

    # Extract document title: "#..."; fallback to the first non-empty line.
    doc_title, first_non_empty = "", ""
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if not first_non_empty:
            first_non_empty = s

        m = _MARKER_RE.match(s)
        if m and len(m.group(1)) == 1:
            doc_title = (m.group(2).strip() or first_non_empty)
            break

    doc_title = doc_title or first_non_empty

    block_start = 0
    block_title = ""
    block_type = "text"

    def emit_chunk(chunk_text: str, start_abs: int, end_abs: int):
        nonlocal chunk_index
        meta = dict(doc.metadata)
        meta["doc_title"] = doc_title
        meta["block_title"] = block_title
        meta["block_type"] = block_type
        meta["chunk_index"] = chunk_index
        meta["chunk_start"] = start_abs
        meta["chunk_end"] = end_abs

        chunks.append(RawDocument(text=chunk_text, metadata=meta))
        chunk_index += 1

    # Split documents into Markdown blocks first, then into chunks.
    def finalize_block(block_end: int):
        if block_end <= block_start:
            return

        block_text = text[block_start:block_end]
        if not block_text.strip():
            return

        for start, end in _token_chunk_ranges(block_text, tokenizer, chunk_size, chunk_overlap):
            chunk_text = block_text[start:end]

            if chunk_text.strip():
                emit_chunk(chunk_text, block_start + start, block_start + end)

    pos = 0
    for line in text.splitlines(keepends=True):
        line_start = pos
        line_end = pos + len(line)
        pos = line_end

        marker = _MARKER_RE.match(line.rstrip("\r\n"))
        if not marker:
            continue

        finalize_block(line_start)

        hashes = marker.group(1)
        title = (marker.group(2).strip() or "")

        block_title = title
        seen_title = False
        if len(hashes) == 1 and not seen_title:
            block_type = "title"
            seen_title = True

        elif len(hashes) == 6:
            first = (title.split()[0] if title else "").lower()
            first = first.strip(" \t\r\n()[]{}<>\"'“”‘’").rstrip(".,;:")    # Filter punctuation.
            if (not first) or any(ch.isdigit() for ch in first):            # Filter numbering.
                block_type = "special"
            else:
                first = BLOCK_TYPES_ALIASES.get(first, first)
                block_type = first if first in ALLOWED_BLOCK_TYPES else "special"

        else:
            block_type = "heading"

        block_start = line_end

    finalize_block(len(text))
    return chunks


# ========== INDEXING ==========
def reset_index_dir(index_dir: str) -> None:
    p = Path(index_dir)
    if p.exists():
        logger.info(f"Resetting index folder {p} ...")
        shutil.rmtree(p)

    p.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created index folder: {p}.")


def _build_index(cfg: Config | None = None, reset_db: bool = False) -> None:
    if cfg is None:
        cfg = load_config()

    if reset_db:
        reset_index_dir(cfg.index_dir)

    logger.info(f"Loading embedding model {cfg.embedding_model} ...")
    model = get_embed_model(cfg)
    tokenizer = getattr(model, "tokenizer", None)
    if tokenizer is None:
        raise ValueError(f"Embedding model {cfg.embedding_model} does not expose a tokenizer.")

    # ========== 1. Load documents ==========
    logger.info(f"Loading documents from {cfg.data_dir} ...")
    docs = _load_documents(cfg.data_dir)

    # ========== 2. Chunk documents ==========
    logger.info("Chunking documents ...")
    chunked_docs: list[RawDocument] = []

    if cfg.chunking_strategy == "simple":
        chunk_func = _simple_chunk
    elif cfg.chunking_strategy == "structure":
        chunk_func = _structure_chunk
    else:
        logging.error(f"Unknown chunking strategy: {cfg.chunking_strategy}")
        raise ValueError()

    mark("CHUNKING_START")
    for doc in docs:
        chunked_docs.extend(chunk_func(
            doc,
            chunk_size=cfg.chunk_size,
            chunk_overlap=cfg.chunk_overlap,
            tokenizer=tokenizer,
        ))
    mark("CHUNKING_END")

    logger.info(f"Created {len(chunked_docs)} chunks.")

    if not chunked_docs:
        logger.warning("No chunks found. Aborting.")
        return

    # ========== 3. Embed documents ==========
    texts = [d.text for d in chunked_docs]
    logger.info("Computing embeddings ...")
    mark("EMBEDDING_START")
    embeddings = model.encode(
        texts,
        batch_size=128,
        convert_to_numpy=True,
        normalize_embeddings=cfg.normalize_embeddings,
        show_progress_bar=True
    )
    mark("EMBEDDING_END")

    # ========== 4. Create database ==========
    logger.info(f"Creating Chroma DB in {cfg.index_dir} ...")
    client = chromadb.PersistentClient(path=cfg.index_dir)

    # See https://cookbook.chromadb.dev/core/configuration/ for metadata details.
    collection = client.get_or_create_collection(
        "rag",
        metadata={
            "hnsw:space": "cosine",
            "hnsw:num_threads": 5,
            "hnsw:batch_size": 10_000,
            "hnsw:sync_threshold": 200_000,
            "ef_construction": cfg.hnsw_ef_construction,
            "ef_search": cfg.hnsw_ef_search,
            "max_neighbors": cfg.hnsw_max_neighbors,
        }
    )

    ids = [str(i) for i in range(len(chunked_docs))]
    metadatas = [d.metadata for d in chunked_docs]

    # Write to Chroma DB in batches (see https://cookbook.chromadb.dev/strategies/batching/).
    # This matters because Chroma DB usually accepts a maximum batch size of 5461.
    # The exact value is retrieved from client.get_max_batch_size(); "-1" adds a safety margin.
    logger.info("Saving embeddings ...")
    batch_size = client.get_max_batch_size() - 1
    total = len(chunked_docs)
    mark("PERSIST_IN_DB_START")

    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        batch_ids = ids[start:end]
        batch_embs = embeddings[start:end]
        batch_metas = metadatas[start:end]

        logger.debug(f"Adding batch {start}-{end} of {total} ...")
        collection.add(
            ids=batch_ids,
            embeddings=batch_embs,
            metadatas=batch_metas,
        )

    mark("PERSIST_IN_DB_END")

    logger.info("========== INDEXING DONE ==========")
    return


if __name__ == "__main__":
    from app.simple_logging import setup_logging

    setup_logging()
    _build_index()
