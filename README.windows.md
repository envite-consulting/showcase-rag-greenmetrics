# Windows Hosted-Service Guide

Use this guide when running the showcase from Windows.

For Windows users, the recommended path is the free Green Metrics Tool hosted service instead of local GMT measurements. Local Windows or WSL setups are useful for development, but the available metric providers can be limited and the resulting measurements may be less useful for a showcase.

## Why Hosted Service On Windows?

The GMT hosted service runs the measurement on Green Coding infrastructure. This avoids local Windows measurement limitations and gives you reproducible reports on a maintained reference machine.

The hosted service requires:

- this repository to be available on GitHub or another Git hosting service
- the application to be containerized
- a default [usage_scenario.yml](usage_scenario.yml) in the repository

This repository already provides the required Docker setup and default usage scenario.

The hosted service uses the committed [.env.example](.env.example) file as the default environment configuration. A local `.env` file is ignored and is not needed for hosted measurements.

## Remote Default Scenario

The default [usage_scenario.yml](usage_scenario.yml) is optimized for hosted execution:

- `CHUNKING_STRATEGY=simple`
- `CHUNK_SIZE=512`
- `CHUNK_OVERLAP=64`
- `METADATA_FILTER=False`
- `METADATA_ENHANCEMENT=False`
- `POST_BM25_RERANK=False`
- `OLLAMA_MODEL=tinyllama:1.1b`
- `RAG_QUESTION_LIMIT=4`
- `MAX_TOKENS=256`

This keeps the remote run lightweight while still demonstrating the full RAG workflow:

1. `Prepare Dataset`
2. `Warmup Indexing`
3. `Indexing`
4. `Warmup RAG`
5. `RAG Queries`

The dataset preparation step is included in the hosted scenario because the GMT server clones the repository fresh and does not have the local `src/data/raw` cache.

The larger `llama3:8b` default remains available for local Linux runs in [usage_scenario.local.yml](usage_scenario.local.yml). It is not recommended for the hosted service because remote execution may become very slow.

## Run On The Hosted Service

1. Open the GMT hosted service: [https://metrics.green-coding.io/](https://metrics.green-coding.io/)
2. Request a new measurement for this public repository URL.
3. Use the default `usage_scenario.yml` when asked for the scenario file.
4. Keep the LLM configuration lightweight for the first run; the default scenario already selects the small hosted-service setup.
5. Wait for the measurement email or report link.
6. Open the report in the GMT dashboard.

You only need to fork, clone, or push your own repository if you want to measure modified code or custom scenario files.

The hosted report can then be used to show phase-level metrics and demonstrate how GMT evaluates a containerized RAG workload.

## What To Compare

For a quick Windows-friendly showcase, use the hosted report from [usage_scenario.yml](usage_scenario.yml) as the main result.

You can still adjust the RAG configuration in the GMT Scenario Runner. Variables such as `CHUNKING_STRATEGY`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `METADATA_FILTER`, `METADATA_ENHANCEMENT`, `POST_BM25_RERANK`, `RAG_QUESTION_LIMIT`, and `MAX_TOKENS` are suitable for hosted experiments.

Avoid large LLMs such as `llama3:8b` for hosted runs. They may work, but they can be very slow on the shared remote infrastructure. Keep `OLLAMA_MODEL=tinyllama:1.1b` unless you specifically want to test a larger model.

For deeper local comparisons on your own hardware, run the Linux workflow from [README.linux.md](README.linux.md).

## Notes For Development

You can still edit and test the repository on Windows. If you run shell scripts or Docker locally, prefer WSL and keep the repository inside the WSL filesystem. Shell scripts in this repository are configured through [.gitattributes](.gitattributes) to use Unix line endings.

## Sources

- [Measuring with the GMT hosted service](https://docs.green-coding.io/docs/measuring/measuring-service/)
- [Measuring locally with GMT](https://docs.green-coding.io/docs/measuring/measuring-locally/)
