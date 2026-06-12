# Linux Local Measurement Guide

Use this guide when running the showcase on a Linux machine with a local Green Metrics Tool installation.

Local Linux measurements are the best option if you want to compare several RAG configurations on the same host and inspect the results in your own GMT dashboard.

## Prerequisites

- local Green Metrics Tool installation
- Python 3, `python3-venv`, `pip`, `git`, `curl`, `make`, `gcc`, `iproute2`
- Docker Engine including Buildx and the Compose plugin
- a running Docker daemon
- Docker access for the current user, typically through the `docker` group, so GMT does not need to run as root
- running GMT Docker services from the `docker/` folder of the GMT installation
- available metric providers on the host, for example RAPL for CPU/RAM and optionally NVIDIA/NVML for GPU measurements

A machine without a dedicated GPU can still run the showcase. GPU metrics are simply not available and local LLM generation may be slower.

## Clone The Repository

```shell
cd ~/projects
git clone <repository-url> showcase-rag-greenmetrics
cd showcase-rag-greenmetrics
```

The committed default configuration lives in [.env.example](.env.example). The Compose files use this file directly so the showcase and the hosted service work without extra setup. For local experiments, edit the `environment` values in [usage_scenario.local.yml](usage_scenario.local.yml); a private `.env` file is ignored by Git, but it is not loaded by default.

## Prepare The Workload

Download the fixed document set once before running comparisons. This keeps network transfer out of the measured workflow.

```shell
cd /path/to/showcase-rag-greenmetrics
docker compose --profile app up --build -d
docker exec showcase-rag-app python scripts/get_dataset.py --force
docker compose --profile app down
```

## Optional App Smoke Test

This step is useful before starting GMT measurements.

```shell
cd /path/to/showcase-rag-greenmetrics
docker compose --profile app up --build
```

In a second terminal:

```shell
docker exec showcase-rag-app python -m app.indexing
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"q_id\":\"manual-001\",\"question\":\"What is the nature of gravity in string theory at high energies?\"}"
```

Stop the app afterwards:

```shell
docker compose --profile app down
```

## Measure With Local GMT

Start the local GMT services:

```shell
cd /path/to/green-metrics-tool/docker
docker compose up -d
```

Make sure the workload has been downloaded:

```shell
cd /path/to/showcase-rag-greenmetrics
docker compose --profile app up --build -d
docker exec showcase-rag-app python scripts/get_dataset.py --force
docker compose --profile app down
```

Run the local scenario:

```shell
cd /path/to/green-metrics-tool
python3 runner.py --uri /path/to/showcase-rag-greenmetrics --filename usage_scenario.local.yml --name rag-local --allow-unsafe
```

The report appears in the local GMT dashboard. Use the dashboard to inspect the run or compare several runs.

## Change RAG Configuration Locally

Edit the `environment` values in [usage_scenario.local.yml](usage_scenario.local.yml) before starting a measurement. Useful variables include:

| Variable | Example values |
| --- | --- |
| `CHUNKING_STRATEGY` | `simple`, `structure` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | `512` / `64`, `256` / `32` |
| `METADATA_FILTER` | `True`, `False` |
| `METADATA_ENHANCEMENT` | `True`, `False` |
| `POST_BM25_RERANK` | `True`, `False` |
| `OLLAMA_MODEL` | `llama3:8b`, `tinyllama:1.1b` |
| `RAG_QUESTION_LIMIT` | `4`, `8`, `12` |
| `MAX_TOKENS` | `256`, `512` |

When changing `OLLAMA_MODEL`, set it for both `rag-app` and `ollama` in the scenario file.
