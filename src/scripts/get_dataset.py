import json
import argparse
from tqdm import tqdm
from pathlib import Path
from datasets import load_dataset

DATASET_SELECTION_PATH = "/src/scripts/dataset.json"
DEFAULT_OUT_DIR = "/src/data/raw"


def parse_args():
    parser = argparse.ArgumentParser(description="Download a small, fixed arXiv subset for the showcase.")
    parser.add_argument("--selection", default=DATASET_SELECTION_PATH)
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    parser.add_argument("--force", action="store_true", help="Replace existing arXiv text files.")
    return parser.parse_args()


def main():
    args = parse_args()
    selection_path = Path(args.selection)
    if not selection_path.exists():
        fallback = Path("scripts/dataset.json")
        selection_path = fallback if fallback.exists() else selection_path

    dataset_selection = json.loads(selection_path.read_text(encoding="utf-8"))

    dataset = dataset_selection["dataset"]
    split = dataset_selection["split"]
    revision = dataset_selection["revision"]
    ids = set(dataset_selection["ids"])
    total_ids = len(ids)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    existing = list(out_dir.glob("arxiv_*.txt"))
    if existing and not args.force:
        print(f"{len(existing)} arXiv documents already exist in {out_dir}. Use --force to replace them.")
        return

    for p in existing:
        p.unlink()

    ds = load_dataset(dataset, split=split, streaming=True, revision=revision)

    found = 0
    missing = set(ids)

    with tqdm(total=total_ids) as pbar:
        pbar.set_description(f"Saving dataset {dataset}")
        for row in ds:
            doc_id = row.get("id")
            if doc_id not in missing:
                continue

            text = row.get("text", "")
            file_name = out_dir / f"arxiv_{doc_id}.txt"
            file_name.write_text(text, encoding="utf-8", errors="ignore")

            missing.remove(doc_id)
            found += 1

            if not missing:
                break
            pbar.update(1)

    if missing:
        raise RuntimeError(
            f"{len(missing)}/{total_ids} documents could not be loaded."
        )

    print(f"{found}/{total_ids} documents saved successfully.\n========== DATASET DOWNLOAD DONE ==========")


if __name__ == "__main__":
    main()
