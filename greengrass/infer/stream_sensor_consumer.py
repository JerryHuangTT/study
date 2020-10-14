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
        print(stream_description.storage_status)     
        if end_index > start_index and end_index > start_index + 10 :
            return client.read_messages(
                    stream_name=stream_name,
                    options=ReadMessagesOptions(
                        desired_start_sequence_number=0,
                        min_message_count=10,
                        max_message_count=15,
                        read_timeout_millis=0
                        ))
    except Exception as e:
        print(e)