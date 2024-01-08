import logging


class ErrorLogger:
    logger = None

    @classmethod
    def initialize_logger(cls):
        if not cls.logger:
            cls.logger = logging.getLogger(__name__)
            cls.logger.setLevel(logging.ERROR)

            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')

            file_handler = logging.FileHandler('error.log')
            file_handler.setFormatter(formatter)

            cls.logger.addHandler(file_handler)

    @classmethod
    def get_logger(cls):
        if not cls.logger:
            cls.initialize_logger()
        return cls.logger
