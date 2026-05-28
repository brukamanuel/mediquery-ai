import os
from sklearn.feature_extraction.text import TfidfVectorizer
from src.pdf_loader import extract_text_from_pdf, split_into_chunks


pdf_folder = "data/medical_pdfs"

all_chunks = []
chunk_sources = []

for file in os.listdir(pdf_folder):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(pdf_folder, file)

        text = extract_text_from_pdf(pdf_path)

        chunks = split_into_chunks(text)

        for chunk in chunks:
         all_chunks.append(chunk)
         chunk_sources.append(file)


vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_df=0.85,
    min_df=1
)

tfidf_matrix = vectorizer.fit_transform(all_chunks)

# print("Total chunks:", len(all_chunks))

# print("Matrix shape:", tfidf_matrix.shape)