from threading import Timer
from export_stream import export_file_tos3,read_infer
'''
from sql import select,connect
import sql
connect()
select()
'''

def main():
    try:
        read_infer()
        #open_client()
        #export_file_tos3()
    except Exception as e:
        print(e)
        pass
    Timer(20, main).start()

main()

def lambda_handler(event, context):
    return