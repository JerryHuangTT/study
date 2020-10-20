from threading import Timer

import stream_sensor_producer
import uart
from json import dumps

record = []
import time

def main():
    try:
        uart.open()
        stream_sensor_producer.open()
        res = uart.get()
        if res:
            global record
            record.append(res)
            if len(record) == 10:
                aggregation_data = dumps(record)
                #print(aggregation_data)
                print(time.time())
                stream_sensor_producer.write(aggregation_data)
                record = []
        Timer(0.016, main).start()       
    except Exception as e:
        print(e)
        
main()

def lambda_handler(event, context):
    return