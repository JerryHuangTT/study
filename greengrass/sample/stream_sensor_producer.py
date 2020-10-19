from greengrasssdk.stream_manager import (
    ExportDefinition,
    MessageStreamDefinition,
    ReadMessagesOptions,
    StrategyOnFull,
    StreamManagerClient,
    Persistence
)

client = None
stream_name = 'sensor'

def open():
    global client
    if not client:
        client = StreamManagerClient()
        client.delete_message_stream(stream_name="sensor")

def main(data):
    try:
        open()
        stream_names = client.list_streams()
        if stream_name not in stream_names:
            client.create_message_stream(MessageStreamDefinition(
                name=stream_name,
                max_size=268435456,  # Default is 256 MB.
                stream_segment_size=16777216,  # Default is 16 MB.
                time_to_live_millis=None,  # By default, no TTL is enabled.
                strategy_on_full=StrategyOnFull.OverwriteOldestData,  # Required.
                persistence=Persistence.File,  # Default is File.
                flush_on_write=False,  # Default is false.
            ))
        client.append_message(stream_name=stream_name, data=data.encode())
        stream_description = client.describe_message_stream(stream_name=stream_name)
        print(stream_description.storage_status)
    except Exception as e:
        print(e)
        pass