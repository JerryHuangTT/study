
from greengrasssdk.stream_manager import (
    StreamManagerClient,
    MessageStreamDefinition,
    StrategyOnFull,
    Persistence,
    S3ExportTaskDefinition,
    Util,
    ExportDefinition,
    S3ExportTaskExecutorConfig,
)

stream_export = 'export'
client = None

def open_client():
    global client
    if not client:
        client = StreamManagerClient()
        stream_names = client.list_streams()
        if stream_export not in stream_names:
            create_export()

def create_export():
    exports = ExportDefinition(
        s3_task_executor=[
            S3ExportTaskExecutorConfig(
                identifier="S3TaskExecutor" + stream_export,  # Required
            )
        ]
    )
    client.create_message_stream(MessageStreamDefinition(
        name=stream_export,
        max_size=536870912,  # 512 MB.
        stream_segment_size=33554432,  # 32 MB.
        time_to_live_millis=None,  # By default, no TTL is enabled.
        strategy_on_full=StrategyOnFull.OverwriteOldestData,  # Required.
        persistence=Persistence.File,  # Default is File.
        flush_on_write=False,  # Default is false.
        export_definition=exports
    ))

file_path = "file:/tmp/data.csv"
def export_file_tos3(data):
    try:
        s3_export_task_definition = S3ExportTaskDefinition(input_url=file_path, bucket="allenyangtest", key="jerry/data.csv")
        client.append_message(stream_name=stream_export, data=Util.validate_and_serialize_to_json_bytes(s3_export_task_definition))
    except Exception as e:
        print(e)
        pass