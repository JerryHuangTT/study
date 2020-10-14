from threading import Timer
from  load_lite import main as ml_main
from stream_sensor_consumer import main as stream_main
from json import loads
def main():
    try:
        labels = []
        datas = stream_main()
        if datas:
            for data in datas:
                print(data.sequence_number)
                for a in loads(data.payload.decode()):
                    lable = ml_main([a])
                    #print(lable)
                    labels.append(lable)
            print(labels)
    except Exception as e:
        print(e)
        pass
    Timer(30, main).start()

main()

def lambda_handler(event, context):
    return