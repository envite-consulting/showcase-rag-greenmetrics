import os

import requests


def main() -> None:
    llm_host = os.getenv("LLM_HOST", "http://ollama:11434").rstrip("/")
    llm_model = os.getenv("OLLAMA_MODEL", "llama3:8b")

    response = requests.post(
        f"{llm_host}/api/pull",
        json={"name": llm_model, "stream": False},
        timeout=900,
    )
    response.raise_for_status()
    print(f"Pulled Ollama model: {llm_model}")


if __name__ == "__main__":
    main()
