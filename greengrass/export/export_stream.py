from greengrasssdk.stream_manager import (
    StreamManagerClient,
    MessageStreamDefinition,
    StrategyOnFull,
    Persistence,
    S3ExportTaskDefinition,
    Util,
    ExportDefinition,
    S3ExportTaskExecutorConfig,
    ReadMessagesOptions
)

stream_export = 'export'
client = None

def open_client():
    global client
    if not client:
        client = StreamManagerClient()
        client.delete_message_stream(stream_export)

def create_export():
    stream_names = client.list_streams()
    if stream_export in stream_names:
        client.delete_message_stream(stream_export)
    exports = ExportDefinition(
        s3_task_executor=[
            S3ExportTaskExecutorConfig(
                identifier="S3TaskExecutor" + stream_export,  # Required
            )
        ]
    )
    client.create_message_stream(MessageStreamDefinition(
        name=stream_export,
        max_size=53687091,  # 51 MB.
        stream_segment_size=3355443,  # 3 MB.
        time_to_live_millis=None,  # By default, no TTL is enabled.
        strategy_on_full=StrategyOnFull.OverwriteOldestData,  # Required.
        persistence=Persistence.File,  # Default is File.
        flush_on_write=False,  # Default is false.
        export_definition=exports
    ))

def export_file_tos3():
    try:
        s3_export_task_definition = S3ExportTaskDefinition(input_url="file:/tmp/data.csv",
                            bucket="allenyangtest",
                            key='jerry/{}.csv'.format(get_time()))
        client.append_message(stream_name=stream_export, 
                        data=Util.validate_and_serialize_to_json_bytes(s3_export_task_definition))
    except Exception as e:
        print(e)
        pass

stream_infer = 'infer'
def read_infer():
    try:
        create_export()
        stream_description = client.describe_message_stream(stream_name=stream_infer)
        print(stream_description.storage_status)
        print('start to read')
        msgs = client.read_messages(
            stream_name=stream_infer,
            options=ReadMessagesOptions(
                desired_start_sequence_number=0,
                min_message_count=stream_description.storage_status.newest_sequence_number,
                max_message_count=100000,
                read_timeout_millis=0
                ))
        print('finish read')
        save(parse(msgs))
        print('finish parse')
        export_file_tos3()
    except Exception as e:
        print(e)

from json import loads
import pandas as pd
def parse(msgs):
    rows = []
    for msg in msgs:
        record = loads(msg.payload.decode())
        for data in record:
            rows.append(data)
    print(len(rows))
    return rows

def save(data):
    print('start to save to csv')
    df = pd.DataFrame(columns=['timestamp','x1','x2','y1','y2','z1','z2','type'],
                                data=data)
    df.to_csv('/tmp/data.csv',index=False)
    print('finish save')
    #client.delete_message_stream(stream_infer)

def get_time():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))