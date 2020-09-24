import logging
import sys

import greengrasssdk
from threading import Thread
import uart
import json
import time
# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
client = greengrasssdk.client("iot-data")
'''
def main():
    while True:
        try:
            if uart.open():
                rx_str = uart.get()
            if rx_str:
                rx_str = json.dumps({'rx':rx_str})
                #client.publish(topic="hello/sample",queueFullPolicy="AllOrException",payload=rx_str)
        except Exception as e:
            logger.error("Failed to publish message: " + repr(e))
        finally:
            time.sleep(0.001)  

th = Thread(target=main)
th.start()
'''
def lambda_handler(event, context):
    return