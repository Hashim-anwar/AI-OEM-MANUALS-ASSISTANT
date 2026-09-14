# ⚓ AI OEM Manuals Assistant

A Streamlit application for asking questions about technical OEM manuals. Users can upload PDF, DOCX, TXT and Markdown files, or load supported public/shared Google Drive files and folders.

The application extracts the documents, creates overlapping text chunks, generates Sentence Transformer embeddings, indexes them with FAISS, combines semantic and keyword retrieval, and sends only the retrieved manual context to Groq's `openai/gpt-oss-120b` model.

## 1. Features

- Multiple local manual uploads
- PDF page-level extraction
- DOCX, TXT and Markdown extraction
- Simple overlapping chunking
- Sentence Transformer embeddings
- FAISS cosine-similarity search
- Simple keyword search
- Hybrid retrieval: 70% semantic + 30% keyword
- Groq `openai/gpt-oss-120b`
- Answers grounded only in retrieved manual evidence
- Explicit "not enough information" behavior
- Source filename and PDF page display
- Google Drive public/shared file or folder loading
- Session-state persistence
- Cached embedding model
- No re-embedding when asking follow-up questions
- Duplicate document protection using file hashes

## 2. Local Installation

Install the packages:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## 3. Groq API Key

For local development, create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

Never put the real API key inside `app.py`.

Do not commit `secrets.toml` to GitHub.

## 4. Google Drive Setup

The app supports supported files that are publicly accessible through Google Drive. The simplest setup is a Google Drive API key.

### A. Create a Google Cloud project

1. Open Google Cloud Console.
2. Create or select a project.
3. Open **APIs & Services → Library**.
4. Search for **Google Drive API**.
5. Enable the Google Drive API.

### B. Create an API key

1. Open **APIs & Services → Credentials**.
2. Select **Create Credentials → API key**.
3. Copy the API key.
4. For better security, restrict the key to the Google Drive API where practical.

### C. Add the key to Streamlit secrets

Add this to `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your-groq-api-key"
GOOGLE_DRIVE_API_KEY = "your-google-drive-api-key"
```

### D. Share the Drive file or folder

The file or folder must be accessible to the application through its Google Drive permissions.

For the easiest public demo:

1. Right-click the file/folder in Google Drive.
2. Select **Share**.
3. Change General access to **Anyone with the link**.
4. Give Viewer access.
5. Copy the Google Drive link.
6. Paste it into the application's Google Drive field.

Only these file types are downloaded:

- `.pdf`
- `.docx`
- `.txt`
- `.md`

Folder links are searched recursively for supported files.

### Important Google Drive limitation

This demo uses an API key for public/shared Drive content. It is not a private Google Drive OAuth application.

If a file belongs to a private Drive and is not publicly accessible, an API key alone is not enough. A production/private implementation should use OAuth or a service account with the required sharing permissions.

## 5. Streamlit Cloud Deployment

### Step 1: Create a GitHub repository

Create a new GitHub repository, for example:

```text
ai-oem-manuals-assistant
```

Upload:

```text
app.py
requirements.txt
README.md
```

Do NOT upload:

```text
.streamlit/secrets.toml
```

Do not upload your API keys.

### Step 2: Open Streamlit Community Cloud

Sign in to Streamlit Community Cloud and create a new app.

Select:

- Your GitHub repository
- Branch: usually `main`
- Main file: `app.py`

Deploy the app.

### Step 3: Add Streamlit secrets

After deployment, open the application's settings/secrets area and add:

```toml
GROQ_API_KEY = "your-groq-api-key"
GOOGLE_DRIVE_API_KEY = "your-google-drive-api-key"
```

Save the secrets and restart/redeploy the application if required.

## 6. How the Pipeline Works

```text
OEM Manual
    ↓
PDF / DOCX / TXT / MD Extraction
    ↓
Text Chunks
    ↓
Sentence Transformer Embeddings
    ↓
FAISS Semantic Search
    +
Keyword Search
    ↓
Hybrid Ranking
70% Semantic + 30% Keyword
    ↓
Top Retrieved Manual Evidence
    ↓
Groq openai/gpt-oss-120b
    ↓
Answer + Sources
```

The important design principle is that the LLM receives the retrieved manual evidence as context and is instructed not to use outside knowledge.

## 7. Performance and State

The app uses `st.session_state` for:

- indexed chunks
- embeddings inside the FAISS index
- processed document hashes
- FAISS index
- chat history

The Sentence Transformer model uses `@st.cache_resource`, so the model is loaded once and reused.

When a new document is added, only the new document is extracted, chunked and embedded. Its embeddings are added to the existing FAISS index.

Asking another question does not re-embed the existing manuals. Only the question itself is embedded for semantic search.

## 8. Testing Checklist

After deployment, test:

1. Start the app with no documents.
2. Upload a PDF.
3. Upload a DOCX.
4. Upload a TXT file.
5. Upload a Markdown file.
6. Confirm the indexed chunk count increases.
7. Ask a question whose answer is clearly in the manual.
8. Confirm the answer appears with Sources.
9. Confirm PDF sources show page numbers.
10. Ask a question that is not covered by the manual.
11. Confirm the assistant says the manuals do not contain enough information rather than guessing.
12. Ask two or more questions and confirm documents are not reprocessed.
13. Test a public/shared Google Drive file.
14. Test a public/shared Google Drive folder.
