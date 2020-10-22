from threading import Timer
from load_lite import main as ml_main
from stream_sensor_consumer import read_sensor,write_infer
from json import loads,dumps

import sql

def main():
    try:
        sql.connect()
        res = []
        msgs = read_sensor()#从流中读出多个消息
        if msgs:
            for msg in msgs:
                for r in loads(msg.payload.decode()):#一个消息包含多条记录
                    lable = ml_main([r[1:]])#去掉第一个时间戳字段、合成二维数组，运行推理模型
                    r.append(lable)
                    res.append(r)
            sql.insert(res)
    except Exception as e:
        print(e)
        pass
    Timer(30, main).start()

main()

def lambda_handler(event, context):
    return