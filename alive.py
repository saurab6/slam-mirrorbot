# Implement By - @anasty17 (https://github.com/SlamDevs/slam-mirrorbot/commit/0bfba523f095ab1dccad431d72561e0e002e7a59)
# (c) https://github.com/SlamDevs/slam-mirrorbot
# All rights reserved

import time
import requests
import os
import logging

logging.info("GETTING BASE URL")
try:
    BASE_URL = os.environ.get('BASE_URL_OF_BOT', None)
    logging.info(BASE_URL)
except Exception:
    logging.info("ERROR WHILE GETTING BASE_URL")
try:
    if len(BASE_URL) == 0:
        BASE_URL = None
except:
    BASE_URL = None
PORT = os.environ.get('PORT', None)
print(str(PORT))
print("checking")
if PORT is not None and BASE_URL is not None:
    while True:
        print("OHH YEAH")
        time.sleep(600)
        status = requests.get(BASE_URL).status_code
