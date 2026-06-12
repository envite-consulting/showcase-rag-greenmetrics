# Green Metrics Tool RAG Showcase

This repository contains a containerized Retrieval-Augmented Generation (RAG) system and Green Metrics Tool (GMT) usage scenarios for demonstrating how different RAG configurations can be measured and compared.

The showcase is intentionally small and self-contained. It uses a fixed arXiv document selection and a fixed question set so repeated runs stay comparable.

## Which Guide Should I Use?

| Environment | Recommended path                | Guide                                  |
|-------------|---------------------------------|----------------------------------------|
| Linux       | Run GMT locally                 | [README.linux.md](README.linux.md)     |
| Windows     | Use the free GMT hosted service | [README.windows.md](README.windows.md) |

Windows users should use the hosted GMT service instead of local measurements. Local Windows or WSL runs are useful for development, but they can produce limited or inconsistent measurement data depending on host support for metric providers.

## What Gets Measured

The measured RAG system consists of two services:

- `rag-app`: FastAPI application for indexing, retrieval, augmentation, and generation orchestration
- `ollama`: local LLM service used by the RAG app

The local scenario measures these phases:

1. `Warmup Indexing`
2. `Indexing`
3. `Warmup RAG`
4. `RAG Queries`

The hosted-service default [usage_scenario.yml](usage_scenario.yml) adds one initial `Prepare Dataset` phase because the hosted service clones the repository fresh and needs to download the fixed document set before indexing.

The fixed workload is defined by:

- [src/scripts/dataset.json](src/scripts/dataset.json): selected arXiv document IDs
- [src/scripts/questions.json](src/scripts/questions.json): questions used by the load script

## Scenarios

| File | Purpose |
| --- | --- |
| [usage_scenario.yml](usage_scenario.yml) | remote scenario for the GMT hosted service; defaults to `tinyllama:1.1b`, fewer questions, and shorter answers |
| [usage_scenario.local.yml](usage_scenario.local.yml) | local Linux scenario; defaults to `llama3:8b` |

Both scenarios expose the relevant RAG configuration through service environment values. For local Linux runs, edit [usage_scenario.local.yml](usage_scenario.local.yml). For hosted runs, keep [usage_scenario.yml](usage_scenario.yml) lightweight and adjust variables in the GMT Scenario Runner.

## Configuration

All base runtime parameters are defined in [.env.example](.env.example). The Compose files load this file through `env_file`; scenario files override individual values where needed.

Important variables:

| Variable                       | Meaning                                  |
|--------------------------------|------------------------------------------|
| `CHUNKING_STRATEGY`            | `simple` or `structure`                  |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | chunk sizing for indexing                |
| `EMBEDDING_MODEL`              | Sentence Transformer model               |
| `EMBEDDING_DEVICE`             | `cpu` or `cuda`                          |
| `POST_BM25_RERANK`             | enable BM25 re-ranking                   |
| `OLLAMA_MODEL`                 | model served by Ollama                   |
| `RAG_QUESTION_LIMIT`           | number of questions in the measured load |

## Structure

```text
showcase-rag-greenmetrics
├── README.md                   # overview and guide selection
├── README.linux.md             # local Linux measurement guide
├── README.windows.md           # hosted-service guide for Windows users
├── .env.example                # committed default runtime configuration
├── docker-compose.gmt.yml      # Compose file for GMT scenarios
├── docker-compose.yml          # local app execution without GMT
├── docker/
│   ├── Dockerfile
│   └── entrypoint.sh
├── emb_models/                 # local embedding cache
├── hf-cache/                   # Hugging Face cache
├── logs/
├── src/app/                    # RAG app
├── src/data/raw/               # downloaded arXiv texts
├── src/scripts/
│   ├── dataset.json            # fixed arXiv selection
│   ├── get_dataset.py
│   ├── questions.json
│   └── rag_queries.py
├── usage_scenario.yml          # hosted-service scenario
└── usage_scenario.local.yml    # local Linux scenario
```

## Sources

- [Green Metrics Tool documentation](https://docs.green-coding.io/)
- [GMT installation on Linux](https://docs.green-coding.io/docs/installation/installation-linux/)
- [Measuring locally with GMT](https://docs.green-coding.io/docs/measuring/measuring-locally/)
- [Measuring with the GMT hosted service](https://docs.green-coding.io/docs/measuring/measuring-service/)
