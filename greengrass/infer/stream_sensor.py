from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient,
    MessageStreamDefinition,
    StrategyOnFull,
    Persistence,
    S3ExportTaskDefinition,
    Util,
    ExportDefinition,
    S3ExportTaskExecutorConfig,
    StatusConfig,
    StatusLevel,
    StatusMessage,
    Status
)

stream_sensor = 'sensor'
stream_infer = 'infer'
stream_export = 'export'
client = None
last_index = -1

def open_client():
    global client
    if not client:
        client = StreamManagerClient()
        print('delete infer and export stream')
        stream_names = client.list_streams()
        if stream_infer in stream_names:
            client.delete_message_stream(stream_name=stream_infer)
        if stream_export in stream_names:    
            client.delete_message_stream(stream_name=stream_export)
        create_export()
        create_infer()

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

##########################################infer#############################################

def create_infer():
    exports = ExportDefinition(
        s3_task_executor=[
            S3ExportTaskExecutorConfig(
                identifier="S3TaskExecutor" + stream_infer,  # Required
                # Optional. Add an export status stream to add statuses for all S3 upload tasks.
                status_config=StatusConfig(
                    status_level=StatusLevel.DEBUG,  # Default is INFO level statuses.
                    # Status Stream should be created before specifying in S3 Export Config.
                    status_stream_name=stream_export,
                ),
            )
        ]
    )
    client.create_message_stream(MessageStreamDefinition(
        name=stream_infer,
        max_size=536870912,  # 512 MB.
        stream_segment_size=33554432,  # 32 MB.
        time_to_live_millis=None,  # By default, no TTL is enabled.
        strategy_on_full=StrategyOnFull.OverwriteOldestData,  # Required.
        persistence=Persistence.File,  # Default is File.
        flush_on_write=False,  # Default is false.
        export_definition=exports
    ))

file_path = "file:/tmp/jerry.txt"
def write_infer(data):
    try:
        s3_export_task_definition = S3ExportTaskDefinition(input_url=file_path, bucket="allenyangtest", key="jerry/data.txt")
        client.append_message(stream_name=stream_infer, data=Util.validate_and_serialize_to_json_bytes(s3_export_task_definition))

        read_export()
        messages_list = client.read_messages(
            stream_infer, ReadMessagesOptions(min_message_count=1)
        )
        print(messages_list)
    except Exception as e:
        print(e)
        pass

##########################################export#############################################

def create_export():
    client.create_message_stream(MessageStreamDefinition(
        name=stream_export,
        strategy_on_full=StrategyOnFull.OverwriteOldestData,
    ))

def read_export():
    try:
        messages_list = client.read_messages(
            stream_export, ReadMessagesOptions(min_message_count=1)
        )
        print(messages_list)
    except Exception as e:
        print(e)