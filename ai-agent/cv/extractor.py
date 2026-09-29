import io
import pdfplumber
import docx


def extract_cv_text(filename: str, content: bytes) -> str:
    """Extrait le texte d'un CV (PDF, DOCX ou TXT) à partir de ses octets."""
    ext = filename.lower().rsplit(".", 1)[-1]
    if ext == "pdf":
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    if ext in ("docx", "doc"):
        d = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in d.paragraphs)
    if ext == "txt":
        return content.decode("utf-8", errors="ignore")
    raise ValueError(f"Format non supporté : {ext}")
