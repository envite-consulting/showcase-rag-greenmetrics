# Green Metrics Tool Setup

This directory contains everything specific to Green Metrics Tool (GMT)
measurements:

- `usage_scenario*.yml`: lightweight, local, and prepared demo workloads
- `docker-compose.gmt.yml`: standard GMT service definition
- `docker-compose.demo.yml`: GPU demo definition with the prepared Ollama volume
- `build-and-push-dev-image.sh`: builds and publishes the RAG app image used by GMT
- environment-specific and demo guides

The general local development setup remains in the repository root and continues to
build from `docker/Dockerfile`.

## Publish The RAG App Image

From Linux, macOS, Git Bash, or WSL:

```shell
docker login
bash gmt/build-and-push-image.sh
```

The defaults are:

```text
IMAGE_REPO=enviteconsulting/showcase-rag-greenmetrics
IMAGE_TAG=demo
DOCKER_PLATFORM=linux/amd64
```

All values can be overridden. An explicit first argument takes precedence over
`IMAGE_TAG`:

```shell
IMAGE_REPO=registry.example.com/team/showcase-rag-greenmetrics \
DOCKER_PLATFORM=linux/amd64 \
  bash gmt/build-and-push-image.sh dev-abc1234
```

The GMT compose files use
`enviteconsulting/showcase-rag-greenmetrics:demo` unless `RAG_APP_IMAGE` is set.
For comparable measurements, prefer a fixed tag or image digest rather than
overwriting `demo`. Images used by the hosted GMT service must be publicly pullable
unless the service has matching registry credentials.

## Guides

- [Linux local measurement](README.linux.md)
- [Windows and hosted service](README.windows.md)
- [Prepared demo comparison](README.demo.md)
