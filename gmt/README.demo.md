# GMT Dashboard Demo Comparison

This document describes the prepared Green Metrics Tool (GMT) demo comparison for
the RAG showcase.

Dashboard comparison:

- [Baseline vs. Enhanced](https://metrics.green-coding.io/compare.html?ids=3fef4fab-d0ab-45f0-9be4-d44e253d35c1,403bb9ee-30d4-480f-bb0b-3f847f69efdb&force_mode=)
- [Baseline vs smallLLM+](https://metrics.green-coding.io/compare.html?ids=f2e7e2a0-dc5e-4997-91d6-cdebaa7b4ba6,403bb9ee-30d4-480f-bb0b-3f847f69efdb&force_mode=)

## Measurement Setup

All demo scenarios use:

- [docker-compose.demo.yml](docker-compose.demo.yml)
- [../src/scripts/dataset.demo.json](../src/scripts/dataset.demo.json): 1000 explicit arXiv document IDs
- [../src/scripts/questions.demo.json](../src/scripts/questions.demo.json): 50 document-specific single-turn questions
- `RAG_QUESTION_LIMIT=0`, so all 50 demo questions are executed

The demo compose file is intended for the hosted GMT ML machine. It enables GPU
access for `rag-app` and `ollama`, and mounts the hosted Ollama model volume
read-only into the `ollama` container. It pulls the prebuilt
`enviteconsulting/showcase-rag-greenmetrics:demo` image by default, avoiding a full
Python dependency installation during measurement setup.

## Scenarios

| Scenario  | File                                                                 | Purpose                                                            |
|-----------|----------------------------------------------------------------------|--------------------------------------------------------------------|
| Baseline  | [usage_scenario.demo_baseline.yml](usage_scenario.demo_baseline.yml) | Simple chunking without BM25 re-ranking                            |
| Enhanced  | [usage_scenario.demo_enhanced.yml](usage_scenario.demo_enhanced.yml) | Structure-aware chunking with BM25 re-ranking                      |
| Small LLM | [usage_scenario.demo_smallLLM.yml](usage_scenario.demo_smallLLM.yml) | Baseline retrieval setup with `llama3.2:3b` instead of `llama3:8b` |

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

The optional small-LLM scenario keeps the baseline retrieval setup constant and changes
only `OLLAMA_MODEL` from `llama3:8b` to `llama3.2:3b`.
