import os
import json
import logging
from pathlib import Path
from pypdf import PdfReader

logging.basicConfig(level=logging.INFO, format="[INTAKE]: %(message)s")


def analyze_pdfs(staging_dir: Path):
    results = []
    pdf_files = list(staging_dir.glob("**/*.pdf"))

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            text_preview = ""
            if len(reader.pages) > 0:
                text_preview = reader.pages[0].extract_text()[:1000]

            results.append(
                {"file": pdf_path.name, "pages": len(reader.pages), "preview": text_preview}
            )
            logging.info(f"Analyzed {pdf_path.name}")
        except Exception as e:
            logging.error(f"Failed to analyze {pdf_path.name}: {e}")

    return results


def analyze_json(staging_dir: Path):
    json_path = staging_dir / "wikoda_basis_database_export.json"
    if json_path.exists():
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            return {"file": json_path.name, "entries": len(data), "type": "database_export"}
        except Exception as e:
            logging.error(f"Failed to analyze JSON: {e}")
    return None


if __name__ == "__main__":
    staging_path = Path("data/offerings/staging")
    pdf_results = analyze_pdfs(staging_path)
    json_results = analyze_json(staging_path)

    summary = {"pdfs": pdf_results, "json": json_results}

    with open("data/offerings/summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    logging.info("Analysis complete. Summary saved to data/offerings/summary.json")
