import logging
import platform
import sys
from threading import Timer

import greengrasssdk
import uart
import json
# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


client = greengrasssdk.client("iot-data")
my_platform = platform.platform()

def greengrass_hello_world_run():
    try:
        uart.open()
        rx_str = uart.query_rx()
        if rx_str:
            if not my_platform:
                client.publish(
                    topic="hello/sample", queueFullPolicy="AllOrException", payload=rx_str
                )
            else:
                client.publish(
                    topic="hello/sample",
                    queueFullPolicy="AllOrException",
                    payload=json.dumps({'rx':rx_str})
                )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(1, greengrass_hello_world_run).start()


# Start executing the function above
greengrass_hello_world_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def lambda_handler(event, context):
    return
