from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient
)

stream_name = 'sensor'
client = None

def open():
    global client
    if not client:
        client = StreamManagerClient()

def main():
    try:
        open()
        stream_description = client.describe_message_stream(stream_name=stream_name)
        start_index = stream_description.storage_status.oldest_sequence_number
        end_index = stream_description.storage_status.newest_sequence_number
        new_bytes = stream_description.storage_status.total_bytes
        print(stream_description.storage_status)     
        if new_bytes > 0 :#流中有可用数据
            count = end_index - start_index + 1
            return client.read_messages(
                    stream_name=stream_name,
                    options=ReadMessagesOptions(
                        desired_start_sequence_number=start_index,
                        min_message_count=count,
                        max_message_count=1000,
                        read_timeout_millis=0
                        ))
    except Exception as e:
        print(e)