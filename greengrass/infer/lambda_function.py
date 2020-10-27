from threading import Timer
from load_lite import main as ml_main
from stream_sensor import read_sensor
from stream_infer import write_infer
from json import loads,dumps
#import sql

import uuid
mac = uuid.UUID(int = uuid.getnode()).hex[-12:].upper()

import greengrasssdk          
client = greengrasssdk.client('iot-data')

def main():
    try:
        t_count = 0 #0是正常标签
        #sql.connect()
        res = []
        msgs = read_sensor()#从流中读出多个消息
        if msgs:
            for msg in msgs:
                for r in loads(msg.payload.decode()):#一个消息包含多条记录
                    lable = ml_main([r[1:]])#去掉第一个时间戳字段、合成二维数组，运行推理模型
                    if lable == 0 :
                        t_count += 1
                    r.append(lable)
                    res.append(r)
            #sql.insert(res)
            print(res[0])
            write_infer(dumps(res))
            tag = True
            if t_count / len(res) < 0.9:
                tag = False
                
            send_2iot({'mac':mac,'tag':tag})
    except Exception as e:
        print(e)
        pass
    Timer(30, main).start()

main()

def send_2iot(data):
    client.publish(
    topic = 'gg/infer',
    qos = 0,
    payload = dumps(data).encode())

def lambda_handler(event, context):
    return