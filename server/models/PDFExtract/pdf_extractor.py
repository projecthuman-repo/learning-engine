"""
Extracts the contents of a pdf using either optical charavyer recognition (ocr) or a normal read.
"""

from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract as tess
import os
import re
import concurrent.futures
import server.models.PDFExtract.pdf_extractor_constants as pdf_extractor_constants

class Extractor:
    def __init__(self, document_path=""):
        # the below line of text is required as we need tesseract.exe installed to use the library.
        # change it to whatever local path you are using
        tess.pytesseract.tesseract_cmd = pdf_extractor_constants.TESSERACT_EXE_PATH
        self.tessdata_dir_config = pdf_extractor_constants.TESSERACT_DATA_PATH
        # Example config: '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
        # It's important to include double quotes around the dir path.

        self.text = ""
        self.document = None
        self.reader = None
        self.document_name = None
        if document_path != "":  # if an argument is provided in the constructor
            self.change_document(document_path)

    # Saves one page individually 
    def getPage(self,x,images):
        # Save pages as images of the pdf. only way optical character recognition will work
        images.save('page' + str(x) + '.png', 'PNG')
        # gets text from the page
        path = "page"+str(x)+".png"
        text=tess.image_to_string("page"+str(x)+".png",config=self.tessdata_dir_config) + "\n"
        # delete the generated image file.
        os.remove("page" + str(x) + ".png")
        return text


    # Uses multithreading to save all the images at once
    def ocr_read(self, path):
        images = convert_from_path(path, poppler_path=pdf_extractor_constants.POPPLER_PATH)
        # Use concurrent.futures instead of for loop
        with concurrent.futures.ThreadPoolExecutor() as ex:
            pgText=ex.map(self.getPage,range(len(images)),images)
        for txt in pgText:
            self.text+=txt


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
        if self.reader.metadata.title is not None:
            self.document_name = self.reader.metadata.title
        else:
            self.document_name = document_path.split(".pdf")[0]

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
                pdf_to_txt = open("output.txt", "w+", encoding="utf-8")
            pdf_to_txt.write(self.text)
            pdf_to_txt.close()

    # return the extracted text
    def get_text(self):
        if self.text != "" or None:
            self.filter()
            return self.text

    # used to remove unnecessary bits from academic papers
    # will remove everything before the introduction and everything after the references
    # will remove stuff from pages with only images (by setting a word limit)
    def filter(self):
        if self.text != "" or None:
            result = re.split("we are at a historic", self.text, flags=re.IGNORECASE)
            if len(result) > 1:
                self.text = "we are at a historic"+result[1]
            result = re.split("references", self.text, flags=re.IGNORECASE)
            if len(result) > 1:
                self.text = result[0]

if __name__ == "__main__":
    extractor = Extractor()
    extractor.ocr_read(pdf_extractor_constants.TEMP_PDF_PATH)
    txt = extractor.get_text()
    txt = txt[0:250]
    txtb ="Amir Sarah Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
    print(len(txtb))
    print(txt)
