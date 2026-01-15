import os, sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentComparator:

    def __init__(self, base_dir):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_existing_files(self):
        """
        Delete existing files at the specified paths
        """        
        try:
            pass
        except Exception as e:
            raise DocumentPortalException("An error occured while deleting existing files", sys)

    def save_uploaded_file(self):
        """
        Save uploaded file to a specified directory. 
        """
        try:
            pass
        except Exception as e:
            raise DocumentPortalException("An error occured while saving uploaded file", sys)

    def read_pdf(self, pdf_path: Path)-> str:
        """
        Read the pdf file and extract text from each page.
        """
        try:
            with fitz.open(self, pdf_path=str) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF is encrypted")
        
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()

                    if text.strip():
                        all_text.append(f"\n--- Page {page_num + 1} ---\n{text}")
                return "\n".join(all_text)
        
        except Exception as e:
            raise DocumentPortalException("An error occured while reading the pdf file", sys)


