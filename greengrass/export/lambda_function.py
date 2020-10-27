from threading import Timer
from export_stream import open_client,read_infer
import schedule

def job():
    open_client()
    read_infer()

schedule.every().day.at("03:00").do(job)

def main():
    try:
        schedule.run_pending()
    except Exception as e:
        print(e)
        pass
    Timer(5, main).start()

main()

def lambda_handler(event, context):
    return