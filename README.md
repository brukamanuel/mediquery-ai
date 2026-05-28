# MediQuery AI

MediQuery AI is a medical document question-answering system built with Python, Streamlit, TF-IDF vectorization, and cosine similarity.

## Project Description

The system allows users to upload medical PDF documents and ask natural language questions. It retrieves relevant passages from the uploaded documents and generates short answers based only on the document content.

## Features

- Medical PDF text extraction
- Text chunking
- TF-IDF vectorization
- Cosine similarity search
- Synonym expansion
- Multi-passage answer generation
- Source document tracking
- Match score display
- Streamlit web interface
- Document upload support

## Technologies Used

- Python
- Streamlit
- PyMuPDF
- Scikit-learn
- TF-IDF
- Cosine Similarity

## How to Run

Install dependencies:

```bash
python3 -m pip install pymupdf scikit-learn nltk streamlit