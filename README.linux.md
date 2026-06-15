# Linux Local Measurement Guide

Use this guide when running the showcase on a Linux machine with a local Green Metrics Tool installation and an NVIDIA GPU.

For installing and configuring GMT itself, follow the official [Installation on Linux](https://docs.green-coding.io/docs/installation/installation-linux/) guide. This README assumes that GMT is already installed, Docker works with GMT, the relevant GMT metric providers are configured, and the local GMT services can be started successfully.

Local Linux measurements are intended for systems where the RAG workload can use an NVIDIA GPU and GMT can measure it through NVML. Without GPU measurements, local runs can still be useful for development checks, but they are less meaningful for comparing LLM-heavy RAG configurations. In that case, prefer the hosted-service workflow in [README.windows.md](README.windows.md).

For this showcase, the relevant GMT metric providers are:

- [NVIDIA NVML for GPU energy](https://docs.green-coding.io/docs/measuring/metric-providers/gpu-energy-nvidia-nvml-component/)
- [RAPL for CPU package energy](https://docs.green-coding.io/docs/measuring/metric-providers/cpu-energy-rapl-msr-component/)
- [RAPL for memory/RAM energy](https://docs.green-coding.io/docs/measuring/metric-providers/memory-energy-rapl-msr-component/)

## Clone The Repository

```shell
cd ~/projects
git clone <repository-url> showcase-rag-greenmetrics
cd showcase-rag-greenmetrics
```

The RAG app provides defaults in [src/app/config.yaml](src/app/config.yaml). For local GMT experiments, edit the `environment` values in [usage_scenario.local.yml](usage_scenario.local.yml).

## Optional App Check

Before starting a GMT measurement, you can run the RAG app once to check that Docker, Ollama, indexing, and the API work together.

```shell
cd /path/to/showcase-rag-greenmetrics
docker compose --profile app up --build
```

In a second terminal:

```shell
docker exec showcase-ollama ollama pull llama3:8b
docker exec showcase-rag-app python scripts/get_dataset.py --force
docker exec showcase-rag-app python -m app.indexing
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d "{\"q_id\":\"manual-001\",\"question\":\"What is the nature of gravity in string theory at high energies?\"}"
```

Stop the app afterwards:

```shell
docker compose --profile app down
```

## Measure With Local GMT

Start the local GMT services as described in the official GMT installation guide. Then run the local showcase scenario from the GMT installation directory:

```shell
cd /path/to/green-metrics-tool
python3 runner.py --uri /path/to/showcase-rag-greenmetrics --filename usage_scenario.local.yml --name rag-local --allow-unsafe
```

The report appears in the local GMT dashboard (default: http://metrics.green-coding.internal:9142). Use the dashboard to inspect the run or compare several runs.

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

## Sources

- [GMT Installation on Linux](https://docs.green-coding.io/docs/installation/installation-linux/)
- [Measuring locally with GMT](https://docs.green-coding.io/docs/measuring/measuring-locally/)
