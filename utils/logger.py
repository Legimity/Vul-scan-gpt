import logging


class ColoredLogger:
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    class ColorFormatter(logging.Formatter):
        def __init__(self, fmt, colors):
            super().__init__(fmt, datefmt="[%H:%M:%S]")
            self.colors = colors

        def format(self, record):
            # Ensure asctime is set
            if not hasattr(record, "asctime"):
                record.asctime = self.formatTime(record, self.datefmt)
            # Apply color to the log level name and timestamp
            levelname_color = self.colors.get(record.levelname, self.colors["RESET"])
            asctime_color = self.colors["RESET"]
            record.levelname = (
                f"{levelname_color}{record.levelname}{self.colors['RESET']}"
            )
            record.asctime = f"{asctime_color}{record.asctime}{self.colors['RESET']}"
            return super().format(record)

    def __init__(self, name="my_logger", level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create console handler and set level
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create formatter and add it to the handler
        formatter = self.ColorFormatter(
            "%(asctime)s - %(levelname)s - %(message)s", self.COLORS
        )
        ch.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger


# Example usage
# if __name__ == "__main__":
#     logger = ColoredLogger().get_logger()
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")
