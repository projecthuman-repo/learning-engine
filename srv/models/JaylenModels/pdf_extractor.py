
"""
author: Jaylen Edwards
Extracts the contents of a pdf using either optical character recognition (ocr) or a normal read.
"""

from pdf2image import convert_from_path
from pypdf import PdfReader, PdfWriter
import pytesseract as tess
import constants
import os
import re


class Extractor:
    """
    This module provides a class Extractor for extracting the text contents from a PDF file. It uses either optical
    character recognition (OCR) or a normal read.

    Dependencies:
    - pdf2image
    - pypdf
    - pytesseract
    - constants (custom module)

    Functions:
    - init(self, document_path="", password=""): Constructor method. Initializes an instance of Extractor with optional
    document_path and password parameters.
    - ocr_read(self, path): Private method. Used on PDFs with no searchable text. Extracts text using OCR and saves as
    images.
    - plain_text_read(self): Private method. Extracts the text from a document with searchable text.
    - change_document(self, document_path="", password=""): Public method. Changes which document to extract text from.
    - to_txt(self): Public method. Creates a txt file of the extracted text.
    - get_text(self): Public method. Returns the extracted text.
    - filter(self): Private method. Used to remove unnecessary bits from academic papers.

    Attributes:
    - document_path: The file path to the PDF document.
    - password: The password for the PDF document, if it is password-protected.
    - text: The extracted text from the PDF document.
    - document: The PDF document itself.
    - reader: A PdfReader object for the PDF document.
    - document_name: The name of the PDF document.
    """
    def __init__(self, document_path="", password=""):
        # the below line of text is required as we need tesseract.exe installed to use the library.
        # change it to whatever local path you are using
        tess.pytesseract.tesseract_cmd = constants.TESS_PATH
        self.text = None
        self.document = None
        self.reader = None
        self.document_name = None
        self.password = None
        if document_path != "":  # if an argument is provided in the constructor
            self.change_document(document_path, password)

    # used on pdfs with no searchable text
    def ocr_read(self, path):
        images = convert_from_path(path, poppler_path=constants.POPPLER_PATH)
        for i in range(len(images)):
            # Save pages as images of the pdf. only way optical character recognition will work
            images[i].save('page' + str(i) + '.png', 'PNG')
            # append the extracted text to the rest of the text
            self.text = self.text + tess.image_to_string("page"+str(i)+".png") + "\n"
            # delete the generated image file.
            os.remove("page"+str(i)+".png")

    # extracts the text from a document with searchable text
    def plain_text_read(self):
        number_of_pages = len(self.reader.pages)
        for i in range(0, number_of_pages):
            page = self.reader.pages[i]
            self.text = self.text + page.extract_text() + "\n"  # add a page to the text with a new line separating

    # change which document we want extracted
    def change_document(self, document_path="", password=""):
        self.text = ""
        self.document = document_path
        self.reader = PdfReader(document_path)
        self.password = password

        # if a pdf is password protected, decrypt it with the passowrd
        if self.reader.is_encrypted:
            self.reader.decrypt(password)

        # check the document metadata for a title, if one does not exist use the name from the document path
        # this name is used for the outputted .txt file

        if self.reader.metadata.title is not None:
            self.document_name = self.reader.metadata.title
        else:
            self.document_name = document_path.split(".pdf")[0]

        # check to see if there is readable text in the pdf, if not
        if self.reader.pages[0].extract_text() == '' or None:
            self.ocr_read(document_path)
        else:
            self.plain_text_read()

    # creates a txt file of the pdf
    def to_txt(self):
        if self.text != "" or None:
            if self.document_name is not None:
                pdf_to_txt = open(self.document_name + "_txt.txt", "w+", encoding="utf-8")
            else:
                pdf_to_txt = open(constants.DEFAULT_SAVE_PATH, "w+", encoding="utf-8")
            pdf_to_txt.write(self.text)
            pdf_to_txt.close()

    # return the extracted text
    def get_text(self):
        if self.text != "" or None:
            self.filter()
            return self.text

    # used to remove unnecessary bits from academic papers
    # will remove everything before the introduction and everything after the references
    # will also remove everything before the abstract
    def filter(self):
        if self.text != "" or None:
            introduction_split = re.split("introduction", self.text, flags=re.IGNORECASE)
            if len(introduction_split) > 1:  # split before an introduction if it exists
                self.text = introduction_split[1]
            references_split = re.split("references", self.text, flags=re.IGNORECASE)
            if len(references_split) > 1:
                self.text = references_split[0]
