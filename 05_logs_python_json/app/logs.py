import logging
from pythonjsonlogger.json import JsonFormatter
from time import time, sleep

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set log level to INFO

logHandler = logging.StreamHandler()
formatter = JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

while True:
    sleep(5 - time() % 5)
    logger.info('Json Logging Event', extra={
        'key1': 'value1',
        'rate': '180.01Mbps'
    })
