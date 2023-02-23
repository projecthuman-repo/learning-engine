"""

Extracts the contents of a pdf using either optical character recognition (ocr) or a normal read.
"""

from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract as tess
import constants
import os
import re


class Extractor:
    def __init__(self, document_path=""):
        # the below line of text is required as we need tesseract.exe installed to use the library.
        # change it to whatever local path you are using
        tess.pytesseract.tesseract_cmd = constants.TESS_PATH
        self.text = None
        self.document = None
        self.reader = None
        self.document_name = None
        if document_path != "":  # if an argument is provided in the constructor
            self.change_document(document_path)

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
            self.text = self.text + page.extract_text() + "\n"

    # change which document we want extracted
    def change_document(self, document_path=""):
        self.text = ""
        self.document = document_path
        self.reader = PdfReader(document_path)

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
