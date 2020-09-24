import logging
import sys
from threading import Timer
import greengrasssdk

import json
import load_model
import uart
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client("iot-data")
def main():
    try:
        uart.open()
        inputs = uart.get()
        if inputs:
            print(inputs)
            results = load_model.main(inputs)
            results_str = json.dumps({'res':results})
            uart.send(results_str)
            client.publish(topic="hello/model",queueFullPolicy="AllOrException",payload=results_str)
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))
    Timer(0.001, main).start()

main()

def lambda_handler(event, context):
    return
