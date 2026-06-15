# Windows Hosted-Service Guide

Use this guide when running the showcase from Windows.

For Windows users, the recommended path is the free Green Metrics Tool hosted service instead of a local GMT measurement. [Local WSL setups](https://docs.green-coding.io/docs/installation/installation-windows/) are useful for development, but the available metric providers are limited.

## Why Use The Hosted Service On Windows?

The GMT hosted service runs the measurement on Green Coding infrastructure. This avoids Windows-specific measurement limitations and provides reproducible reports from a maintained reference machine.

The hosted service requires:

- a public repository, available on GitHub
- the application to be containerized
- a [usage_scenario.yml](usage_scenario.yml) file in the repository

This repository already provides the required Docker setup and usage scenario.

## Remote Default Scenario

The default [usage_scenario.yml](usage_scenario.yml) is optimized for hosted execution by using a small LLM: `OLLAMA_MODEL=tinyllama:1.1b`. The free version of the GMT hosted service provides a simple machine without specialized hardware such as GPUs or TPUs.

This keeps the remote run lightweight while still demonstrating the full RAG workflow:

1. `Prepare Dataset`
2. `Warmup Indexing`
3. `Indexing`
4. `Warmup RAG`
5. `RAG Queries`

The dataset preparation step is part of the hosted scenario because the GMT server clones the repository fresh for each execution. As a result, the dataset must be downloaded during every hosted run.

## Run On The Hosted Service

Open the GMT hosted service: [ScenarioRunner - Submit Software](https://metrics.green-coding.io/request.html). This page lets you submit software for measurement.

1. Enter a measurement name and your email address.
2. Use this repository URL for the measurement.
3. Use the default `usage_scenario.yml` as the scenario file.
4. Select `CO2 Profiling (DVFS ON, TB ON, HT ON) Esprimo P956` as the hardware.
5. Select `One-Off [Free - Fair use]` as the measurement interval.
6. Start the measurement by clicking _Submit software_.
7. Wait for the measurement email.
8. Open the report in the GMT dashboard.

The hosted report can be used to show phase-level metrics and demonstrate how GMT evaluates a containerized RAG workload.

Keep in mind that the free version of the hosted service has certain [limitations and restrictions](https://www.green-coding.io/products/green-metrics-tool/).

## What To Compare

Use the hosted report from [usage_scenario.yml](usage_scenario.yml) as the baseline result.

You can adjust the RAG configuration in the GMT Scenario Runner. Variables such as `CHUNKING_STRATEGY`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `METADATA_FILTER`, `METADATA_ENHANCEMENT`, `POST_BM25_RERANK`, `RAG_QUESTION_LIMIT`, and `MAX_TOKENS` are suitable for hosted experiments.

Avoid large LLMs such as `llama3:8b` for hosted runs and keep `OLLAMA_MODEL=tinyllama:1.1b`.

For deeper local comparisons on your own hardware, run the Linux workflow from [README.linux.md](README.linux.md).

## Sources

- [Measuring with the GMT hosted service](https://docs.green-coding.io/docs/measuring/measuring-service/)
- [Measuring locally with GMT](https://docs.green-coding.io/docs/measuring/measuring-locally/)
