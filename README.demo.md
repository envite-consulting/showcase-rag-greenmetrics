# GMT Dashboard Demo Comparison

This document describes the prepared Green Metrics Tool (GMT) demo comparison for
the RAG showcase.

Dashboard comparison:

- TODO: add GMT dashboard comparison link

## Measurement Setup

Both demo scenarios use:

- [docker-compose.demo.yml](docker-compose.demo.yml)
- [src/scripts/dataset.demo.json](src/scripts/dataset.demo.json): 1000 explicit arXiv document IDs
- [src/scripts/questions.demo.json](src/scripts/questions.demo.json): 50 document-specific single-turn questions
- `OLLAMA_MODEL=llama3:8b`
- `RAG_QUESTION_LIMIT=0`, so all 50 demo questions are executed

The demo compose file is intended for the hosted GMT ML machine. It enables GPU
access for `rag-app` and `ollama`, and mounts the hosted Ollama model volume
read-only into the `ollama` container.

## Scenarios

| Scenario | File                                                                 | Purpose                                       |
|----------|----------------------------------------------------------------------|-----------------------------------------------|
| Baseline | [usage_scenario.demo_baseline.yml](usage_scenario.demo_baseline.yml) | Simple chunking without BM25 re-ranking       |
| Enhanced | [usage_scenario.demo_enhanced.yml](usage_scenario.demo_enhanced.yml) | Structure-aware chunking with BM25 re-ranking |

## Configuration Difference

| Variable            | Baseline | Enhanced    |
|---------------------|----------|-------------|
| `CHUNKING_STRATEGY` | `simple` | `structure` |
| `CHUNK_SIZE`        | `192`    | `192`       |
| `CHUNK_OVERLAP`     | `24`     | `24`        |
| `POST_BM25_RERANK`  | `False`  | `True`      |
| `TOP_K`             | `5`      | `5`         |
| `MAX_TOKENS`        | `512`    | `512`       |

The comparison keeps the dataset, question workload, model, top-k, token limit, and
hosted machine constant. The intended comparison is the effect of structure-aware
chunking plus BM25 re-ranking on the measured GMT phases.
