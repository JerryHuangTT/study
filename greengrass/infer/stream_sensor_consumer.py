from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient
)

stream_name = 'sensor'
client = None
last_index = 0

def open():
    global client
    if not client:
        client = StreamManagerClient()

def main():
    global last_index
    try:
        open()
        stream_description = client.describe_message_stream(stream_name=stream_name)
        end_index = stream_description.storage_status.newest_sequence_number
        print(stream_description.storage_status)
        print(last_index)  
        if end_index > last_index :#流中有可用数据
            count = end_index - last_index + 1
            data = client.read_messages(
                stream_name=stream_name,
                options=ReadMessagesOptions(
                    desired_start_sequence_number=last_index,
                    min_message_count=count,
                    max_message_count=3000,
                    read_timeout_millis=0
                    ))
            last_index = end_index
            print(last_index)
            return data
    except Exception as e:
        print(e)