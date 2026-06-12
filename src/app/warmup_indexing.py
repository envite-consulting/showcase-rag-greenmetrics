import logging

from app.config import load_config
from app.simple_logging import setup_logging
from app.indexing import reset_index_dir
from app.embedding import get_embed_model

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    cfg = load_config()

    # Reset the existing database.
    reset_index_dir(cfg.index_dir)

    # Preload the embedding model and run a simple embedding operation.
    model = get_embed_model(cfg)
    embedding_1 = model.encode(["Small warmup"], convert_to_numpy=True)
    embedding_2 = model.encode(["Small warmup_"], convert_to_numpy=True)
    similarity = model.similarity(embedding_1, embedding_2)
    logger.debug(f"[WARMUP] Similarity check result: {similarity.item()}.")
    model.encode(["Small warmup"], convert_to_numpy=True)
    logger.info("========== WARMUP INDEXING DONE ==========")


if __name__ == '__main__':
    main()
