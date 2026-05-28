import fitz
import re


def extract_text_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    full_text = ""

    for page in document:

        text = page.get_text()

        full_text += text + "\n"

    document.close()

    full_text = clean_text(full_text)

    return full_text


def clean_text(text):

    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)

    # Remove html / print junk
    text = re.sub(r"html\S*", "", text)
    text = re.sub(r"print\s*\d+/\d+", "", text)

    # Remove timestamps
    text = re.sub(
        r"\d{1,2}/\d{1,2}/\d{2,4},?\s*\d{1,2}:\d{2}\s*(AM|PM)?",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove page indicators
    text = re.sub(r"\b\d+/\d+\b", "", text)

    # Remove strange symbols
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def split_into_chunks(text, chunk_size=120):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i + chunk_size])

        chunks.append(chunk)

    return chunks