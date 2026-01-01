import os
from utils.config_loader import Config
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.model import *
from langchain.output_parsers import JsonOutputToolsParser
from langchain.output_parsers import OutputFixingParser

class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model.
    Automatically logs all actions and supports session-based organization.
    """

    def __init__(self):
        

    def analyzer_metdata(self):
        pass
        