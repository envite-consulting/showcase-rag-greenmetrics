import json
import sys
import os
from tqdm import tqdm
from urllib.request import Request, urlopen

JSON_PATH = os.getenv("RAG_QUESTIONS_PATH", "/src/scripts/questions.json")
API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000/ask")
PRINT = os.getenv("RAG_PRINT_RESPONSES", "0") == "1"
LIMIT = int(os.getenv("RAG_QUESTION_LIMIT", "8") or "8")


def post_question(question: str, q_id: str) -> str:
    data = json.dumps({"q_id": q_id, "question": question}).encode("utf-8")
    req = Request(
        API_URL,
        data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=120) as response:
        return response.read().decode("utf-8", errors="replace")


def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    if LIMIT > 0:
        items = items[:LIMIT]

    with tqdm(total=len(items)) as pbar:
        for item in items:
            question = item.get("question")
            q_id = item.get("q_id")
            pbar.set_description(f"Processing question #{q_id}")
            if not question:
                continue
            output = post_question(question, q_id)
            if PRINT:
                print(f"{output}\n")
            pbar.update(1)


if __name__ == "__main__":
    main()
