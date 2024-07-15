import logging

class ColoredLogger:
    # 类属性，用于存储单例实例
    _instance = None

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
            super().__init__(fmt, datefmt="%Y-%m-%d %H:%M:%S")
            self.colors = colors

        def format(self, record):
            log_fmt = super().format(record)
            levelname_color = self.colors.get(record.levelname, self.colors["RESET"])
            record.levelname = f"{levelname_color}{record.levelname}{self.colors['RESET']}"
            return log_fmt

    def __new__(cls, name="my_logger", level=logging.DEBUG):
        if cls._instance is None:
            cls._instance = super(ColoredLogger, cls).__new__(cls)
            cls._instance._name = name
            cls._instance._level = level
            cls._instance._logger = None
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        self.logger = logging.getLogger(self._name)
        self.logger.setLevel(self._level)
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(self._level)
            formatter = self.ColorFormatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                self.COLORS
            )
            ch.setFormatter(formatter)
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
