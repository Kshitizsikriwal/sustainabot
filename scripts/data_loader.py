import fitz # pymupdf
import os

RAW_DATA = "/Users/kshitizsikriwal/Kshitiz/sustainabot/data/raw"
OUTPUT = "/Users/kshitizsikriwal/Kshitiz/sustainabot/data/processed"
os.makedirs(OUTPUT, exist_ok=True)

def pdf_to_text(pdf_path, out_file):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    for file in os.listdir(RAW_DATA):
        if file.endswith(".pdf"):
            pdf_to_text(os.path.join(RAW_DATA, file),
                os.path.join(OUTPUT, file.replace(".pdf", ".txt")))

