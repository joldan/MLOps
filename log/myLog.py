### LOGGING Python

import logging as log
from logging.handlers import RotatingFileHandler
from os.path import dirname, abspath
logPath = (dirname(abspath(__file__)))
logName = "app.log"

# Define system log
rf_handler = RotatingFileHandler((logPath+"/"+logName), maxBytes=10_000_000, backupCount=5, encoding='utf-8', mode='w')
log.basicConfig(encoding='utf-8',format='%(asctime)s %(message)s', level=log.INFO,handlers=[rf_handler])
log.info(f"Main -> %s - Start Log",__name__)