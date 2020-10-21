from greengrasssdk.stream_manager import (
    ReadMessagesOptions,
    StreamManagerClient,
    MessageStreamDefinition,
    StrategyOnFull,
    Persistence,
    S3ExportTaskDefinition,
    Util,
    ExportDefinition,
    S3ExportTaskExecutorConfig
)

stream_sensor = 'sensor'
stream_infer = 'infer'
client = None
last_index = -1

def open():
    global client
    if not client:
        client = StreamManagerClient()
        client.delete_message_stream(stream_name=stream_infer)
        create_stream()

def read():
    global last_index
    try:
        open()
        stream_description = client.describe_message_stream(stream_name=stream_sensor)
        end_index = stream_description.storage_status.newest_sequence_number
        print(stream_description.storage_status)
        print(last_index)  
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
            print(last_index)
            return data
    except Exception as e:
        print(e)


##########################################infer#############################################

def create_stream():
    '''
    exports = ExportDefinition(
            s3_task_executor=[S3ExportTaskExecutorConfig(identifier="s3Export{}".format(stream_infer))]
        )
    '''
    stream_names = client.list_streams()
    if stream_infer not in stream_names:
        client.create_message_stream(MessageStreamDefinition(
            name=stream_infer,
            max_size=536870912,  # 512 MB.
            stream_segment_size=33554432,  # 32 MB.
            time_to_live_millis=None,  # By default, no TTL is enabled.
            strategy_on_full=StrategyOnFull.OverwriteOldestData,  # Required.
            persistence=Persistence.File,  # Default is File.
            flush_on_write=False,  # Default is false.
            #export_definition=exports
        ))

import json

def write(data):
    try:
        '''
        client.append_message(stream_name=stream_infer, data=data.encode())
        stream_description = client.describe_message_stream(stream_name=stream_infer)
        print(stream_description.storage_status)
        '''
        s3_export_task_definition = S3ExportTaskDefinition(input_url="/tmp/jerry.txt", bucket="allenyangtest", key="jerry/data.txt")
        sequence_number = client.append_message(stream_name=stream_sensor, data=Util.validate_and_serialize_to_json_bytes(s3_export_task_definition))
        print('export {}'.format(sequence_number))
    except Exception as e:
        print(e)
        pass