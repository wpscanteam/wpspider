import logging
import sys

from enums import CUSTOM_LOGGING

# Add new logs to the default log system
logging.addLevelName(CUSTOM_LOGGING.RES_FOUND, "RESOURCE FOUND")

# The WPSpider logger
LOGGER = logging.getLogger("wpspiderLog")

LOGGER_HANDLER = None
try:
    from wpspider.spiders.thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

    LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
    
    # Color
    LOGGER_HANDLER.level_map[logging.getLevelName("INFO")] = (None, "cyan", False)
    LOGGER_HANDLER.level_map[logging.getLevelName("RESOURCE FOUND")] = (None, "green", False)
    
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
    


# Format
FORMATTER = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S")

# Set
LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)

# Default level - CUSTOM_LOGGING.RES_FOUND (7)
LOGGER.setLevel(CUSTOM_LOGGING.RES_FOUND)
