import os
import json
import re

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(PROCESSED_DIR, "chunks.json")

# ------------------------------------------------------------------
# Chunking helpers
# ------------------------------------------------------------------

def clean_heading(text):
    return text.lstrip("#").strip()


def extract_h1(md):
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0][2:], "\n".join(lines[1:])
    return None, md


def extract_front_matter(md):
    match = re.search(r"\n##\s+", md)
    if match:
        return md[:match.start()], md[match.start():]
    return "", md


def make_chunk(text, source, section):
    return {
        "text": text.strip(),
        "metadata": {
            "source_file": source,
            "section": section
        }
    }


def chunk_markdown(md, source):
    chunks = []

    title, md = extract_h1(md)
    if title:
        chunks.append(make_chunk(title, source, "Document Title"))

    meta, md = extract_front_matter(md)
    if meta.strip():
        chunks.append(make_chunk(meta, source, "Document Metadata"))

    sections = re.split(r"\n##\s+", md)

    for sec in sections:
        if not sec.strip():
            continue

        header, *body = sec.split("\n", 1)
        header = clean_heading(header)
        body = body[0] if body else ""

        chunks.append(
            make_chunk(f"## {header}\n{body}", source, header)
        )

    return chunks

# ------------------------------------------------------------------
# Main ingestion
# ------------------------------------------------------------------

def run_ingestion():
    all_chunks = []

    if not os.path.exists(RAW_DATA_DIR):
        raise FileNotFoundError(f"RAW_DATA_DIR not found: {RAW_DATA_DIR}")

    for filename in sorted(os.listdir(RAW_DATA_DIR)):
        if not filename.endswith(".md"):
            continue

        path = os.path.join(RAW_DATA_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            md_text = f.read().strip()

        if not md_text:
            print(f"⚠️ Skipping empty file: {filename}")
            continue

        chunks = chunk_markdown(md_text, filename)
        all_chunks.extend(chunks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print("✅ Ingestion complete")
    print(f"Files read     : {len(set(c['metadata']['source_file'] for c in all_chunks))}")
    print(f"Total chunks   : {len(all_chunks)}")
    print(f"Output written : {OUTPUT_FILE}")

# ------------------------------------------------------------------

if __name__ == "__main__":
    run_ingestion()
