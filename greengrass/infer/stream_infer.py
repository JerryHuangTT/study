from greengrasssdk.stream_manager import (
    StreamManagerClient,
    MessageStreamDefinition,
    StrategyOnFull,
    Persistence,
)

stream_infer = 'infer'
client = None

def open_client():
    global client
    if not client:
        client = StreamManagerClient()

def create_infer():
    stream_names = client.list_streams()
    if stream_infer not in stream_names:
        print('recreate infer because of exporting delete')
        client.create_message_stream(MessageStreamDefinition(
            name=stream_infer,
            max_size=536870912,  # 512 MB.
            stream_segment_size=33554432,  # 32 MB.
            time_to_live_millis=None,  # By default, no TTL is enabled.
            strategy_on_full=StrategyOnFull.OverwriteOldestData,  # Required.
            persistence=Persistence.File,  # Default is File.
            flush_on_write=False,  # Default is false.
        ))

def write_infer(data):
    try:
        open_client()
        print('check if infer has been deleted: listing stream')
        create_infer()
        print('start to append infer')
        client.append_message(stream_name=stream_infer, data=data.encode())
        print('start to read infer status')
        stream_description = client.describe_message_stream(stream_name=stream_infer)
        print(stream_description.storage_status)
    except Exception as e:
        print(e)
        pass