from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient,
)

stream_sensor = 'sensor'
client = None

def open_client():
    global client
    if not client:
        client = StreamManagerClient()

def read_sensor(index,count):
    try:
        open_client()
        data = client.read_messages(
            stream_name=stream_sensor,
            options=ReadMessagesOptions(
                desired_start_sequence_number = index,
                min_message_count = 1,
                max_message_count = count,
                read_timeout_millis=0
                ))
        return data
    except Exception as e:
        print(e)