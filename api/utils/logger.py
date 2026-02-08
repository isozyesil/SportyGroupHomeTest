import logging
import sys

class FrameworkLogger:
    @staticmethod
    def get_logger(name="framework"):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
            )

            # Console Handler
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

            # File Handler
            fh = logging.FileHandler("framework.log", mode="a")
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            
            # Prevent double logging if parent loggers have handlers
            logger.propagate = False

        return logger

# Global logger instance
logger = FrameworkLogger.get_logger()
