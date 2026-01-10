import os, sys

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.config_loader import Config
from utils.model_loader import ModelLoader
from model.models import *
from prompt.prompt_libraries import *

from langchain.output_parsers import JsonOutputToolsParser, OutputFixingParser

class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model.
    Automatically logs all actions and supports session-based organization.
    """

    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            # load the model
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            # Create parser
            self.parser = JsonOutputToolsParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

            self.prompt = prompt

            self.log.info("DocumentAnalyzer Intialized successfully.")

        except Exception as e:
            self.log.error(f"Error Initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException("Error Initializing DocumentAnalyzer", sys)

    def analyzer_document(self, document_text: str):
        """
        Analyze a document's text and extract structured metadata & summary.
        """
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("Meta-data analysis chain initialized")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": self.document_text
            })

            self.log.info("Meta-data analysis chain executed", keys=list(response.keys()))
            return response

        except Exception as e:
            self.log.error(f"Metadata analysis failed: error=str{e}")
            raise DocumentPortalException("Metadata extraction failed") from e

    
    def analyzer_metdata(self):
        pass
        