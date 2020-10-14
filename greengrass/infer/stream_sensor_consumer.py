from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient
)

stream_name = 'sensor'

def open():
    global client
    if not client:
        client = StreamManagerClient()

def main():
    try:
        open()
        message_list = client.read_messages(
                stream_name=stream_name,
                options=ReadMessagesOptions(
                    desired_start_sequence_number=0,
                    min_message_count=100,
                    max_message_count=1000,
                    read_timeout_millis=0
                    )
            )
        print(message_list)
        return message_list
    except Exception as e:
        print(e)