import io
from pathlib import Path

import streamlit as st
from pypdf import PdfReader
from docx import Document


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI OEM Manuals Assistant",
    page_icon="⚓",
    layout="wide",
)


# ---------------------------------------------------------
# DOCUMENT EXTRACTION FUNCTIONS
# ---------------------------------------------------------

def extract_pdf(file):
    """Extract text from each page of a PDF file."""
    results = []

    reader = PdfReader(file)

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            results.append(
                {
                    "text": text,
                    "filename": file.name,
                    "page": page_number,
                }
            )

    return results


def extract_docx(file):
    """Extract text from a DOCX file."""
    file_bytes = file.read()
    document = Document(io.BytesIO(file_bytes))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    combined_text = "\n".join(paragraphs)

    return [
        {
            "text": combined_text,
            "filename": file.name,
            "page": None,
        }
    ]


def extract_txt(file):
    """Extract text from a TXT file."""
    file_bytes = file.read()
    text = file_bytes.decode("utf-8", errors="ignore")

    return [
        {
            "text": text,
            "filename": file.name,
            "page": None,
        }
    ]


def extract_md(file):
    """Extract text from a Markdown file."""
    file_bytes = file.read()
    text = file_bytes.decode("utf-8", errors="ignore")

    return [
        {
            "text": text,
            "filename": file.name,
            "page": None,
        }
    ]


def extract_document(file):
    """Route a file to the correct extraction function."""
    extension = Path(file.name).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file)

    if extension == ".docx":
        return extract_docx(file)

    if extension == ".txt":
        return extract_txt(file)

    if extension == ".md":
        return extract_md(file)

    return []


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "documents" not in st.session_state:
    st.session_state.documents = []


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("⚓ AI OEM Manuals Assistant")

st.write(
    "Upload OEM technical manuals and prepare them for "
    "AI-powered document-based question answering."
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.header("📚 Documents")

    uploaded_files = st.file_uploader(
        "Upload OEM Manuals",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
    )


# ---------------------------------------------------------
# PROCESS UPLOADED DOCUMENTS
# ---------------------------------------------------------

if uploaded_files:
    existing_filenames = {
        document["filename"]
        for document in st.session_state.documents
    }

    new_files = [
        file
        for file in uploaded_files
        if file.name not in existing_filenames
    ]

    if new_files:
        with st.spinner("Extracting documents..."):
            for file in new_files:
                try:
                    extracted = extract_document(file)

                    if extracted:
                        st.session_state.documents.extend(extracted)
                    else:
                        st.warning(
                            f"No text could be extracted from {file.name}"
                        )

                except Exception as error:
                    st.error(
                        f"Could not process {file.name}: {error}"
                    )

        st.success(
            f"Processed {len(new_files)} new document(s)."
        )


# ---------------------------------------------------------
# DOCUMENT SUMMARY
# ---------------------------------------------------------

if st.session_state.documents:
    st.subheader("📄 Document Summary")

    summary = {}

    for item in st.session_state.documents:
        filename = item["filename"]

        if filename not in summary:
            summary[filename] = {
                "filename": filename,
                "type": Path(filename).suffix.upper().replace(".", ""),
                "pages": set(),
                "characters": 0,
            }

        if item["page"] is not None:
            summary[filename]["pages"].add(item["page"])

        summary[filename]["characters"] += len(item["text"])

    summary_rows = []

    for item in summary.values():
        pages = item["pages"]

        page_count = len(pages) if pages else "N/A"

        summary_rows.append(
            {
                "Filename": item["filename"],
                "Type": item["type"],
                "Pages": page_count,
                "Characters": item["characters"],
            }
        )

    st.dataframe(
        summary_rows,
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        f"Loaded {len(summary)} document(s) successfully."
    )

else:
    st.info(
        "No documents uploaded yet. "
        "Upload a PDF, DOCX, TXT, or MD manual from the sidebar."
    )
