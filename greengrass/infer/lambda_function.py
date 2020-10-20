from threading import Timer
from load_lite import main as ml_main
from stream_sensor_consumer import read,write
from json import loads,dumps

def main():
    try:
        labels = []
        datas = read()
        if datas:
            for data in datas:
                record = loads(data.payload.decode())
                #一个记录100个传感器数据
                for r in record:
                    #print(r[0])
                    d = r[1:] #去掉第一个时间戳字段
                    lable = ml_main([d])
                    #print(lable)
                    labels.append(lable)
            print(labels)
            write(dumps(labels))
    except Exception as e:
        print(e)
        pass
    Timer(30, main).start()

main()

def lambda_handler(event, context):
    return