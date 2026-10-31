from io import BytesIO
from pypdf import PdfReader
from docx import Document

def extract_text(uploaded_file) -> str:
    """Extract text from a Streamlit UploadedFile (PDF, DOCX or TXT)."""
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        reader = PdfReader(BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".docx"):
        doc = Document(BytesIO(raw))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                paragraphs.append(" | ".join(cell.text for cell in row.cells))
        return "\n".join(paragraphs)

    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")

    raise ValueError("Unsupported file type. Upload PDF, DOCX or TXT.")
