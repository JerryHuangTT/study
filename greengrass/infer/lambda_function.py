from threading import Timer
from  load_lite import main as ml_main
from stream_sensor_consumer import main as stream_main
def main():
    try:
        labels = []
        datas = stream_main()
        for data in datas: 
            lable = ml_main(data)
            labels.append(lable)
            
    except Exception as e:
        print(e)
    Timer(30, main).start()

main()

def lambda_handler(event, context):
    return