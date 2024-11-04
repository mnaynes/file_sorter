import os
import pandas as pd
import PyPDF2
import re
import time
from file_sorter_constants import *

class FileType:
    def __init__(self, type, df, folder, path):
        self.type = type
        self.df = df
        self.folder = folder
        self.output_dir = os.path.join(path, folder)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_info():
        pass

    def get_date_modified(self, file):
        ti_m = os.path.getmtime(file)
        m_ti = time.ctime(ti_m)
        t_obj = time.strptime(m_ti)

        return time.strftime("%m/%d/%Y", t_obj)
    
class DocumentType(FileType):
    def get_word_count():
        pass

    def save_info(self, filename, df, src_path):
        src = os.path.join(src_path, filename)
        date_modified = super().get_date_modified(src)
        word_count = self.get_word_count(src)

        return df.append({
            FILENAME : filename,
            WORD_COUNT : word_count,
            DATE_MODIFIED : date_modified},
            ignore_index=True)
    
class ImageType(FileType):
    def __init__(self, path):
        super().__init__("Images", pd.DataFrame(columns=[FILENAME, FILE_TYPE,
                                                         DATE_MODIFIED]),
                                                         "images",
                                                         path)
    
    def save_info(self, filename, df, src_path):
        src = os.path.join(src_path, filename)
        file_ext = os.path.splitext(filename)
        date_modified = super().get_date_modified(src)

        return df.append({
            FILENAME : filename,
            FILE_TYPE : file_ext[1].replace(".","").lower(),
            DATE_MODIFIED : date_modified},
            ignore_index=True)
    
class PDFType(DocumentType):
    def __init__(self, path):
        super().__init__("PDFs", pd.DataFrame(columns=[FILENAME, WORD_COUNT,
                                                       DATE_MODIFIED]),
                                                       "pdf",
                                                       path)
    
    """
    Reading PDF files returns hyphenated words with a space in between
    ex. "armour-like" is read as "armour -like"
    To get the accurate word count, this merges the hyphenated words as expected.
    """
    def pdf_special_case(self, text):
        return re.sub(r"([^\W_]+) -([^\W_]+)", r"\1-\2", text)
    
    def get_word_count(self, pdf):
        file = open(pdf, "rb")
        read_PDF = PyPDF2.PdfReader(file)
        pages = len(read_PDF.pages)
        word_count = 0

        for i in range(pages):
            page_obj = read_PDF.pages[i]
            extracted_text = page_obj.extract_text()
            text = self.pdf_special_case(extracted_text)
            words = re.findall(WORD_REGEX, text, re.MULTILINE)
            word_count += len(words)
        
        return word_count
    
class TXTType(DocumentType):
    def __init__(self, path):
        super().__init__("Documents", pd.DataFrame(columns=[FILENAME, WORD_COUNT,
                                                            DATE_MODIFIED]),
                                                            "docs",
                                                            path)
        
    def get_word_count(self, txt):
        word_count = 0

        with open(txt, "r") as file:
            text = file.read()
            words = re.findall(WORD_REGEX, text, re.MULTILINE)
            word_count = len(words)
        
        return word_count
