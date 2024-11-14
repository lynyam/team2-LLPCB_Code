import colorlog
import logging

def safely_add_trace_level():
    """
    Safely adds TRACE level to logging if it doesn't exist.
    Returns the TRACE level number.
    """
    TRACE_LEVEL_NUM = logging.DEBUG - 5
    TRACE_LEVEL_NAME = 'TRACE'
    
    # Check if TRACE level already exists
    if not hasattr(logging, TRACE_LEVEL_NAME):
        def trace_for_level(self, message, *args, **kwargs):
            if self.isEnabledFor(TRACE_LEVEL_NUM):
                self._log(TRACE_LEVEL_NUM, message, args, **kwargs)

        def trace_to_root(message, *args, **kwargs):
            logging.log(TRACE_LEVEL_NUM, message, *args, **kwargs)

        logging.addLevelName(TRACE_LEVEL_NUM, TRACE_LEVEL_NAME)
        setattr(logging, TRACE_LEVEL_NAME, TRACE_LEVEL_NUM)
        setattr(logging.getLoggerClass(), TRACE_LEVEL_NAME.lower(), trace_for_level)
        setattr(logging, TRACE_LEVEL_NAME.lower(), trace_to_root)
    
    return getattr(logging, TRACE_LEVEL_NAME)

def get_logger(name=None):
    """
    Creates and configures a logger with colored output and TRACE level support.
    
    Args:
        name (str, optional): Logger name. Defaults to __name__ of calling module.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Use provided name or fall back to __name__
    logger_name = name if name is not None else __name__
    
    # Create or get logger instance
    logger = logging.getLogger(logger_name)
    
    # Only configure if logger doesn't have handlers
    if not logger.handlers:
        # Clear any existing handlers and prevent propagation
        logger.handlers = []
        logger.propagate = False
        
        # Add TRACE level safely
        trace_level = safely_add_trace_level()
        logger.setLevel(trace_level)

        # Create and configure handler
        handler = logging.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | >>> %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
            log_colors={
                'TRACE': 'purple',
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger