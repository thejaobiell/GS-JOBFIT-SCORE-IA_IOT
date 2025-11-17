from typing import Tuple
import io
import PyPDF2


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extrai texto de um PDF recebido como bytes."""
    with io.BytesIO(pdf_bytes) as bio:
        reader = PyPDF2.PdfReader(bio)
        text = []
        for page in reader.pages:
            try:
                text.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(text).strip()
