from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient,
)

stream_sensor = 'sensor'
client = None
last_index = -1

def open_client():
    global client
    if not client:
        client = StreamManagerClient()

def read_sensor():
    global last_index
    try:
        open_client()
        stream_description = client.describe_message_stream(stream_name=stream_sensor)
        end_index = stream_description.storage_status.newest_sequence_number
        print(stream_description.storage_status)
        if end_index > last_index :#流中有可用数据
            count = end_index - last_index
            print(count)
            data = client.read_messages(
                stream_name=stream_sensor,
                options=ReadMessagesOptions(
                    desired_start_sequence_number=last_index + 1,
                    min_message_count=count,
                    max_message_count=3000,
                    read_timeout_millis=0
                    ))
            last_index = end_index
            return data
    except Exception as e:
        print(e)