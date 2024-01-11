# Extract text from different document types
import io
import filetype
import fitz
import docx


def extract_text_from_document(document):
    # Extract text from different document types
    # Returns None if the document type is not supported
    
    mime_type = filetype.guess_mime(document)

    if mime_type == 'text/plain':
        return document.decode('utf-8')
    elif mime_type == 'application/pdf':
        return extract_text_from_pdf(document)
    elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return extract_text_from_doc(document)
    
    return None


def extract_text_from_pdf(document):
    file = fitz.open(stream=document, filetype='pdf')
    return ''.join(page.get_text() for page in file)


def extract_text_from_doc(document):
    file_io = io.BytesIO(document)
    file = docx.Document(file_io)
    return '\n'.join(para.text for para in file.paragraphs)