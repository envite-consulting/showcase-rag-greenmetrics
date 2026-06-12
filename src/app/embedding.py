import logging
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer

from app.config import Config

logger = logging.getLogger(__name__)

_model: SentenceTransformer | None = None


def _get_model_dir(cfg: Config) -> Path:
    base_dir = Path(cfg.embed_dir)
    safe_name = cfg.embedding_model.replace("/", "_")
    return base_dir / safe_name


def _ensure_local_model(cfg: Config) -> Path:
    model_dir = _get_model_dir(cfg)
    model_dir.mkdir(parents=True, exist_ok=True)

    if any(model_dir.iterdir()):
        logger.debug(f"Embedding model already exists: {model_dir}")
        return model_dir

    logger.debug(f"Embedding model not found: {cfg.embedding_model} will be downloaded ...")
    model = SentenceTransformer(cfg.embedding_model)
    model.save(str(model_dir))
    logger.debug(f"Embedding model saved to: {model_dir}")
    return model_dir


def get_embed_model(cfg: Config) -> SentenceTransformer:
    global _model
    if _model is not None:
        return _model

    device = cfg.embedding_device
    if device == "cuda":
        import torch
        if not torch.cuda.is_available():
            logger.warning("CUDA not found, using CPU instead.")
            device = "cpu"

    model_dir = _ensure_local_model(cfg)

    logger.debug(f"Loading embedding model {cfg.embedding_model} (device: {device}) ...")
    _model = SentenceTransformer(
        model_name_or_path=str(model_dir),
        device=device,
        local_files_only=True,
    )
    logger.info("Embedding model loaded.")
    return _model
