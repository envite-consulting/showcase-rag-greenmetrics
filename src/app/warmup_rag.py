import logging

from app.config import load_config
from app.simple_logging import setup_logging
from app.rag_pipeline import RagPipeline
from app.retrieval import get_collection
from app.embedding import get_embed_model

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    cfg = load_config()

    # Open the collection for preloading.
    collection = get_collection(cfg)
    logger.debug(f"[WARMUP] Collection size: {collection.count()} chunks.")
    result_10 = collection.get(ids="10")
    logger.debug(f"[WARMUP] Collection metadata for ID #10:\n{result_10.get("metadatas", [[]])}")

    # Preload the embedding model and run a simple embedding operation.
    model = get_embed_model(cfg)
    embedding_1 = model.encode(["Small warmup"], convert_to_numpy=True)
    embedding_2 = model.encode(["Small warmup_"], convert_to_numpy=True)
    similarity = model.similarity(embedding_1, embedding_2)
    logger.debug(f"[WARMUP] Test similarity result: {similarity.item()}.")

    # Call the LLM once.
    pipeline = RagPipeline(cfg)
    response = pipeline.llm.generate("This is a warmup. Answer with 'OK'.")
    logger.debug(f"[WARMUP] LLM response: {response}.")


if __name__ == '__main__':
    main()
    logger.info("========== WARMUP RAG APP DONE ==========")
