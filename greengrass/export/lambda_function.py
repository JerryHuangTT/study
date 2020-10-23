from threading import Timer
from export_stream import open_client,read_infer#,export_file_tos3
'''
from sql import select,connect
import sql
connect()
select()
'''

def main():
    try:
        open_client()
        read_infer()
        #export_file_tos3()
    except Exception as e:
        print(e)
        pass
    Timer(86400, main).start()#86400

main()

def lambda_handler(event, context):
    return