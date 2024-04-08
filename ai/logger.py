import logging
from logging import getLogger

logger = getLogger('ai')

# logger format
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to logger
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


