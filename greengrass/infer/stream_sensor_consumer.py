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
        max_count = stream_description.newest_sequence_number
        print(max_count)        
        message_list = client.read_messages(
                stream_name=stream_name,
                options=ReadMessagesOptions(
                    desired_start_sequence_number=max_count-15,
                    min_message_count=10,
                    max_message_count=15,
                    read_timeout_millis=0
                    )
            )

        return message_list
    except Exception as e:
        print(e)