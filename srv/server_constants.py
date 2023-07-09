import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # folder srv is included

TESSERACT_EXE_PATH = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
TESSERACT_DATA_PATH = '--tessdata-dir "D:\Program Files\Tesseract-OCR\\tessdata"'
POPPLER_PATH = r"D:\poppler-0.68.0_x86\poppler-0.68.0\bin"
TEMP_PDF_PATH = "D:\pycharm_projecs\learning-engine-phc\Academic_papers\\1-s2.0-S0092867421000118-main.pdf"

CROSSWORD_TXT_PATH = CONFIG_PATH = os.path.join(ROOT_DIR, 'models','Crossword','cwf-spec.txt') 