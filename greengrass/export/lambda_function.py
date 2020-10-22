from threading import Timer
from export_stream import open_client,export_file_tos3
from sql import select,connect

import sql

def main():
    try:
        connect()
        select()
        #open_client()
        #export_file_tos3()
    except Exception as e:
        print(e)
        pass
    Timer(60, main).start()

main()

def lambda_handler(event, context):
    return