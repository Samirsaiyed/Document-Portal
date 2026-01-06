import os
import sys
import fitz
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """
    Handles PDF saving and reading operations.
    Automatically logs all actions and supports session-based organization.
    """

    def __init__(self, data_dir=None, session_id=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv( 
                    "DATA_STORAGE_PATH", 
                    os.path.join(os.getcwd(), "data", "document_analysis")
            )
            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S ')}_{uuid.uuid4().hex[:8]}"

            # Create base session directory
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)

            self.log.info("PDFHandler intialized", session_id=self.session_id, session_path=self.session_path)
        except Exception as e:
            self.log.error(f"Error intializing DocumentHanlder: {e}")
            raise DocumentPortalException("Error intializing DocumentHandler", e) from e

    def save_pdf(self, uploaded_file):
        try:
            # Convert name to string to ensure os.path.basename works
            filename = os.path.basename(str(uploaded_file.name))

            # 1. Validation (This block only runs if the file is BAD)
            if not filename.lower().endswith(".pdf"):
                raise DocumentPortalException("Invalid file type, Only PDFs are allowed.")

            # 2. Saving Logic (This MUST be at the same level as the 'if')
            save_path = os.path.join(self.session_path, filename)
            
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            self.log.info("PDF saved successfully", 
                          file=filename, 
                          save_path=save_path, 
                          session_id=self.session_id)
            
            return save_path # Now this will execute for PDF files
        
        except Exception as e:
            self.log.error(f"Error saving PDF: {e}")
            raise DocumentPortalException("Error saving PDF", e) from e

    def read_pdf(self, pdf_path:str)->str :
        try:
            text_chunks = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    text_chunks.append(f"\n--- Page {page_num} ---\n{page.get_text()}")
            text = "\n".join(text_chunks)

            self.log.info("PDF read successfully", pdf_path=pdf_path, session_id=self.session_id)
            return text

        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("Error reading PDF", e) from e
    
if __name__ == '__main__':
    from pathlib import Path
    from io import BytesIO
    

    pdf_path = r"/home/user/document-portal/data/document_analysis/attention_all_you_need_paper.pdf"

    class DummyFile:
        def __init__(self, file_path):
            self.name = Path(file_path)
            self._file_path = file_path

        def getbuffer(self):
            return open(self._file_path, "rb").read()

    dummy_pdf = DummyFile(pdf_path)

    handler = DocumentHandler(session_id="test_session")

    try:
        save_path = handler.save_pdf(dummy_pdf)
        print(f"PDF saved to: {save_path}")

        content = handler.read_pdf(save_path)
        print("PDF Content: ")
        print(content[:500])

    except Exception as e:
        print(f"Error: {e}")

