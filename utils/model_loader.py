import os
import sys

from utils.config_loader import load_config

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

logger = CustomLogger().get_logger(__name__)

class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        logger.info("Configuration loaded successfully.", config_keys=list(self.config.keys()))

    def _validate_env(self):
        """
        Validate the environment variables.
        Ensuring API key exist.
        """

        required_vars = ["OPENAI_API_KEY"]
        self.api_keys={key: os.getenv(key) for key in required_vars}
        missing = [k for k,v in self.api_keys.items() if not v]
        if missing:
            logger.error("Missing Environment Vairables", missing_vars=missing)
            raise DocumentPortalException("Missing environment variables", sys)
        logger.info("Environment variablrd is valid.")

    def load_embeddings(self):
        """
        Load and return the embedding models.
        """

        try:
            logger.info("Loading embedding model...")
            model_name = self.config["embedding_model"]["model_name"]
            return OpenAIEmbeddings(model=model_name)
        except Exception as e:
            logger.error("Error loading emedding model", error=str(e))
            raise DocumentPortalException("Failed to load embedding model.", sys)

    def load_llm(self):
        """
        Load and return the LLM model.
        """
        """"Load LLM Dynamically based on provider in config."""

        llm_block = self.config["llm"]
        logger.info("loading LLM...")

        # Default provider 
        provider_key = os.getenv("LLM_PROVIDER", "openai")

        if provider_key not in llm_block:
            logger.error("LLM provider not found in config", provider_key=provider_key)
            raise ValueError(f"Provider '{provider_key}' no found in config")

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_tokens", 2048)

        logger.info("LLM provider found in config", provider=provider, model_name=model_name, temperature=temperature, max_tokens=max_tokens)

        if provider == "openai":
            return ChatOpenAI(
                model=model_name,
                api_key = self.api_keys["OPENAI_API_KEY"],
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            logger.info("Upsupported LLM Provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")

if __name__ == "__main__":
    loader = ModelLoader()

    # Test embedding model loading
    embeddings = loader.load_embeddings()
    print(f"Embedding model loaded: {embeddings}")

    # Test LLM loading based on YAML config
    llm = loader.load_llm()
    print(f"LLM model loaded: {llm}")

    # Test the ModelLoader
    result = llm.invoke("Hello, how are you?")
    print(f"LLM result: {result.content}")



