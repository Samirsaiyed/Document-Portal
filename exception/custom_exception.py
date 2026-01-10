import traceback
import sys
from logger.custom_logger import CustomLogger
logger=CustomLogger().get_logger(__file__)

class DocumentPortalException(Exception):
    """Custom exception for Document Portal"""
    def __init__(self,error_message):
        _,_,exc_tb= sys.exc_info()
        _, _, exc_tb = sys.exc_info()
        
        # Safely extract file and line number
        if exc_tb:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.lineno = exc_tb.tb_lineno
        else:
            self.file_name = "Unknown"
            self.lineno = 0
            
        self.error_message = str(error_message)
        # Fix: Use format_exc() instead of the undefined error_details
        self.traceback_str = traceback.format_exc() 
        
    def __str__(self):
       return f"""
        Error in [{self.file_name}] at line [{self.lineno}]
        Message: {self.error_message}
        Traceback:
        {self.traceback_str}
        """
    
if __name__ == "__main__":
    try:
        # Simulate an error
        a = 1 / 0
        print(a)
    except Exception as e:
        app_exc=DocumentPortalException(e)
        logger.error(app_exc)
        raise app_exc