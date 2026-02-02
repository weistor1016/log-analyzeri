import logging
import sys
from structlog import configure, get_logger, processors, stdlib

def setup_logging(log_level: str = "INFO"):
    logging.basicConfig(
        format="%(message)s", 
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )

    configure(
        processors=[
            stdlib.filter_by_level,
            processors.TimeStamper(fmt="iso"),
            processors.JSONRenderer(),
        ],
        logger_factory=stdlib.LoggerFactory(),
        wrapper_class=stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


logger = get_logger()