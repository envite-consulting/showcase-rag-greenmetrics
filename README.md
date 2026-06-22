# Green Metrics Tool RAG Showcase

This repository contains a containerized Retrieval-Augmented Generation (RAG) system and Green Metrics Tool (GMT) usage scenarios for demonstrating how different RAG configurations can be measured and compared.

The showcase is intentionally small and self-contained. It uses a fixed arXiv document selection and a fixed question set so repeated runs stay comparable.

## Which Guide Should I Use?

| Environment | Recommended path                | Guide                                          |
|-------------|---------------------------------|------------------------------------------------|
| Linux       | Run GMT locally                 | [gmt/README.linux.md](gmt/README.linux.md)     |
| Windows     | Use the free GMT hosted service | [gmt/README.windows.md](gmt/README.windows.md) |
| Live demo   | Prepared dashboard comparison   | [gmt/README.demo.md](gmt/README.demo.md)       |

Windows users should use the hosted GMT service instead of local measurements. Local WSL runs are useful for development, but they can produce limited or inconsistent measurement data depending on host support for metric providers.

## What Gets Measured

The measured RAG system consists of two services:

- `rag-app`: FastAPI application for indexing, retrieval, augmentation, and generation orchestration
- `ollama`: local LLM service used by the RAG app

The standard remote and local scenarios measure these phases:

1. `Prepare Dataset`
2. `Warmup Indexing`
3. `Indexing`
4. `Pull Ollama Model`
5. `Warmup RAG`
6. `RAG Queries`

The `Prepare Dataset` phase downloads the fixed document set inside the measured container before indexing.

The standard remote and local scenarios download their configured Ollama model because they do not have access to the prepared GMT model volume. The three demo scenarios skip the pull step and use models already available in the mounted read-only volume. In those demo scenarios, `OLLAMA_MODEL` must exactly match the complete name and tag of a model in that volume.

The fixed workload is defined by:

- [src/scripts/dataset.json](src/scripts/dataset.json): selected arXiv document IDs
- [src/scripts/questions.json](src/scripts/questions.json): questions used by the load script
- [src/scripts/dataset.demo.json](src/scripts/dataset.demo.json): larger arXiv workload with 1000 explicit document IDs for prepared full-service demo measurements
- [src/scripts/questions.demo.json](src/scripts/questions.demo.json): 50 document-specific single-turn questions for energy-measurement-focused demo runs

## Scenarios

| File                                                                         | Purpose                                                                                                             |
|------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| [gmt/usage_scenario.yml](gmt/usage_scenario.yml)                             | remote scenario for the GMT hosted service; downloads `tinyllama:1.1b` and uses fewer questions and shorter answers |
| [gmt/usage_scenario.local.yml](gmt/usage_scenario.local.yml)                 | local Linux scenario; downloads `llama3:8b`                                                                         |
| [gmt/usage_scenario.demo_baseline.yml](gmt/usage_scenario.demo_baseline.yml) | fuller hosted-service baseline using the preloaded `llama3:8b`, 1000 arXiv documents, and 50 questions              |
| [gmt/usage_scenario.demo_enhanced.yml](gmt/usage_scenario.demo_enhanced.yml) | fuller hosted-service scenario using the preloaded `llama3:8b`, structured retrieval, and BM25 re-ranking           |
| [gmt/usage_scenario.demo_smallLLM.yml](gmt/usage_scenario.demo_smallLLM.yml) | fuller hosted-service scenario using the preloaded `llama3.2:3b` instead of `llama3:8b`                             |

The RAG app defaults are defined in [src/app/config.yaml](src/app/config.yaml). Variables declared in the `gmt/usage_scenario.*.yml` files override these defaults. For local Linux runs, edit [gmt/usage_scenario.local.yml](gmt/usage_scenario.local.yml) before starting the measurement. For hosted runs, keep [gmt/usage_scenario.yml](gmt/usage_scenario.yml) lightweight and adjust variables in the GMT Scenario Runner.

## Prebuilt GMT Image

The GMT compose files use the prebuilt image
`enviteconsulting/showcase-rag-greenmetrics:demo` by default. This keeps dependency
installation, including PyTorch and Sentence Transformers, out of each measurement
setup.

Build and push the image from Linux, macOS, Git Bash, or WSL:

```shell
bash gmt/build-and-push-image.sh
```

Pass a tag as the first argument when a fixed version is required:

```shell
bash gmt/build-and-push-image.sh dev-abc1234
```

The image repository and tag can also be configured through `IMAGE_REPO` and
`IMAGE_TAG`. When changing either value, update the fixed `image` entry in the GMT
compose files to the same published image.

On Windows, run the script in WSL with Docker Desktop's WSL integration enabled.
The `.sh` files use LF line endings through `.gitattributes`.

## Configuration

Base runtime parameters are defined by [src/app/config.yaml](src/app/config.yaml). The GMT scenario files override individual values where needed.

Important variables:

| Variable                       | Meaning                                                              |
|--------------------------------|----------------------------------------------------------------------|
| `CHUNKING_STRATEGY`            | `simple` or `structure`                                              |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | chunk sizing for indexing                                            |
| `EMBEDDING_MODEL`              | Sentence Transformer model                                           |
| `POST_BM25_RERANK`             | enable BM25 re-ranking                                               |
| `TOP_K`                        | number of retrieved text segments used as context                    |
| `OLLAMA_MODEL`                 | model to download, or exact preloaded name and tag in demo scenarios |
| `RAG_QUESTION_LIMIT`           | number of questions in the measured load                             |

## Structure

```text
showcase-rag-greenmetrics
├── README.md                           # overview and guide selection
├── docker-compose.yml                  # local app execution without GMT
├── docker/
│   └── Dockerfile
├── gmt/
│   ├── README.md                       # GMT setup and image publishing
│   ├── README.demo.md                  # prepared dashboard comparison
│   ├── README.linux.md                 # local Linux measurement guide
│   ├── README.windows.md               # hosted-service guide for Windows users
│   ├── build-and-push-image.sh         # publish the prebuilt RAG app image
│   ├── docker-compose.gmt.yml          # default GMT compose file
│   ├── docker-compose.demo.yml         # hosted GPU demo compose file
│   ├── usage_scenario.yml              # lightweight hosted-service scenario
│   ├── usage_scenario.local.yml        # local Linux GMT scenario
│   ├── usage_scenario.demo_baseline.yml
│   ├── usage_scenario.demo_enhanced.yml
│   └── usage_scenario.demo_smallLLM.yml
├── requirements.txt
├── src/
│   ├── app/                            # RAG app
│   ├── scripts/                        # dataset, question, and workload scripts
│   ├── data/raw/                       # downloaded arXiv texts
│   └── data/index/                     # generated Chroma index
├── emb_models/                         # local embedding model cache
├── hf-cache/                           # local Hugging Face cache
└── logs/                               # runtime logs
```

## Sources

- [Green Metrics Tool documentation](https://docs.green-coding.io/)
- [GMT installation on Linux](https://docs.green-coding.io/docs/installation/installation-linux/)
- [Measuring locally with GMT](https://docs.green-coding.io/docs/measuring/measuring-locally/)
- [Measuring with the GMT hosted service](https://docs.green-coding.io/docs/measuring/measuring-service/)
