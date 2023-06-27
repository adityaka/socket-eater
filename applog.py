import logging
import os.path as path
import sys

class LoggerFactory(object):
    _root_logger = None
    
    @classmethod
    def _get_default_formatter(cls):
        return logging.Formatter("%(asctime)s | %(levelname)s | %(module)s | %(message)s")
    
    @classmethod
    def get_default_handler(cls):
        default_handler =  logging.StreamHandler(sys.stderr)
        default_handler.setFormatter(cls._get_default_formatter())
    
    @classmethod
    def get(cls, logger_name: str, log_handler: logging.Handler = None ) -> logging.Logger:
        if not log_handler:
            log_handler = cls.get_default_handler()
        if not logger_name:
            logger_name = (path.split(__file__)[1]).replace(".py","")
        if not cls._root_logger:
            root_logger = logging.getLogger(logger_name)
            root_logger.addHandler(log_handler)
            cls._root_logger = root_logger
            cls._root_logger.setLevel(logging.DEBUG)
            return cls._root_logger
        elif cls._root_logger.name == logger_name:
            return cls._root_logger
        elif logger_name in cls._root_logger.manager.loggerDict.keys():
            child_logger =  cls._root_logger.getChild(logger_name)
            child_logger.setHandler(log_handler)
            return child_logger
        else:
            return cls._root_logger.getChild(logger_name)