import csv
from pathlib import Path

from pypdf import PdfReader


def extract_text(file_path: str, file_name: str) -> str:

    extension = Path(file_name).suffix.lower()

    # -------------------------
    # TXT
    # -------------------------
    if extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()



    # -------------------------
    # PDF
    # -------------------------
    elif extension == ".pdf":

        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    # -------------------------
    # Unsupported file
    # -------------------------
    else:

        raise ValueError(
            "Unsupported file type"
        )
def extract_csv_records(file_path: str) -> list[dict]:

    records = []

    with open(
        file_path,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if not row.get("text"):
                continue

            records.append({
                "text": row["text"],
                "file_format": row.get("file_format"),
                "label": row.get("label")
            })

    return records