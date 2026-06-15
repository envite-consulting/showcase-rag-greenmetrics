import requests

from app.config import load_config


def main() -> None:
    cfg = load_config()
    response = requests.post(
        f"{cfg.llm_host.rstrip('/')}/api/pull",
        json={"name": cfg.llm_model, "stream": False},
        timeout=900,
    )
    response.raise_for_status()
    print(f"Pulled Ollama model: {cfg.llm_model}")


if __name__ == "__main__":
    main()
