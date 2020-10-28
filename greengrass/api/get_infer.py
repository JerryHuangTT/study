from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient,
)
from json import loads

client = None

def open_client():
    global client
    if not client:
        client = StreamManagerClient()

def read_sensor(index,count):
    try:
        open_client()
        msgs = client.read_messages(
            stream_name = 'infer',
            options=ReadMessagesOptions(
                desired_start_sequence_number = index,
                min_message_count = 1,
                max_message_count = count,
                read_timeout_millis=0
                ))
        res = []
        for msg in msgs:
            record = loads(msg.payload.decode())
            for data in record:
                res.append(data) 
        return res
    except Exception as e:
        print(e)