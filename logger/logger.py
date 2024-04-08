import logging

logger = logging.getLogger()
logger.name = 'yangai-logger'

formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

file_handler = logging.FileHandler('yangai.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
