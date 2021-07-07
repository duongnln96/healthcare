import logging

def get_logger():
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger

def info(logger, msg: str):
    logger.info(msg=msg)

def debug(logger, msg: str):
    logger.info(msg=msg)

def err(logger, msg: str):
    logger.error(msg=msg)
