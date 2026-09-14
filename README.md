# AI OEM Manuals Assistant

A simple Streamlit application for uploading OEM technical manuals and extracting their text. The project will be expanded step by step into a document-grounded AI assistant using embeddings, FAISS hybrid retrieval, and Groq.

## Step 1: Current Features

- Upload multiple PDF, DOCX, TXT, and MD files.
- Extract PDF text page by page.
- Extract DOCX, TXT, and Markdown text.
- Preserve filename and PDF page number as metadata.
- Display a document summary with file type, page count, and character count.
- Avoid processing the same filename repeatedly during the current Streamlit session.

## Setup

Create a virtual environment if desired, then install the requirements:

```bash
pip install -r requirements.txt
```

Create the Streamlit secrets file:

```text
.streamlit/secrets.toml
```

Add your Groq API key:

```toml
GROQ_API_KEY = "your-key-here"
```

The current Step 1 code does not call Groq yet, but the secret is prepared for later steps.

## Run

```bash
streamlit run app.py
```

## Project Files

```text
AI-OEM-Manuals-Assistant/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

Do not commit your real `secrets.toml` to GitHub.

## Planned Pipeline

The application will be developed in stages:

1. Document extraction
2. Text chunking
3. Sentence Transformer embeddings
4. FAISS semantic search
5. Keyword search
6. Hybrid retrieval
7. Groq LLM answering
8. Source/evidence display
9. Google Drive document loading
10. Session-state and performance optimization

The final assistant will answer questions only from retrieved OEM manual evidence and will explicitly say when the documents do not contain the requested information.
