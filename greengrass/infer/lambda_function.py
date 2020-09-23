import logging
import sys
from threading import Timer
import greengrasssdk

import json
import load_model

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

client = greengrasssdk.client("iot-data")
def greengrass_hello_world_run():
    try:
        res = load_model.main()
        if res:
            client.publish(topic="hello/model",
            queueFullPolicy="AllOrException",
            payload=json.dumps({'res':res})
            )
    except Exception as e:
        logger.error("Failed to publish message: " + repr(e))

    Timer(10, greengrass_hello_world_run).start()

greengrass_hello_world_run()

def lambda_handler(event, context):
    return
