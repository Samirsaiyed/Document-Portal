import os
import logging
import sys
from datetime import datetime
import structlog

class CustomLogger:
    _configured = False

    def __init__(self, log_dir="logs", level=logging.INFO):
        self.log_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)
        
        log_file = f"{datetime.now().strftime('%Y-%m-%d')}.log"
        self.log_file_path = os.path.join(self.log_dir, log_file)
        
        if not CustomLogger._configured:
            self._configure_structlog(level)
            CustomLogger._configured = True

    def _configure_structlog(self, level):
        # 1. Define common processors
        shared_processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
        ]

        # 2. Configure Standard Library Handlers
        # File Handler (JSON)
        file_handler = logging.FileHandler(self.log_file_path)
        file_formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(), # Machine readable
            foreign_pre_chain=shared_processors,
        )
        file_handler.setFormatter(file_formatter)

        # Console Handler (Pretty Printing)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(colors=True), # Human readable
            foreign_pre_chain=shared_processors,
        )
        console_handler.setFormatter(console_formatter)

        # 3. Apply configuration to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.setLevel(level)

        # 4. Configure Structlog to use the Stdlib wrapper
        structlog.configure(
            processors=shared_processors + [
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(self, name=None):
        return structlog.get_logger(name or __name__)

# --- Usage ---
if __name__ == "__main__":
    # Initialize once
    log_factory = CustomLogger()
    logger = log_factory.get_logger("AppModule")

    # Add global context (e.g., in a web request)
    structlog.contextvars.bind_contextvars(request_id="abc-123")

    logger.info("User logged in", user_id=42, email="test@example.com")
    logger.error("Database connection failed", db_name="primary_replica")