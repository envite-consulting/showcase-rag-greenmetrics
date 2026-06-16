# Green Metrics Tool RAG Showcase

This repository contains a containerized Retrieval-Augmented Generation (RAG) system and Green Metrics Tool (GMT) usage scenarios for demonstrating how different RAG configurations can be measured and compared.

The showcase is intentionally small and self-contained. It uses a fixed arXiv document selection and a fixed question set so repeated runs stay comparable.

## Which Guide Should I Use?

| Environment | Recommended path                | Guide                                  |
|-------------|---------------------------------|----------------------------------------|
| Linux       | Run GMT locally                 | [README.linux.md](README.linux.md)     |
| Windows     | Use the free GMT hosted service | [README.windows.md](README.windows.md) |
| Live demo   | Prepared dashboard comparison   | [README.demo.md](README.demo.md)       |

Windows users should use the hosted GMT service instead of local measurements. Local WSL runs are useful for development, but they can produce limited or inconsistent measurement data depending on host support for metric providers.

## What Gets Measured

The measured RAG system consists of two services:

- `rag-app`: FastAPI application for indexing, retrieval, augmentation, and generation orchestration
- `ollama`: local LLM service used by the RAG app

Both scenarios measure these phases:

1. `Prepare Dataset`
2. `Warmup Indexing`
3. `Indexing`
4. `Pull Ollama Model`
5. `Warmup RAG`
6. `RAG Queries`

The `Prepare Dataset` phase downloads the fixed document set inside the measured container before indexing.

The fixed workload is defined by:

- [src/scripts/dataset.json](src/scripts/dataset.json): selected arXiv document IDs
- [src/scripts/questions.json](src/scripts/questions.json): questions used by the load script
- [src/scripts/dataset.demo.json](src/scripts/dataset.demo.json): larger arXiv workload with 1000 explicit document IDs for prepared full-service demo measurements
- [src/scripts/questions.demo.json](src/scripts/questions.demo.json): 50 document-specific single-turn questions for energy-measurement-focused demo runs

## Scenarios

| File                                                                 | Purpose                                                                                                           |
|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| [usage_scenario.yml](usage_scenario.yml)                             | remote scenario for the GMT hosted service; defaults to `tinyllama:1.1b`, fewer questions, and shorter answers    |
| [usage_scenario.local.yml](usage_scenario.local.yml)                 | local Linux scenario; defaults to `llama3:8b`                                                                     |
| [usage_scenario.demo_baseline.yml](usage_scenario.demo_baseline.yml) | fuller hosted-service baseline with 1000 arXiv documents and 50 questions for prepared dashboard comparisons      |
| [usage_scenario.demo_enhanced.yml](usage_scenario.demo_enhanced.yml) | fuller hosted-service scenario with 1000 arXiv documents, 50 questions, structured retrieval, and BM25 re-ranking |
| [usage_scenario.demo_smallLLM.yml](usage_scenario.demo_smallLLM.yml) | fuller hosted-service scenario with baseline retrieval and `phi3:mini` instead of `llama3:8b`                     |

The RAG app defaults are defined in [src/app/config.yaml](src/app/config.yaml). Variables declared in the `usage_scenario.*.yml` files override these defaults. For local Linux runs, edit [usage_scenario.local.yml](usage_scenario.local.yml) before starting the measurement. For hosted runs, keep [usage_scenario.yml](usage_scenario.yml) lightweight and adjust variables in the GMT Scenario Runner.

## Configuration

Base runtime parameters are defined by [src/app/config.yaml](src/app/config.yaml). The GMT scenario files override individual values where needed.

Important variables:

| Variable                       | Meaning                                  |
|--------------------------------|------------------------------------------|
| `CHUNKING_STRATEGY`            | `simple` or `structure`                  |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | chunk sizing for indexing                |
| `EMBEDDING_MODEL`              | Sentence Transformer model               |
| `POST_BM25_RERANK`             | enable BM25 re-ranking                   |
| `TOP_K`                        | number of retrieved text segments used as context |
| `OLLAMA_MODEL`                 | model served by Ollama                   |
| `RAG_QUESTION_LIMIT`           | number of questions in the measured load |

## Structure

```text
showcase-rag-greenmetrics
├── README.md                         # overview and guide selection
├── README.demo.md                    # prepared dashboard comparison
├── README.linux.md                   # local Linux measurement guide
├── README.windows.md                 # hosted-service guide for Windows users
├── docker-compose.yml                # local app execution without GMT
├── docker-compose.gmt.yml            # default GMT compose file
├── docker-compose.demo.yml           # hosted GPU demo compose file
├── docker/
│   └── Dockerfile
├── usage_scenario.yml                # lightweight hosted-service scenario
├── usage_scenario.local.yml          # local Linux GMT scenario
├── usage_scenario.demo_baseline.yml  # prepared demo baseline run
├── usage_scenario.demo_enhanced.yml  # prepared demo comparison run
├── usage_scenario.demo_smallLLM.yml  # prepared demo small-LLM run
├── requirements.txt
├── src/
│   ├── app/                          # RAG app
│   ├── scripts/                      # dataset, question, and workload scripts
│   ├── data/raw/                     # downloaded arXiv texts
│   └── data/index/                   # generated Chroma index
├── emb_models/                       # local embedding model cache
├── hf-cache/                         # local Hugging Face cache
└── logs/                             # runtime logs
```

## Sources

- [Green Metrics Tool documentation](https://docs.green-coding.io/)
- [GMT installation on Linux](https://docs.green-coding.io/docs/installation/installation-linux/)
- [Measuring locally with GMT](https://docs.green-coding.io/docs/measuring/measuring-locally/)
- [Measuring with the GMT hosted service](https://docs.green-coding.io/docs/measuring/measuring-service/)
