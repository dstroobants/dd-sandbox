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
        'rate': '180.01Mbps',
        'ClientRequestPath': '//hup/payments/abcdefg-1234-5678-ab12-345678901234',
        'ClientRequestMethod': 'GET',
        'ClientRequestHost': 'api.hup.com',
        'ClientRequestPort': '443',
        'ClientRequestProtocol': 'https' 
    })
