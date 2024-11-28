import logging
from colorama import Fore, Style, init

# Ініціалізація colorama
init(autoreset=True)

# Налаштування кольорових логів


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"


def get_logger(name: str, level=logging.INFO):
    """
    Створює логер із кольоровими повідомленнями.
    :param name: Ім'я логера
    :param level: Рівень логування (за замовчуванням INFO)
    :return: Логер
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Уникаємо дублювання обробників
        logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter(
            "%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(console_handler)
    return logger
